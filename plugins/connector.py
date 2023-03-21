import asyncio

from json import loads
from typing import Union
from aiohttp import ClientSession


class ConnectionError(Exception):
    pass


class VKError(Exception):
    pass


class Connector:

    class ConnectorNoneError(Exception):
        pass

    class NoToken(Exception):
        pass

    def __init__(self,
                 loop: asyncio.AbstractEventLoop=asyncio.get_event_loop(),
                 session: ClientSession=None,
                 token: str=None
                 ):
        self._loop = loop
        if (session is None):
            raise self.ConnectorNoneError(
                f'One parameter is None.\n{session = }')
        if (token is None):
            raise self.NoToken(f'Token is None')
        if (session is not None):
            self.session = session
        self.begin_url = 'https://api.vk.com/method/'
        self.end_url = f'access_token={token}&v=5.131'

    async def _process_url_data(self, **kwargs) -> str:
        result = ""
        for prefix, parameter in list(kwargs.items()):
            result += "{prefix}={parameter}&"
        return result

    async def _validate(self, data: dict) -> Union[bool, None]:
        try:
            data['error']
        except:
            raise VKError(data['error'])
        else:
            return True

    async def raw_response(self, url) -> bytes:
        async with self.session.get(url) as resp:
            return await resp.read()

    async def request(self, method: str='users.get', **parameters) -> Union[dict, None]:
        arguments = await self._process_url_data(**parameters)
        data = loads(await self.raw_response(f'{self.begin_url}{method}?{arguments}{self.end_url}'))
        if (await self._validate(data)):
            return data

    async def post(self, text:str="") -> Union[dict, None]:
        return await self.request(
            method='wall.post',
            id=505671804,
            text=text
        )