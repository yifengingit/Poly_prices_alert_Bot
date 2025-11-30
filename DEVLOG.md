# 📅 开发日记 (DevLog)

**记录日期**: 2025-11-30
**记录人**: Web3 Architect & Mentor (AI)
**当前版本**: v0.1.0 (Phase 1.5 Completed)

---

## 1. 项目概况 (Project Overview)
**PolyStatics** 是一个针对 Polymarket 预测市场的高频波动率监控工具。
目前已完成 **Telegram 告警机器人** 的开发与部署，能够实时捕获市场价格的剧烈波动（Pump/Dump）并推送通知。

## 2. 当前功能 (Current Features)

### 🤖 Telegram 波动率机器人
*   **监控范围**: 全网成交量前 5700 名的市场。
*   **过滤条件**:
    *   流动性 (Liquidity) > $5,000 USD。
    *   排除已关闭 (Closed) 的市场。
*   **触发机制**:
    *   扫描频率: 每 2 秒一次。
    *   波动阈值: 最新成交价 (Last Trade Price) 在 5 分钟内变化幅度 >= 10%。
*   **防骚扰机制**:
    *   冷却时间 (Cooldown): 同一市场触发报警后，5 分钟内不再重复报警。
    *   数据清理: 自动维护最近 200 个价格点的滑动窗口，防止内存溢出。
*   **告警内容**:
    *   涨跌方向 (🚀 PUMP / 🔻 DUMP)
    *   问题描述 (Question)
    *   变化幅度 (Change %)
    *   价格变化 (Old -> New)
    *   当前流动性
    *   **直达链接**: 智能解析 Event Slug，生成可点击的 Polymarket 详情页链接。

### 🏗️ 基础设施
*   **语言**: Python 3.12
*   **包管理**: `uv` (代替 pip/poetry)
*   **部署**: Docker + Docker Compose (基于 Debian 12)
*   **并发**: 使用 `asyncio` + `httpx` 并发分页拉取 Polymarket API 数据（突破 500 条限制）。

## 3. 关键技术决策 (Technical Decisions)
1.  **价格来源确认**: 经脚本验证，Polymarket API 返回的 `lastTradePrice` 在二元市场中锚定的是 **Yes** 的价格。
2.  **内存架构**: 鉴于数据量（5000+ 市场）和实时性要求，目前使用 **内存快照 (In-Memory Snapshot)** 存储历史价格，暂未使用 Redis/SQL。这大大降低了部署复杂度。
3.  **API 优化**: 实现了并发分页 (Parallel Pagination) 以在 2 秒内完成 5700+ 个市场的数据同步。

## 4. 部署信息 (Deployment)
*   **服务器**: 日本双 ISP VPS (Debian 12, 1核 1G)。
*   **部署方式**: 使用 `deploy.ps1` 脚本一键自动化部署。
*   **路径**: `/root/polystatics`
*   **注意**: `deploy.ps1` 和 `setup_remote.sh` 包含敏感服务器信息，**严禁上传到公开 Git 仓库** (已加入 .gitignore)。

## 5. 已知问题与待办 (Known Issues & TODOs)
*   **[待观察]** 报警阈值 (10%/5min) 是否过于敏感或迟钝？需根据实际运行数据调整。
*   **[待开发]** 前端 Dashboard (Next.js) 目前仅搭建了框架，尚未接入后端数据。
*   **[待优化]** 目前日志仅输出到 Docker console，未来可考虑接入专门的日志系统。

## 6. 交接备注 (Handover Notes)
*   **代码库**: 核心逻辑在 `backend/app/bot/volatility_monitor.py`。
*   **启动命令**: 本地开发用 `uv run backend/app/bot/main.py`，服务器用 `docker compose up -d`。
*   **环境变量**: 必须配置 `.env` 文件中的 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAM_CHAT_ID`。

---
*End of Log*
