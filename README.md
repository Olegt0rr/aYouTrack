# aYouTrack 
[![Supported python versions](https://img.shields.io/pypi/pyversions/aiogram.svg?style=flat-square)](https://pypi.python.org/pypi/aiogram)
[![MIT License](https://img.shields.io/pypi/l/aiogram.svg?style=flat-square)](https://opensource.org/licenses/MIT)

**aYouTrack** is a library for [YouTrack REST API](https://www.jetbrains.com/help/youtrack/standalone/YouTrack-REST-API-Reference.html) written in Python 3.6 with [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://github.com/aio-libs/aiohttp). 
It helps to integrate YouTrack with your product.

## How to use
1) Import YouTrack
```python
from youtrack import YouTrackAPI
```

2) Create yt instance
```python
yt = YouTrackAPI(url=YT_SITE_URL, login=YT_LOGIN, password=YT_PASSWORD)
```

3) Create issue and get new issue id or issue link or issue object
```python
issue = await yt.create_issue(project='MyProject', summary='My Issue', output='issue')
```

4) Update issue 
```python
await issue.update(summary="My Issue 2", description='Added description')
```

5) Delete issue
```python
await issue.delete()
```

6) Get another issue by id
```python
another_issue = await yt.get_issue('YT-123')
```

7) Execute issue commands (for example set custom field)
```python
value = 'some value'
await another_issue.execute(f'field {value}')
```

## To do
* Token authorization
* Set default project
* Project related methods
* User related methods
