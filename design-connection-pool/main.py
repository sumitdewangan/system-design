from ConnectionPool import ConnectionPool
import threading
import time

def worker(pool: ConnectionPool, worker_id):
    try:
        conn = pool.acquire(timeout=2)
        print(f"Worker {worker_id} using {conn}")
        time.sleep(1)
        pool.release(conn)
    except Exception as e:
        print(f"Worker {worker_id}: {e}")


if __name__ == "__main__":
    pool = ConnectionPool(max_size=2)

    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(pool, i))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()