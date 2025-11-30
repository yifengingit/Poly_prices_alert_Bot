import asyncio
import os
import sys
from dotenv import load_dotenv

# Fix path to import backend modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from backend.app.bot.telegram_service import TelegramService
from backend.app.bot.volatility_monitor import VolatilityMonitor
from backend.app.services.polymarket import polymarket_client

load_dotenv()

async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN is missing!")
        return
    
    if not chat_id:
        print("⚠️ TELEGRAM_CHAT_ID is missing! Alerts will not be sent.")
        print("👉 Run 'uv run scripts/setup_telegram.py' to setup.")
    
    print("🤖 Starting PolyStatics Bot...")
    
    telegram = TelegramService(token=token, chat_id=chat_id)
    
    # Send startup message
    if chat_id:
        await telegram.send_message("👀 <b>PolyStatics Monitor Started</b>\nScanning for volatility > 20%...")
    
    monitor = VolatilityMonitor(telegram_service=telegram)
    
    try:
        await monitor.start()
    except KeyboardInterrupt:
        print("\n🛑 Stopping Bot...")
    finally:
        await telegram.close()
        await polymarket_client.close()

if __name__ == "__main__":
    asyncio.run(main())
