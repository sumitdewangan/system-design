import asyncio
from collections import deque

class BlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = deque()
        self.lock = asyncio.Lock()
        self.not_full = asyncio.Condition(self.lock)
        self.not_empty = asyncio.Condition(self.lock)

    async def enqueue(self, item, timeout=2):
        async with self.not_full:
            while len(self.queue) == self.capacity:
                await asyncio.wait_for(self.not_empty.wait(), timeout=timeout) # wait until space available

            self.queue.append(item)

            # Notify one waiting consumer
            self.not_empty.notify()

    async def dequeue(self, timeout=2):
        async with self.not_empty:
            while len(self.queue) == 0:
                await asyncio.wait_for(self.not_empty.wait(), timeout=timeout) # wait until item available

            item = self.queue.popleft()

            # Notify one waiting producer
            self.not_full.notify()

            return item