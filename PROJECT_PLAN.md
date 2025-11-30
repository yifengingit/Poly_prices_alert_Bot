# PolyStatics - Project Plan

## 1. 项目愿景 (Vision)
打造 Polymarket 生态最专业的数据分析与筛选工具，帮助交易者发现错误定价、监控巨鲸动向、优化投资组合。

## 2. 敏捷开发策略 (Agile Strategy)
*   **原则**: "Ship Early, Ship Often"
*   **当前重心**: Telegram 实时机会监控机器人 (Volatility Monitor)。

## 3. 路线图 (Roadmap)

### 🟢 Phase 1: 核心数据服务 (Core Data Service) - [✅ Completed]
- [x] **环境搭建**: Git, uv, FastAPI 结构。
- [x] **API Client**: 封装 Polymarket Gamma API。
- [x] **Web API**: `/markets` 接口 (支持排序、缓存)。

### 🔵 Phase 1.5: Telegram 机会猎手 (Telegram Opportunity Hunter) - [🚀 Current Focus]
**目标**: 监控短时间内的剧烈波动，自动发送告警。
- [x] **Bot 基础**: 申请 Bot Token (已完成: `796...CJo`)。
- [ ] **快照引擎 (Snapshot Engine)**: 
    - 实现“内存快照对比”机制。
    - 每 10 秒拉取一次市场，对比上一轮价格。
- [ ] **波动分析 (Volatility Analysis)**:
    - **核心指标**: 重点监控 **Last Trade Price (最新成交价)**。
    - **阈值**: 1m/5m 内涨跌幅 > 20%。
    - **过滤杂音**: 
        - Liquidity > $5,000 (流动性过滤)。
        - Spread Filter (点差过滤，具体阈值待定)。
- [ ] **告警推送**: 发送包含 Question, Price Change, Link, Liquidity, Last Price 的富文本消息。

### 🟡 Phase 2: Web 数据看板 (Web Dashboard) - [⏸️ Paused]
**状态**: 框架已搭建 (Next.js + Tailwind)，暂停开发以优先 Bot。
- [ ] **市场列表**: 对接后端 API 展示数据。
- [ ] **K 线图表**: 整合 TradingView。

### 🔴 Phase 3: 深度分析 (Advanced Analytics)
- [ ] **历史数据**: 引入数据库存储历史价格。
- [ ] **套利矩阵**: 监控 Group Markets 套利机会。

## 4. 技术栈 (Tech Stack)

### Backend & Bot
*   **Framework**: FastAPI (API) + Asyncio Loop (Bot)
*   **Data**: Polymarket Gamma API
*   **Notification**: Telegram Bot API (HTTPX)

### Frontend (Paused)
*   **Framework**: Next.js 14
