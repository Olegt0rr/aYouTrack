from xml.etree import cElementTree
from youtrack.types import types, Field, YouTrackObject
import logging

logger = logging.getLogger(f'Youtrack.{__name__}')


async def get_object(xml_data: str, yt):
    """
    Factory steps:
        1) Get xml data
        2) Parse it to ElementTree
        3) Get YouTrack class by root.tag
        4) Set attributes to yt object
        5) Return object

    :param yt: api object
    :param xml_data:
    :return:
    """
    root = cElementTree.fromstring(xml_data)
    type_class = types.get(root.tag)
    if type_class:
        return type_class(root, yt)

    else:
        return None
