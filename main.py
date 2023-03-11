import asyncio

from sys import platform
from vkbottle.user import User, Message
from vkbottle import VKAPIError, ABCRule
from config import vk_token

vk = User(token=vk_token)


class GenerateRuleIn(ABCRule[Message]):
	async def check(self, message:Message):
		return 'генерировать' in message.text.lower()

@vk.on.private_message(GenerateRule())
async def generate_message(message:Message):
	await message.answer('Не поддерживается!')

async def polling(loop:asyncio.AbstractEventLoop=asyncio.get_event_loop()):
	await vk.run_polling(loop=loop)

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(
		asyncio.wait([
			loop.create_task(polling())
		])
	)