import asyncio
import aiohttp
import async_timeout
from aiohttp.errors import *
from telegramio.log import logger


class HttpProtocol(object):

    def __init__(self, loop, proxy=None, retry_fail=False, retry_count=10, retry_interval=60):
        """
        :param loop: Event loop used for processing HTTP requests.
        :param proxy: Dictionary with proxies,
        :param retry_fail: Retry request if failed, default False
        :param retry_count: Count of request retry
        :param retry_interval: Time to wait before next request retry
        """
        self.tlgrm_loop = loop
        self.protocol_errors = 0

        self._session = None
        self._proxy = proxy
        self._request_seq = 0
        self._retry_fail = retry_fail
        self._retry_count =  retry_count if retry_count < 100 else 100
        self._retry_interval = retry_interval

    async def request(self, url, method='GET', timeout=30, retries = 0, **kwargs):
        if self._session is None:
            self._session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=30), loop=self.tlgrm_loop)
        self._request_seq +=1
        seq = self._request_seq
        logger.info("seq %s: %s" % (seq, url))
        for key, value in sorted(kwargs.items()):
            logger.debug("seq %s: %s=%s" % (seq, key, value))
        try:
            with async_timeout.timeout(timeout, loop=self.tlgrm_loop):
                async with self._session.request(method, url, proxy=self._proxy, **kwargs) as response:
                    logger.info("seq %s: %s %s %s" % (seq, method, url, response.status))
                    if response.status == 200:
                        resp = await response.text()
                        logger.debug("seq %s: response=%s" % (seq,resp))
                        return resp
                    else:
                        raise HttpProcessingError(code=response.status, message=response.reason)
        except (HttpProcessingError, HttpProxyError, ClientOSError, asyncio.TimeoutError, ClientResponseError) as exc:
            logger.error("seq %s: %s" %(seq, exc))
            self.protocol_errors += 1
            if self._retry_fail and retries < self._retry_count:
                logger.error("seq %s: Request will retry at %s second" % (seq,self._retry_interval))
                await asyncio.sleep(self._retry_interval)
                await self.request(url, method, timeout, retries + 1, **kwargs)
            else:
                return None
