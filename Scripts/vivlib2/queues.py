class BroadcastQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self._output_queues = []
    def subscribe(self):
        import queue
        q = queue.Queue(self.capacity)
        self._output_queues.append(q)
        return q
    
    def put(self, item):
        for q in self._output_queues:
            try:
                q.put(item, block=False)
                q.put_
            except:
                pass

import queue
def service_queue_on_thread(q: queue.Queue, func):
    import threading
    def _thread_exec():
        while True:
            try:
                item = q.get(block=True)
                func(item)
            except Exception as e:
                pass
    t =threading.Thread(target=_thread_exec, args=())
    t.daemon = True
    t.start()
    return t