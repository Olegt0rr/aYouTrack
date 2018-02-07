import aiohttp
import asyncio
import json
import logging
from urllib.parse import quote, urlencode
from youtrack.utils.static import Methods
from youtrack.utils import parse_xml, relogin_on_401, get_object
from youtrack.utils.exceptions import YouTrackException, NotFound
from youtrack.types import Issue, IssueList

logger = logging.getLogger('YouTrack')


class YouTrackAPI:

    def __init__(self, url, login, password):
        self.url = url.rstrip('/')
        self.base_url = self.url + "/rest"
        self.headers = {}
        self._last_credentials = (login, password)

        # Asyncio loop instance
        self.loop = asyncio.get_event_loop()

        # aiohttp main session
        self.session = aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10),
            loop=self.loop, json_serialize=json.dumps)

    def __del__(self):
        self.session.close()

    async def login(self):
        await self._login(*self._last_credentials)

    async def _login(self, login, password):
        url = self.base_url + '/user/login'
        data = {'login': quote(login), 'password': quote(password)}
        payload = urlencode(data)
        headers = {'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Content-Length': str(len(payload))}

        response: aiohttp.ClientResponse = await self.session.post(url=url, data=payload, headers=headers)

        if response.status != 200:
            raise YouTrackException(response, 'Login fails')

        resp_dict = await parse_xml(await response.text())
        self.headers = {'Cookie': resp_dict.get('set-cookie'),
                        'Cache-Control': 'no-cache'}
        self._last_credentials = (login, password)

    @relogin_on_401
    async def _request(self, method, api_url, data=None):
        url = self.base_url + api_url
        data = await self._compose_data(data)

        async with self.session.request(method, url, data=data) as response:

            if response.status == 404:
                raise NotFound(response, "Can't find")

            xml_body = await response.text()
            logger.debug(f'Response: {response}')
            return response, xml_body

    async def create_issue(self, project, summary, description=None, attachments=None, permitted_group=None,
                           output='link'):
        """
        Create an issue
         # todo attachments file in the "multipart/form-data" format
         # todo ability to get another params (assignee, type, status etc)

        :param output: 'link' or 'id' or 'issue'
        :param project: ID of a project to add new issue to.
        :param summary: Short summary for the new issue.
        :param description: Optional. Description for the new issue.
        :param attachments: Optional. One or several files in the "multipart/form-data" format that should be attached
                            to the new issue.
        :param permitted_group: Optional. Specify a user group to which the issue will be visible.
        :return: issue link or issue id or Issue object
        """
        method = Methods.PUT
        url = '/issue'
        data = {
            'project': project,
            'summary': summary,
            'description': description,
            'attachments': attachments,
            'permitted_group': permitted_group,
        }
        response, body = await self._request(method=method, api_url=url, data=data)

        if response and response.status == 201:
            link = response.headers.get('location')
            issue_id = list(link.split(sep='/')).pop()

            if output == 'link':
                return link

            elif output == 'id':
                return issue_id

            elif output == 'issue':
                return await self.get_issue(issue_id)

    async def get_issue(self, issue_id, wikify_description=False):
        """
        Get an Issue

        :param issue_id: ID of an issue to get.
        :param wikify_description: true if issue description in the response should be formatted ("wikified")
        :return: Issue object
        """
        method = Methods.GET
        url = f'/issue/{issue_id}'
        data = {
            'wikifyDescription': wikify_description,
        }
        response, body = await self._request(method=method, api_url=url, data=data)

        if response and response.status == 200:
            issue: Issue = await get_object(body)
            return issue

    async def update_issue(self, issue_id, summary=None, description=None, **kwargs):
        """
        Update an Issue

        :param issue_id:
        :param summary:
        :param description:
        :param kwargs:
        :return:
        """
        # todo         # todo issue.update(fields={"labels": issue.fields.labels})

        method = Methods.POST
        url = f'/issue/{issue_id}'
        data = {
            'summary': summary,
            'description': description,
        }
        response, body = await self._request(method=method, api_url=url, data=data)

        if response and response.status == 200:
            return True
        else:
            return False

    async def check_issue_exists(self, issue_id):
        method = Methods.GET
        url = f'/issue/{issue_id}/exists'
        data = {}
        response, body = await self._request(method=method, api_url=url, data=data)

        if response and response.status == 200:
            return True
        else:
            return False

    async def get_issue_history(self, issue_id):
        """
        Get Issue history
        Returns sorted list of all Issue states

        :param issue_id: ID of an issue
        :return: IssueList object
        """
        method = Methods.GET
        url = f'/issue/{issue_id}/history'
        data = {}
        response, body = await self._request(method=method, api_url=url, data=data)

        if response and response.status == 200:
            issues_list: IssueList = await get_object(body)
            return issues_list

    async def delete_issue(self, issue_id):
        """
        Delete Issue

        :param issue_id: ID of an issue
        :return: boolean
        """
        method = Methods.DELETE
        url = f'/issue/{issue_id}'
        data = {}
        response, body = await self._request(method=method, api_url=url, data=data)

        if response and response.status == 200:
            return True

    @staticmethod
    async def _compose_data(params=None, files=None):
        """
        Prepare request data

        :param params:
        :param files:
        :return:
        """
        data = aiohttp.formdata.FormData(quote_fields=False)

        if params:
            for key, value in params.items():
                if value is not None:
                    data.add_field(key, str(value))

        # if files:
        #     for key, f in files.items():
        #         if isinstance(f, tuple):
        #             if len(f) == 2:
        #                 filename, fileobj = f
        #             else:
        #                 raise ValueError('Tuple must have exactly 2 elements: filename, fileobj')
        #         elif isinstance(f, types.InputFile):
        #             filename, fileobj = f.filename, f.file
        #         else:
        #             filename, fileobj = _guess_filename(f) or key, f
        #
        #         data.add_field(key, fileobj, filename=filename)

        return data
