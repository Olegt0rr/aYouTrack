import warnings

try:
    from .api import YouTrackAPI

except ImportError as e:
    if 'aiohttp' in str(e):
        warnings.warn('Dependencies are not installed!',
                      category=ImportWarning)
    else:
        raise

# try:
#     import uvloop
#
# except ImportError:
#     pass
#
# else:
#     import asyncio
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
