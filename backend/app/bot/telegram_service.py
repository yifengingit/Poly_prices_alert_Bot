import httpx
import os
import asyncio
from typing import Optional

class TelegramService:
    def __init__(self, token: str, chat_id: Optional[str] = None):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.client = httpx.AsyncClient(timeout=10.0)

    async def send_message(self, text: str, parse_mode: str = "HTML") -> bool:
        """
        发送消息到指定 Chat ID
        """
        if not self.chat_id:
            print("⚠️ Telegram Chat ID not set. Skipping message.")
            return False

        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": True
        }
        
        try:
            resp = await self.client.post(url, json=payload)
            resp.raise_for_status()
            return True
        except Exception as e:
            print(f"❌ Failed to send Telegram message: {e}")
            return False

    async def get_updates(self) -> dict:
        """
        获取最新消息（用于获取 Chat ID）
        """
        url = f"{self.base_url}/getUpdates"
        try:
            resp = await self.client.get(url)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ Failed to get updates: {e}")
            return {}

    async def close(self):
        await self.client.aclose()
