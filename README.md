# lowhaio-chunked [![CircleCI](https://circleci.com/gh/michalc/lowhaio-chunked.svg?style=svg)](https://circleci.com/gh/michalc/lowhaio-chunked)

Chunked transfer request encoding for [lowhaio](https://github.com/michalc/lowhaio). This is only needed if `content-length` is unknown before the body starts to transfer.


## Installation

```bash
pip install lowhaio lowhaio_chunked
```

or just copy and paste the below 6 lines of code into your project, ensuring to also follow the requirements in the LICENSE file.

```python
async def chunked(body):
    async for chunk in body:
        yield hex(len(chunk))[2:].encode() + b'\r\n'
        yield chunk
        yield b'\r\n'
    yield b'0\r\n\r\n'
```


## Usage

Usage is very similar to standard lowhaio, except that the `body` data should be wrapped with the `chunked` function; the `transfer-encoding: chunked` header is required; and the `content-length` header should _not_ be specified.

So instead of a request like

```python
from lowhaio import Pool

request, _ = Pool()

body = ...

code, headers, body = await request(
    b'POST', 'https://example.com/path', body=body(),
    headers=((b'content-length', b'1234'),),
)
```

you can write

```python
from lowhaio import Pool
from lowhaio_chunked import chunked  # Or paste in the code above

request, _ = Pool()

body = ...

code, headers, body = await request(
    b'POST', 'https://example.com/path', body=chunked(body()),
    headers=((b'transfer-encoding': b'chunked'),),
)
```
