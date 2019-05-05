# lowhaio-chunked

Chunked transfer request encoding for lowhaio

> Work in progress. These docs serve as a rough design spec.


## Usage

Usage is very similar to the standard lowhaoi, except that the `request` function should be wrapped with `chunked`, and no `content-length` header is required.

```python

from lowhaio import Pool
from lowhaio_chunked import chunked

request, _ = Pool()
chunked_request = chunked(request)

path = 'my.file'
content_length = str(os.stat(path).st_size).encode()
async def file_data():
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(16384), b''):
            yield chunk

code, headers, body = await chunked_request(
    b'POST', 'https://example.com/path', body=file_data(),
)
```
