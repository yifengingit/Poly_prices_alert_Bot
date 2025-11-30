import asyncio
import time
from typing import Dict, Deque
from collections import deque
from backend.app.services.polymarket import polymarket_client
from backend.app.schemas import Market
from backend.app.bot.telegram_service import TelegramService

class VolatilityMonitor:
    def __init__(self, telegram_service: TelegramService):
        self.telegram = telegram_service
        # Snapshots: { market_id: { "price": float, "last_updated": float, "history": deque } }
        self.snapshots: Dict[str, Dict] = {}
        self.is_running = False
        
        # Config
        self.CHECK_INTERVAL = 2  # seconds (Aggressive polling)
        self.LIQUIDITY_THRESHOLD = 5000  # $5,000
        self.VOLATILITY_THRESHOLD = 0.10  # 10%
        # Max history points needed: 5 mins (300s) / 2s interval = 150 points. 
        # Give some buffer, say 200 points.
        self.MAX_HISTORY_LEN = 200
        
    async def start(self):
        print("🚀 Volatility Monitor Started...")
        self.is_running = True
        while self.is_running:
            try:
                await self.cycle()
            except Exception as e:
                print(f"❌ Error in monitor cycle: {e}")
            
            await asyncio.sleep(self.CHECK_INTERVAL)

    async def stop(self):
        self.is_running = False

    async def cycle(self):
        # 1. Get Top Markets by Volume (Liquidity sort is broken on API side)
        markets = await polymarket_client.get_markets(limit=5700, order="volume24hr", ascending=False)
        print(f"🔍 Scanned {len(markets)} markets. (Limit set to 5700)")
        
        current_time = time.time()
        
        for market in markets:
            # 2. Filter by Liquidity
            if market.liquidity < self.LIQUIDITY_THRESHOLD:
                continue
                
            # Use Last Trade Price if available, else fallback (maybe 0.5 for binary? No, safer to skip if 0)
            price = market.last_trade_price
            if price is None or price <= 0:
                # Fallback to outcome prices if needed, but user emphasized Last Trade Price
                # Let's try to find the "Yes" price if outcome is binary
                # But for now, skip if no valid price
                continue

            market_id = market.id
            
            # 3. Initialize or Update Snapshot
            if market_id not in self.snapshots:
                self.snapshots[market_id] = {
                    "current_price": price,
                    "last_updated": current_time,
                    # Use deque with fixed size for automatic pruning
                    "history": deque(maxlen=self.MAX_HISTORY_LEN),
                    "last_alert_time": 0
                }
                # Don't continue, we might want to add the first point immediately
            
            # 4. Volatility Check
            prev_data = self.snapshots[market_id]
            history: Deque = prev_data["history"]
            
            # Add current to history (Auto-removes oldest if full)
            history.append((current_time, price))
            
            # Update current state
            self.snapshots[market_id]["current_price"] = price
            self.snapshots[market_id]["last_updated"] = current_time
            
            # Check 5m changes
            await self.check_volatility(market, price, history, current_time)

    async def check_volatility(self, market: Market, current_price: float, history: Deque, now: float):
        # Check Cooldown First (Optimization: Don't calculate if cooled down)
        last_alert_time = self.snapshots[market.id].get("last_alert_time", 0)
        if now - last_alert_time < 300:  # 5 minutes cooldown
            return

        # Find closest data points for 5m (300s) ago
        # Allow a small window (e.g., +/- 10s)
        
        price_5m = None
        
        for ts, p in history:
            age = now - ts
            # Look for data point around 5 mins ago (290s - 310s)
            if 290 <= age <= 310 and price_5m is None:
                price_5m = p
        
        # Calculate changes
        if price_5m:
            change_5m = (current_price - price_5m) / price_5m
            if abs(change_5m) >= self.VOLATILITY_THRESHOLD:
                await self.send_alert(market, "5m", change_5m, current_price, price_5m)
                self.snapshots[market.id]["last_alert_time"] = now

        # Queue notifications to avoid flooding
        # (Ideally, use a dedicated queue system, but for now, simple sleep works)
        # await asyncio.sleep(1) 
        pass

    async def send_alert(self, market: Market, period: str, change: float, current: float, old: float):
        direction = "🚀 PUMP" if change > 0 else "🔻 DUMP"
        percent = change * 100
        
        # Fix URL: Prefer Event Slug, fallback to Market Slug
        # 1. Try event_slug (e.g., "time-2025-person-of-the-year")
        # 2. Try slug (e.g., "will-volodymyr-zelenskyy...")
        # 3. Fallback to "market"
        
        url_slug = market.event_slug if market.event_slug else (market.slug if market.slug else "market")
        
        msg = (
            f"<b>{direction} Alert ({period})</b>\n\n"
            f"❓ <b>Question:</b> {market.question}\n"
            f"📉 <b>Change:</b> {percent:+.2f}%\n"
            f"💲 <b>Price:</b> ${old:.3f} ➡️ ${current:.3f}\n"
            f"💧 <b>Liquidity:</b> ${market.liquidity:,.0f}\n"
            f"🔗 <a href=\"https://polymarket.com/event/{url_slug}?tid={market.id}\">View Market</a>"
        )
        
        print(f"🔔 Triggering Alert: {market.question} ({percent:.2f}%)")
        await self.telegram.send_message(msg)
        # Add a small delay to prevent Telegram rate limits if multiple alerts trigger at once
        await asyncio.sleep(0.5)

