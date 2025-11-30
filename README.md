# PolyStatics 📊

> Polymarket Advanced Analytics & Screener

PolyStatics 是一个专注于 Polymarket 预测市场的数据分析工具。它旨在帮助交易者发现高价值的投资机会，提供比官方界面更丰富的筛选维度和深度分析。

## ✨ Features

*   **🚀 Market Screener**: 实时筛选热门、高流动性或剧烈波动的市场。
*   **📈 Advanced Charts**: (Coming Soon) 专业级 K 线与深度图。
*   **🐋 Whale Alerts**: (Coming Soon) 链上大单监控。

## 🛠️ Tech Stack

*   **Backend**: Python, FastAPI, `uv`
*   **Frontend**: Next.js, Tailwind CSS
*   **Data**: Polymarket Gamma API

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   Node.js 18+
*   `uv` package manager

### Backend Setup

1.  Initialize environment:
    ```bash
    uv sync
    ```
2.  Run server:
    ```bash
    uv run fastapi dev
    ```

### Frontend Setup

1.  Install dependencies:
    ```bash
    cd frontend
    npm install
    ```
2.  Run development server:
    ```bash
    npm run dev
    ```
