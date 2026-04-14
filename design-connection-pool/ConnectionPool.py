from queue import Queue, Empty

class Connection:
    """Dummy connection object"""
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"<Connection {self.id}>"

class ConnectionPool:
    def __init__(self, max_size):
        self.max_size = max_size
        self.pool = Queue(maxsize=max_size)
        self._initialize_pool()

    def _initialize_pool(self):
        for i in range(self.max_size):
            conn = Connection(i)
            self.pool.put(conn)

    def acquire(self, timeout=None):
        """
        Get a connection from the pool.
        Blocks if none available.
        """
        try:
            conn = self.pool.get(block=True, timeout=timeout)
            print(f"Acquired {conn}")
            return conn
        except Empty:
            raise Exception("Timeout: No available connections")

    def release(self, conn):
        """
        Return connection back to pool.
        """
        if conn:
            self.pool.put(conn)
            print(f"Released {conn}")