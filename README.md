# lowhaio-chunked

Chunked transfer request encoding for [lowhaio](https://github.com/michalc/lowhaio). This is only needed if `content-length` is unknown before the body starts to transfer.


## Usage

Usage is very similar to the standard lowhaio, except that the `body` data should be wrapped with `chunked`, and the `transfer-encoding: chunked` header is required, without `content-length`.

Note that there are only 6 lines of code required, so suggested usage is to simply copy and paste the below code into your project (ensuring to follow the LICENSE fine).

```python
async def chunked(body):
    async for chunk in body:
        yield hex(len(chunk))[2:].encode() + b'\r\n'
        yield chunk
        yield b'\r\n'
    yield b'0\r\n\r\n'
```

So instead of a request like

```python
code, headers, body = await request(
    b'POST', 'https://example.com/path', body=file_data(),
    headers=((b'content-length', b'1234'),),
)
```

you can write

```python
async def chunked(body):
    async for chunk in body:
        yield hex(len(chunk))[2:].encode() + b'\r\n'
        yield chunk
        yield b'\r\n'
    yield b'0\r\n\r\n'

code, headers, body = await request(
    b'POST', 'https://example.com/path', body=chunked(file_data()),
    headers=((b'transfer-encoding': b'chunked'),),
)
```
