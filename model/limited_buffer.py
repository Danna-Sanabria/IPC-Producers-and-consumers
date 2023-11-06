import threading


class LimitedBuffer:
    def __init__(self, size):
        self.size = size
        self.buffer = []
        self.mutex = threading.Semaphore(1)
        self.empty_slots = threading.Semaphore(size)
        self.full_slots = threading.Semaphore(0)
        self.event_log = []

    def add(self, item):
        self.empty_slots.acquire()
        self.mutex.acquire()
        self.buffer.append(item)
        event = f"Produced {item}. Buffer: {self.buffer}"
        self.event_log.append(event)
        self.mutex.release()
        self.full_slots.release()

    def remove(self):
        self.full_slots.acquire()
        self.mutex.acquire()
        item = self.buffer.pop(0)
        event = f"Consumed {item}. Buffer: {self.buffer}"
        self.event_log.append(event)
        self.mutex.release()
        self.empty_slots.release()
        return item
