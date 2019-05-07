import asyncio
import unittest

from aiohttp import (
    web,
)

from lowhaio import (
    Pool,
    buffered,
)
from lowhaio_chunked import (
    chunked,
)


def async_test(func):
    def wrapper(*args, **kwargs):
        future = func(*args, **kwargs)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(future)
    return wrapper


class TestIntegration(unittest.TestCase):

    def add_async_cleanup(self, coroutine, *args):
        loop = asyncio.get_event_loop()
        self.addCleanup(loop.run_until_complete, coroutine(*args))

    @async_test
    async def test_http_chunked_request(self):
        request_datas = []
        request_encodings = []

        data = b'abcdefghijklmnopqrstuvwxyz'
        chunk_size = None

        async def handle_get(request):
            request_datas.append(await request.content.read())
            request_encodings.append(request.headers['transfer-encoding'])
            return web.Response()

        app = web.Application()
        app.add_routes([
            web.get('/page', handle_get)
        ])
        runner = web.AppRunner(app)
        await runner.setup()
        self.add_async_cleanup(runner.cleanup)
        site = web.TCPSite(runner, '0.0.0.0', 8080)
        await site.start()

        request, close = Pool()
        self.add_async_cleanup(close)

        async def chunked_data(chunk_size):
            chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
            for chunk in chunks:
                yield chunk

        for chunk_size in range(1, 27):
            _, _, body = await request(
                b'GET', 'http://localhost:8080/page',
                headers=((b'transfer-encoding', b'chunked'),),
                body=chunked(chunked_data),
                body_kwargs=(('chunk_size', chunk_size),),
            )
            await buffered(body)

        self.assertEqual(request_datas, [data] * 26)
        self.assertEqual(request_encodings, ['chunked']*26)
