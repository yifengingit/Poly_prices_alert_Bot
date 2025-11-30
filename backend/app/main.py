from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from typing import List
from .schemas import Market
from .services.polymarket import polymarket_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    print("🚀 PolyStatics Backend Starting...")
    yield
    # 关闭时执行
    print("🛑 Shutting down...")
    await polymarket_client.close()

app = FastAPI(
    title="PolyStatics API",
    description="Backend for Polymarket Analytics",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "PolyStatics API is running", "status": "ok"}

@app.get("/markets", response_model=List[Market])
async def get_markets(
    limit: int = Query(20, description="返回数量"),
    sort_by: str = Query("volume24hr", description="排序字段 (volume24hr, liquidity, createdAt)"),
    ascending: bool = Query(False, description="是否升序")
):
    """
    获取市场列表 (Cached 10s)
    """
    markets = await polymarket_client.get_markets(
        limit=limit, 
        order=sort_by, 
        ascending=ascending
    )
    return markets
