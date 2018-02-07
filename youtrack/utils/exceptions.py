from .xml_parser import parse_xml
import asyncio

loop = asyncio.get_event_loop()


def run(func, *args, **kwargs):
    return loop.run_until_complete(func(*args, **kwargs))


class YouTrackException(Exception):
    def __init__(self, response, comment):
        self.response = response
        super().__init__(comment)


class NotFound(YouTrackException):
    pass
