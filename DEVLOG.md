# 📅 开发日记 (DevLog)

本文档用于记录项目的开发历程、技术决策与重要更新。采用倒序或顺序追加记录。

---

## 📝 记录日期: 2025-11-30 (Phase 1.5 Completed)
**记录人**: Web3 Architect & Mentor (AI)
**当前版本**: v0.1.0

### 1. 项目概况 (Project Overview)
**PolyStatics** 是一个针对 Polymarket 预测市场的高频波动率监控工具。
目前已完成 **Telegram 告警机器人** 的开发与部署，能够实时捕获市场价格的剧烈波动（Pump/Dump）并推送通知。

### 2. 当前功能 (Current Features)

#### 🤖 Telegram 波动率机器人
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

#### 🏗️ 基础设施
*   **语言**: Python 3.12
*   **包管理**: `uv` (代替 pip/poetry)
*   **部署**: Docker + Docker Compose (基于 Debian 12)
*   **并发**: 使用 `asyncio` + `httpx` 并发分页拉取 Polymarket API 数据（突破 500 条限制）。

### 3. 关键技术决策 (Technical Decisions)
1.  **价格来源确认**: 经脚本验证，Polymarket API 返回的 `lastTradePrice` 在二元市场中锚定的是 **Yes** 的价格。
2.  **内存架构**: 鉴于数据量（5000+ 市场）和实时性要求，目前使用 **内存快照 (In-Memory Snapshot)** 存储历史价格，暂未使用 Redis/SQL。这大大降低了部署复杂度。
3.  **API 优化**: 实现了并发分页 (Parallel Pagination) 以在 2 秒内完成 5700+ 个市场的数据同步。

### 4. 部署信息 (Deployment)
*   **服务器**: 日本双 ISP VPS (Debian 12, 1核 1G)。
*   **部署方式**: 使用 `deploy.ps1` 脚本一键自动化部署。
*   **路径**: `/root/polystatics`
*   **注意**: `deploy.ps1` 和 `setup_remote.sh` 包含敏感服务器信息，**严禁上传到公开 Git 仓库** (已加入 .gitignore)。

---

## 📝 记录日期: 2025-12-07 (Strategy Tuning & Architecture)
**记录人**: Web3 Architect & Mentor (AI)
**主题**: 策略调优与架构思考

### 1. 🔄 策略调整 (Strategy Tuning)

#### 问题描述
用户反馈“信号太多”，存在大量噪音。
分析发现，许多低流动性或交易不活跃的市场，因为几笔小额交易导致价格剧烈跳变（如从 0.01 变 0.02，涨幅 100%），但这并不具备套利价值。

#### 调整方案
1.  **提高波动率阈值**: 将 5 分钟波动率阈值从 `10%` 提高到 **`25%`**。
    *   *理由*: 10% 在 Crypto 预测市场中确实太常见了。25% 更能过滤出真正的“事件驱动”行情。
2.  **新增成交量过滤**: 新增 `VOLUME_THRESHOLD = 1000` (24h Volume)。
    *   *理由*: 仅看 Liquidity 是不够的（有些市场有流动性但没人玩）。只有 24小时成交量 > $1000 的市场才被视为“活跃市场”，值得监控。

### 2. 🏛️ 架构思考: Polling vs WebSocket

#### 用户疑问
> 是保持现在的五分钟查一次（实际是2秒轮询），还是使用 WebSocket？

#### 架构师分析
对于 **“全网扫描 (Global Scanner)”** 场景，目前采用的 **HTTP Polling (2s Interval)** 方案优于 WebSocket。

**Polling (当前方案) 的优势**:
1.  **全局视角**: 我们需要监控 5700+ 个市场。Polymarket API `/markets` 接口经过优化，适合批量拉取快照。
2.  **状态管理简单**: 不需要维护 5000 个 WebSocket 连接或处理复杂的 Subscription 逻辑。
3.  **鲁棒性**: HTTP 请求失败重试即可；WebSocket 断连需要处理重连、状态同步、丢包等复杂问题。
4.  **API 限制**: 只有少数机构级 API (如 Clob Client) 支持高效的 Firehose 模式。对于免费/公开 API，高频轮询是最稳妥的。

**WebSocket 的适用场景**:
*   高频交易 (HFT)
*   只监控特定的几个市场 (Watchlist)
*   需要毫秒级反应速度

**结论**: 维持 Polling 架构，重点优化过滤逻辑。
