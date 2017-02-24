import asyncio

from telegramio.telegram import Telegram
from telegramio.botan import Botan
from telegramio.log import logger


class Telegramio(Telegram, Botan):

    def __init__(self, telegram, botan=None, loop=asyncio.get_event_loop(), last_id=0, proxy=None,
                 retry_if_fail=True, retry_intreval=60.0):
        Telegram.__init__(self, loop, telegram, proxy, retry_if_fail,10, retry_intreval)
        Botan.__init__(self, botan)
        self.message_counter = 0

        self._run = True
        self._last_id = last_id
        self._message = None
        self._inline_query = None
        self._edited_message = None
        self._callback_query = None
        self._chosen_inline_result = None

    async def get_updates_loop(self):
        while self._run:
            updates = await self.getUpdates(self._last_id + 1)
            tasks = []
            for upd in updates:
                self.message_counter += 1
                self._last_id = max(self._last_id, upd['update_id'])
                tasks.append(asyncio.Task(self._update_parser(upd)))
            asyncio.gather(*tasks, return_exceptions=True)

    async def _update_parser(self, upd):
        if 'message' in upd.keys():
            await self._message(upd['message'])
        elif 'edited_message' in upd.keys():
            await self._edited_message(upd['edited_message'])
        elif 'inline_query' in upd.keys():
            await self._inline_query(upd['inline_query'])
        elif 'chosen_inline_result' in upd.keys():
            await self._chosen_inline_result(upd['chosen_inline_result'])
        elif 'callback_query' in upd.keys():
            await self._callback_query(upd['callback_query'])

    def message(self, callback):
        self._message = callback
        return callback

    def inline_query(self, callback):
        self._inline_query = callback
        return callback

    def edited_message(self, callback):
        self._edited_message = callback
        return callback

    def callback_query(self, callback):
        self._callback_query = callback
        return callback

    def chosen_inline_result(self, callback):
        self._chosen_inline_result = callback
        return callback

