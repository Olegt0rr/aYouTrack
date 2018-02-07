from .base import YouTrackObject


class Issue(YouTrackObject):
    id = None
    jiraId = None
    projectShortName = None
    numberInProject = None
    summary = None
    description = None
    created = None
    updated = None
    updaterName = None
    resolved = None
    reporterName = None
    voterName = None
    commentsCount = None
    votes = None
    permittedGroup = None
    comment = None
    tag = None

    def __init__(self, root, yt):
        from youtrack import YouTrackAPI

        self._yt: YouTrackAPI = yt
        for name, value in root.attrib.items():
            self.__setattr__(name, value)

        for element in root:
            if element.tag == 'field':
                name = element.get('name')
                value = element.find('value').text
                self.__setattr__(name, value)

    def __repr__(self):
        return f'YT Issue {self.id}'

    async def update(self, summary=None, description=None, **kwargs):
        # todo issue.update(fields={"labels": issue.fields.labels})
        return await self._yt.update_issue(self, issue_id=self.id, summary=summary, description=description, **kwargs)

    async def delete(self):
        return await self._yt.delete_issue(self.id)

    async def get_history(self):
        return await self._yt.get_issue_history(self.id)


class IssueList(list):
    def __init__(self, root):
        super().__init__()

        for element in root:
            self.append(Issue(element))

    def __repr__(self):
        text = f'Issues: '
        for issue in self:
            text += f'{issue} '
        return text
