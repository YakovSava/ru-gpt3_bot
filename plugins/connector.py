import asyncio 

from aiohttp import ClientSession
from vkbottle import API


class Connector:

	class ConnectorNoneError(Exception): pass

	def __init__(self, loop:asyncio.AbstractEventLoop=asyncio.get_event_loop(), api:API=None, session:ClientSession=None):
		self._loop = loop
		if (api is None) or (session is None):
			raise self.ConnectorNoneError(f'One parameter is None.\n{api = }\n{session = }')
		self._api_check = False
		self._session_check = False
		if (api is not None):
			self._api_check = True
			self.api = api
		else:
			self._session_check = True
			self._loop.run_until_complete(self._preset(session))

	async def _preset(self, session:ClientSession) -> None:
		self.session = session