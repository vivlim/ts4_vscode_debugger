import queue

_func_queue = None

instance = None

def check_on_main_thread():
    import threading
    mt = threading.main_thread()
    thist = threading.current_thread()
    return mt == thist
        
def throw_if_not_main_thread():
    import threading
    mt = threading.main_thread()
    thist = threading.current_thread()
    if mt != thist:
        raise Exception(f'Current thread {thist} is not main thread {mt}')

class MainThreadDispatcher:
    def __init__(self):
        global _func_queue
        if _func_queue == None:
            throw_if_not_main_thread()
            _func_queue = queue.Queue(64)

        self._func_queue = _func_queue
    
    def run_on_main_thread(self, func):
        if check_on_main_thread():
            func()
        else:
            self._func_queue.put(func)
    
    def _on_tick(self):
        # This count is unreliable (a func could be pushed while we are getting it) but this runs frequently so it's fine if we miss a tick
        if self._func_queue.qsize() == 0:
            return
        
        func = None
        try:
            func = self._func_queue.get(block=False)
        except:
            return
        
        func()
    
    def wrap_on_tick(self, target_void_func):
        def on_tick_wrapper():
            target_void_func()
            self._on_tick()
        
        return on_tick_wrapper
