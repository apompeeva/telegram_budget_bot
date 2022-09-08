from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from typing import List


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_ids: List):
        self.allowed_ids = allowed_ids
        super().__init__()

    async def on_process_message(self, message: types.Message, _):
        if int(message.from_user.id) not in self.allowed_ids:
            await message.answer("Access Denied")
            raise CancelHandler()

