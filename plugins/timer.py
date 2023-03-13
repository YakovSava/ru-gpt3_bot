import hashlib
import asyncio

from typing import Any, Coroutine, Callable


class TimerError(Exception): pass

class Timer:

	def __init__(self,
				loop: asyncio.AbstractEventLoop=asyncio.get_event_loop(),
				executor: Any=None
				):
		self._loop = loop
		self.executor = executor
		self._tasks = []

	def _new_task(self, task: Coroutine) -> None:
		self._tasks.append(self._loop.create_task(task))

	def _shedule(self,
				task: Coroutine=None,
				every: int=60
				) -> None:
		self._tasks.append(
			self._loop.create_task(
				self._every_sheduler(
					task=task,
					every=every
				)
			)
		)

	def _repeats_shedule(self,
						task: Coroutine=None,
						every: int=60,
						repeats: int=10
						) -> None:
		self._tasks.append(
			self._loop.create_task(
				self._every_while_sheduler(
					task=task,
					every=every,
					repeats=repeats
				)
			)
		)

	def _sync_sheduler(self,
						function: Callable=None,
						every: int=60
						) -> None:
		self._tasks.append(
			self._loop.create_task(
				self._every_sheduler(
					task=self._loop.run_in_executor(self.executor, function),
					every=every
				)
			)
		)

	async def _every_sheduler(self,
							task: Coroutine=None,
							every: int=60
							) -> None:
		while True:
			await task
			await asyncio.sleep(every)

	async def _every_while_sheduler(self,
									task: Coroutine=None,
									every: int=60,
									repeats: int=10
									) -> None:
		for _ in range(repeats):
			await task
			await asyncio.sleep(every)

	def create_task(self, task: Coroutine) -> None:
		self._tasks.append(
			self._loop.create_task(task)
		)

	def shedule_task(self, 
					task: Coroutine=None,
					every: int=None,
					repeats: int=None
				) -> None:
		if not task:
			raise TimerError('No tasks in arguments')
		if every and repeats:
			self._new_task(task=task)
		elif not repeats and not every:
			self._every_while_sheduler(
				task=task,
				every=every,
				repeats=repeats
			)
		elif not every:
			self._every_sheduler(
				task=task,
				every=every
			)

	async def start_tasks(self):
		await asyncio.gather(*self._tasks)

	async def clear_tasks(self) -> None:
		del self._tasks
		del self._tasks

	def __iadd__(self, other: Coroutine):
		self.create_task(other)

	def __add__(self, other: Coroutine):
		self.create_task(other)
		return 0

	def __str__(self):
		return f'<timer object has {len(self._tasks)} tasks>'

	def __len__(self):
		return len(self._tasks)

	def __del__(self):
		self._loop.run_until_complete(self.clear_tasks())
		self._loop.close()

	def __hash__(self):
		return hashlib.sha256(bytes(str(len(self._tasks)))).hexdigest()

	def __await__(self, *args):
		return self.start_tasks

	def sync_task(self, every:int=60) -> Callable:
		def wrapper(self, task:Callable):
			self._sync_sheduler(task=task, every=every)

			return task
		return wrapper