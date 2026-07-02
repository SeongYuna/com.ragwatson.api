from __future__ import annotations

import os

import httpx

from teaching_assistant_spoke.app.ports.output.receiver_port import TelegramNotifierPort

_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
_TELEGRAM_URL = f"https://api.telegram.org/bot{_BOT_TOKEN}/sendMessage"


class TelegramNotifierAdapter(TelegramNotifierPort):
    async def send(self, message: str) -> bool:
        if not _BOT_TOKEN or not _CHAT_ID:
            return False
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                _TELEGRAM_URL,
                json={"chat_id": _CHAT_ID, "text": message},
            )
            return response.status_code == 200
