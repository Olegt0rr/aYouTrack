import functools
import asyncio
from .exceptions import YouTrackException


def relogin_on_401(func):
    @functools.wraps(func)
    async def wrapped(self, *args, **kwargs):
        attempts = 10
        while attempts:

            try:
                attempts -= 1
                return await func(self, *args, **kwargs)

            except YouTrackException as e:
                if e.response.status not in (401, 403, 500, 504):
                    raise e

                if e.response.status == 504:
                    await asyncio.sleep(30)

                elif self._last_credentials is not None:
                    await self._login(*self._last_credentials)

                else:
                    break
        return await func(self, *args, **kwargs)

    return wrapped
