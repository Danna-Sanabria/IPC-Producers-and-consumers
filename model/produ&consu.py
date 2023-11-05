import threading
import time
import random

class LimitedBuffer:
    """
    Class representing a limited buffer shared between producers and consumers.
    """
    def __init__(self, size):
        """
        Constructor of the class.
        
        Args:
            size (int): Maximum size of the buffer.
        """
        self.size = size
        self.buffer = []
        self.mutex = threading.Semaphore(1)  # Semaphore for mutual exclusion to the buffer.
        self.empty_slots = threading.Semaphore(size)  # Semaphore counting empty slots in the buffer.
        self.full_slots = threading.Semaphore(0)  # Semaphore counting occupied slots in the buffer.

    def add(self, item):
        """
        Add an item to the buffer.
        
        Args:
            item: Item to be added to the buffer.
        """
        self.empty_slots.acquire()
        self.mutex.acquire()
        self.buffer.append(item)
        print(f"Produced {item}. Buffer: {self.buffer}")
        self.mutex.release()
        self.full_slots.release()

    def remove(self):
        """
        Remove and return an item from the buffer.
        
        Returns:
            The item removed from the buffer.
        """
        self.full_slots.acquire()
        self.mutex.acquire()
        item = self.buffer.pop(0)
        print(f"Consumed {item}. Buffer: {self.buffer}")
        self.mutex.release()
        self.empty_slots.release()
        return item

def producer(buffer):
    """
    Producer function. Produces items and adds them to the buffer.
    
    Args:
        buffer (LimitedBuffer): The shared buffer.
    """
    while True:
        item = random.randint(1, 100)
        buffer.add(item)
        time.sleep(random.random())

def consumer(buffer):
    """
    Consumer function. Consumes items from the buffer.
    
    Args:
        buffer (LimitedBuffer): The shared buffer.
    """
    while True:
        buffer.remove()
        time.sleep(random.random())

if __name__ == "__main__":
    buffer_size = int(input("Enter the buffer size: "))
    num_producers = int(input("Enter the number of producers: "))
    num_consumers = int(input("Enter the number of consumers: "))

    buffer = LimitedBuffer(buffer_size)

    for _ in range(num_producers):
        threading.Thread(target=producer, args=(buffer,)).start()

    for _ in range(num_consumers):
        threading.Thread(target=consumer, args=(buffer,)).start()
