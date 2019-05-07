def chunked(body):
    async def _chunked(*args, **kwargs):
        async for chunk in body(*args, **kwargs):
            yield hex(len(chunk))[2:].encode() + b'\r\n'
            yield chunk
            yield b'\r\n'
        yield b'0\r\n\r\n'
    return _chunked
