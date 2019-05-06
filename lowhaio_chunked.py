
async def chunked(body):
    async for chunk in body:
        yield hex(len(chunk))[2:] + b'\r\n'
        yield chunk
        yield b'\r\n'
    yield b'0\r\n\r\n'
