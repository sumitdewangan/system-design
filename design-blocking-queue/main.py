import asyncio
from AsyncBlockingQueue import BlockingQueue

async def producer(queue: BlockingQueue):
    for i in range(5):
        print(f"Producing {i}")
        await queue.enqueue(i)
        await asyncio.sleep(1)

async def consumer(queue: BlockingQueue):
    for _ in range(5):
        item = await queue.dequeue()
        print(f"Consumed {item}")
        await asyncio.sleep(2)

async def main():
    queue = BlockingQueue(capacity=2)

    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )

if __name__ == "__main__":
    asyncio.run(main())