from BlockingQueue import BlockingQueue
import threading
import time

def producer(queue: BlockingQueue, items: list):
    for item in items:
        print(f"Producing {item}")
        queue.enqueue(item)
        time.sleep(1)

def consumer(queue: BlockingQueue, count: int):
    for _ in range(count):
        item = queue.dequeue()
        print(f"Consumed {item}")
        time.sleep(2)

if __name__ == "__main__":
    bq = BlockingQueue(capacity=2)

    t1 = threading.Thread(target=producer, args=(bq, [1, 2, 3, 4]))
    t2 = threading.Thread(target=consumer, args=(bq, 4))

    t1.start()
    t2.start()

    t1.join()
    t2.join()