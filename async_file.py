import asyncio


class AsyncFile:
    def __init__(self, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        self._loop = loop
        self._file = None

    async def open(self, file, mode='r'):
        f = await self._loop.run_in_executor(None, open, *(file, mode))
        self._file = f
        return self

    async def read(self):
        content = await self._loop.run_in_executor(None, self._file.read)
        return content

    async def write(self, content):
        await self._loop.run_in_executor(None, self._file.write, content)

    async def close(self):
        await self._loop.run_in_executor(None, self._file.close)


class AsyncFileContextManager:
    def __init__(self, coro):
        self._coro = coro
        self._obj = None

    async def __aenter__(self):
        self._obj = await self._coro
        return self._obj

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._obj.close()


async def _open(file, mode='r'):
    async_file = AsyncFile()
    return await async_file.open(file, mode)


def aopen(file, mode='r'):
    return AsyncFileContextManager(_open(file, mode))
