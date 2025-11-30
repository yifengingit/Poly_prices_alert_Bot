import httpx
import json
import time
import asyncio
from typing import List, Dict, Any
from ..schemas import Market, MarketOutcome

class PolymarketClient:
    BASE_URL = "https://gamma-api.polymarket.com/markets"
    
    def __init__(self, cache_ttl: int = 2):
        """
        :param cache_ttl: 缓存有效期（秒），机器人需要极速响应，设为 2 秒
        """
        # 缓存结构: { "cache_key": {"data": [...], "timestamp": 123456} }
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = cache_ttl
        self.client = httpx.AsyncClient(timeout=10.0)

    async def get_markets(self, limit: int = 20, order: str = "volume24hr", ascending: bool = False) -> List[Market]:
        """
        获取市场列表，支持排序和缓存。
        如果 limit > 500，会自动并发请求分页数据。
        """
        # 生成唯一的缓存 Key
        cache_key = f"markets_{limit}_{order}_{ascending}"
        current_time = time.time()
        
        # 1. 检查缓存
        cached_item = self._cache.get(cache_key)
        if cached_item and (current_time - cached_item["timestamp"] < self._cache_ttl):
            print(f"⚡ Using In-Memory Cache for key: {cache_key}")
            return cached_item["data"]

        # 2. 如果缓存过期，请求 API
        # Polymarket API 单次最大返回 500 条
        MAX_PAGE_SIZE = 500
        
        try:
            if limit <= MAX_PAGE_SIZE:
                markets = await self._fetch_page(limit, 0, order, ascending)
            else:
                # 并发分页请求
                print(f"🌍 Fetching {limit} markets in parallel pages...")
                tasks = []
                for offset in range(0, limit, MAX_PAGE_SIZE):
                    # 最后一页可能不满 500
                    page_limit = min(MAX_PAGE_SIZE, limit - offset)
                    tasks.append(self._fetch_page(page_limit, offset, order, ascending))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                markets = []
                for res in results:
                    if isinstance(res, list):
                        markets.extend(res)
                    else:
                        print(f"⚠️ Page fetch failed: {res}")

            # 3. 更新缓存
            self._cache[cache_key] = {
                "data": markets,
                "timestamp": current_time
            }
            return markets
            
        except Exception as e:
            print(f"❌ API Error: {e}")
            if cached_item:
                print("⚠️ Returning stale cache due to API error")
                return cached_item["data"]
            return []

    async def _fetch_page(self, limit: int, offset: int, order: str, ascending: bool) -> List[Market]:
        """内部方法：获取单页数据"""
        params = {
            "limit": limit,
            "offset": offset,
            "order": order,
            "ascending": str(ascending).lower(),
            "closed": False
        }
        # print(f"  -> Fetching page offset={offset}, limit={limit}...")
        response = await self.client.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        markets = []
        for item in data:
            try:
                outcomes_list = json.loads(item.get("outcomes", "[]"))
                prices_list = json.loads(item.get("outcomePrices", "[]"))
                
                market_outcomes = []
                if outcomes_list and prices_list and len(outcomes_list) == len(prices_list):
                    for name, price in zip(outcomes_list, prices_list):
                        market_outcomes.append(MarketOutcome(name=name, price=float(price)))
                
                # Parse Event Slug
                event_slug = ""
                events_data = item.get("events", [])
                if events_data and isinstance(events_data, list) and len(events_data) > 0:
                    # Take the first event's slug
                    event_slug = events_data[0].get("slug", "")
                
                market = Market(
                    id=item.get("id", ""),
                    question=item.get("question", "Unknown"),
                    slug=item.get("slug", ""),
                    event_slug=event_slug,
                    volume_24h=float(item.get("volume24hr", 0) or 0),
                    liquidity=float(item.get("liquidity", 0) or 0),
                    last_trade_price=float(item.get("lastTradePrice", 0) or 0),
                    spread=float(item.get("spread", 0) or 0),
                    outcomes=market_outcomes,
                    end_date=item.get("endDate")
                )
                markets.append(market)
            except Exception as e:
                continue
        return markets

    async def close(self):
        await self.client.aclose()

# 单例模式：整个应用只用一个 Client 实例
# TTL 设置为 2 秒，配合机器人的极速扫描
polymarket_client = PolymarketClient(cache_ttl=2)
