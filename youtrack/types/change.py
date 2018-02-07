
class Link:
    def __init__(self, text, url):
        self.text = text
        self.url = url


class Field:
    def __init__(self, field):
        self.values = []
        for value in field:
            url = value.get('url')
            text = value.text

            if url and text:
                self.values.append(Link(text, url))

            elif text:
                self.values.append(text)

        if len(self.values) == 1:
            self.values = self.values[0]


class Change:
    def __init__(self, change, yt):
        self._yt = yt
        for field in change:
            name = field.get('name')
            self.__setattr__(name, Field(field))

    def __repr__(self):
        text = 'Change: \n'
        for k, v in self.__dict__.items():
            text += f'{k}: {v[0]} --> {v[1]}'


class ChangeList(list):
    def __init__(self, changes, yt):
        super().__init__()

        for change in changes:
            self.append(Change(change, yt))

    def __repr__(self):
        text = f'Changes: '
        for change in self:
            text += f'{change} '
        return text
