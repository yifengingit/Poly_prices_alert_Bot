# PolyStatics Bot 🤖

> **Real-time Volatility Alert Bot for Polymarket**
>
> 🔴 **Live Channel**: [https://t.me/poly_volume_alert](https://t.me/poly_volume_alert)

PolyStatics Bot is a high-frequency monitoring tool designed to catch "Pump & Dump" movements on Polymarket. It scans the top 5000+ liquid markets every 2 seconds and sends instant alerts when a price changes significantly.

## ✨ Features

*   **⚡️ Real-time Monitoring**: Scans ~5,700 markets every 2 seconds.
*   **🌊 Liquidity Filter**: Only monitors markets with Liquidity > $5,000 (filters out junk markets).
*   **📉 Volatility Detection**: Triggers alert if "Last Trade Price" changes by **≥10%** within **5 minutes**.
*   **🔗 Smart Linking**: Generates direct links to the specific market event (handles `event_slug` vs `slug` logic).
*   **🛡️ Spam Protection**:
    *   **Cooldown**: 5-minute silence period per market after an alert.
    *   **Auto-Pruning**: Efficient memory management for historical data.

## 🛠️ Tech Stack

*   **Core**: Python 3.12, `asyncio`, `httpx`
*   **Package Manager**: `uv` (The Astral Project)
*   **Deployment**: Docker, Docker Compose
*   **Integration**: Telegram Bot API

## 🚀 Getting Started

### Prerequisites
*   Python 3.10+
*   `uv` installed (or use pip)
*   A Telegram Bot Token

### 1. Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/yifengingit/Poly_prices_alert_Bot.git
cd Poly_prices_alert_Bot

# Install dependencies with uv
uv sync
```

### 2. Configuration

Copy the example environment file and edit it:

```bash
cp .env.example .env
```

Fill in your Telegram credentials in `.env`:
```ini
TELEGRAM_BOT_TOKEN=your_token_here
TELEGRAM_CHAT_ID=your_channel_id_here
```

### 3. Run Locally

```bash
# Run the bot
uv run backend/app/bot/main.py
```

### 4. Run with Docker (Recommended)

```bash
docker compose up -d --build
```

## 📂 Project Structure

*   `backend/app/bot`: Core bot logic (Volatility Monitor, Telegram Service).
*   `backend/app/services`: Polymarket API client (Async, Parallel Pagination).
*   `scripts/`: Utility scripts (e.g., checking price sources).

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

[MIT](LICENSE)
