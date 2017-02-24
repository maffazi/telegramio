import json
from telegramio.log import logger
from telegramio.transport import HttpProtocol


TRACK_URL = 'https://api.botan.io/track'
SHORTENER_URL = 'https://api.botan.io/s/'


class Botan(HttpProtocol):

    def __init__(self, botan):
        self.tracked_messages = 0

        self._botan = botan

    async def track(self, message, name='Message'):
        if self._botan is not None:
            headers = {'Content-type': 'application/json'}
            params = {"token": self._botan, "uid": message['chat']['id'], "name": name}
            result = await self.request(url=TRACK_URL, params=params, data=json.dumps(message), headers=headers)
            result = json.loads(result)
            logger.info('Message tracking return %s,' % result)
        else:
            logger.info('Message not tracking, botan token is None')

    async def shorten_url(self, url, user_id):
        if self._botan is not None:
            params = {"token": self._botan, "user_ids": user_id, "url": url}
            result, seq = await self.request(url=SHORTENER_URL, params=params)
            return result
        else:
            logger.info('Botan token is None')
