## icodeapi, the The second generation of IcodeYoudao API framework.

**More powerful and Faster than [TuringAPI](https://xbz-studio.gitbook.io/turingapi) and TuringIO.**

icodeapi is easy to use, and it supports for sync and async.

```python
from icodeapi import *
import asyncio
cookie = input('Enter cookie: ')
syncAPI = IcodeAPI(cookie = cookie)
print(syncAPI.updateIntro('hello, icodeapi!'))
asyncAPI = AsyncIcodeAPI(cookie = cookie)

async def main(api : AsyncIcodeAPI):
    await api.login()
    print(await api.updateIntro('hello, async icodeapi!'))
    await api.closeClient()

asyncio.run(main(asyncAPI))
```

### Use pip to install:

```PowerShell
pip install icodeapi
```

### [Documentation](https://xbz-studio.gitbook.io/icodeapi)

### [Github](https://github.com/xbzstudio/icodeapi)
