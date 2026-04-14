# ⚡ Blocking Queue Implementation in Python (asyncio)

## 📌 Problem Statement

Design and implement a **bounded blocking queue** in Python that:

- Supports concurrent producers and consumers
- Blocks producers when the queue is full
- Blocks consumers when the queue is empty
- Avoids thread-based blocking
- Works efficiently within an event-driven system

---

## 🧠 Conceptual Knowledge

### 🔹 What is a Blocking Queue?

A **blocking queue** is a thread-safe (or coroutine-safe) data structure where:

- Producers **wait** if the queue is full
- Consumers **wait** if the queue is empty

---

### 🔹 Threading (Traditional Approach)

In a multi-threaded system:

- Uses OS-level threads
- Synchronization via:
  - `Lock`
  - `Condition`
  - `Semaphore`
- Threads are **blocked** when waiting

#### Pros:
- True parallelism (for CPU-bound tasks with multiprocessing)
- Simple mental model

#### Cons:
- Context switching overhead
- Higher memory usage
- Risk of deadlocks and race conditions
- Limited scalability

---

### 🔹 Asyncio (Modern Approach)

`asyncio` is Python’s **asynchronous programming framework**:

- Uses a **single-threaded event loop**
- Tasks are scheduled cooperatively
- Uses `async/await` for non-blocking execution

#### Key Components:
- `async def` → coroutine definition  
- `await` → suspend execution  
- `asyncio.Lock` → async mutual exclusion  
- `asyncio.Condition` → async coordination  

---

### ⚖️ Threading vs Asyncio

| Feature            | Threading                  | Asyncio                     |
|-------------------|---------------------------|-----------------------------|
| Concurrency Model | Preemptive (OS managed)   | Cooperative (event loop)    |
| Blocking          | Blocks thread             | Non-blocking (`await`)      |
| Overhead          | High                      | Low                         |
| Scalability       | Limited                   | High                        |
| Best For          | CPU-bound tasks           | I/O-bound tasks             |

---

## 🚀 Advantages of Asyncio Over Threading

- ⚡ **Non-blocking execution** → better CPU utilization  
- 📉 **Lower memory overhead** → no multiple threads  
- 🔄 **Efficient context switching** → handled by event loop  
- 📈 **Highly scalable** → thousands of concurrent tasks  
- 🧘 **Avoids thread-related bugs** → fewer race conditions  
- 🌐 Ideal for:
  - APIs
  - Web servers
  - Streaming systems
  - Message queues

---

## 🏗️ Approach Chosen

### Core Idea

Use:
- `asyncio.Lock` → ensure mutual exclusion  
- `asyncio.Condition` → coordinate producers and consumers  
- `collections.deque` → efficient queue operations  

---

### Design Overview

1. **Initialization**
   - Create bounded queue with fixed capacity
   - Initialize async conditions

2. **Enqueue**
   - Wait if queue is full
   - Add item
   - Notify waiting consumers

3. **Dequeue**
   - Wait if queue is empty
   - Remove item
   - Notify waiting producers

---

## ⚙️ Implementation Details

### Core Data Structure

```python
from collections import deque
self.queue = deque()
```
- O(1) append and pop operations
- Better than list for queue behavior

#### AsyncBlockingQueue Class
```
import asyncio
from collections import deque

class AsyncBlockingQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = deque()
        self.lock = asyncio.Lock()
        self.not_full = asyncio.Condition(self.lock)
        self.not_empty = asyncio.Condition(self.lock)
```

#### Enqueue Operation
```
async def enqueue(self, item):
    async with self.not_full:
        while len(self.queue) == self.capacity:
            await self.not_full.wait()

        self.queue.append(item)
        self.not_empty.notify()
```
- Waits when queue is full
- Notifies consumers after adding

#### Dequeue Operation
```
async def dequeue(self):
    async with self.not_empty:
        while len(self.queue) == 0:
            await self.not_empty.wait()

        item = self.queue.popleft()
        self.not_full.notify()
        return item
```
- Waits when queue is empty
- Notifies producers after removal

#### Execution Flow
```
ENQUEUE → (WAIT if FULL) → ADD → NOTIFY CONSUMER
DEQUEUE → (WAIT if EMPTY) → REMOVE → NOTIFY PRODUCER
```

### 🧵 Key Design Decisions
#### 1. asyncio.Condition
- Enables coroutine coordination
- Avoids blocking threads
#### 2. while instead of if
``` while len(self.queue) == 0: ```
- Handles spurious wakeups
- Ensures correctness in concurrent scenarios
#### 3. async with
- Guarantees lock safety
- Required for condition variables