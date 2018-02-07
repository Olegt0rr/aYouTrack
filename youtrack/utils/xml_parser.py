from collections import defaultdict
from xml.etree import cElementTree


async def parse_xml(xml_data) -> dict:
    """
    Parses data from string xml to Element Tree
    Then convert data to dict and return

    :param xml_data:
    :return:
    """
    element_tree = cElementTree.XML(xml_data)
    xml_dict = etree_to_dict(element_tree)
    return xml_dict


async def xml_to_etree(xml_data):
    tree = cElementTree.fromstring(xml_data)
    return tree.get_root()


def etree_to_dict(t):
    """
    Parses entities as well as attributes following this XML-to-JSON "specification"

    from xml.etree import cElementTree as ET
        e = ET.XML(xml_data)
        d = etree_to_dict(e)

    :param t:
    :return:
    """
    d = {t.tag: {} if t.attrib else None}
    children = list(t)

    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v
                     for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v)
                        for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d
