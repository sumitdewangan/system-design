import threading

class BlockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = []
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def enqueue(self, item, timeout=2):
        with self.not_full:
            while len(self.queue) == self.capacity:
                self.not_full.wait(timeout=timeout)  # wait until space is available

            self.queue.append(item)

            # Notify one waiting consumer
            self.not_empty.notify()

    def dequeue(self, timeout=2):
        with self.not_empty:
            while len(self.queue) == 0:
                self.not_empty.wait(timeout=timeout)  # wait until item is available

            item = self.queue.pop(0)

            # Notify one waiting producer
            self.not_full.notify()

            return item