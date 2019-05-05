

class EmptyAsyncGenerator():

    __slots__ = ()

    def __aiter__(self):
        return self

    async def __anext__(self):
        raise StopAsyncIteration()


def chunked(request):

    def chunked_request():

        async def chunked_body(body):
            async for chunk in body:
                length = len(chunk)
                yield hex(length)[2:] + b'\r\n'
                yield chunk
                yield b'\r\n'

            # Final 0-length-chunk
            yield b'0\r\n\r\n'

        async def _request(method, url, params=(), headers=(), body=EmptyAsyncGenerator()):
            return await request(
                method, url, params, headers + ((b'transfer-encoding', b'chunked'),),
                chunked_body(body),
            )

    return chunked_request
