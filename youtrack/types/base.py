import asyncio

loop = asyncio.get_event_loop()


class YouTrackObject:

    def __repr__(self):
        _repr = ''
        for k, v in self.__dict__.items():
            _repr += f'{k} = {v} \n'
        return _repr

    def __iter__(self):
        for item in self.__dict__:
            if item == '_attribute_types':
                continue
            attr = self.__dict__[item]
            if isinstance(attr, str) or isinstance(attr, list) \
                    or getattr(attr, '__iter__', False):
                yield item

    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value


class Field:
    type = None
    name = None
    value = None

    def __init__(self, field_type=None, name=None, value=None):
        self.type = field_type or ''
        self.name = name or ''
        self.value = value or ''

    def __repr__(self):
        return f'{self.name} ({self.type}) = {self.value}'
