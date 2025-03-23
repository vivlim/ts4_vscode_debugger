import vivlib2
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

@vivlib2.lazy_global
def _func_queue():
    import queue
    return queue.Queue(64)

class MainThreadDispatcher:
    def __init__(self):
        self._func_queue = _func_queue()
    
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


@vivlib2.lazy_global
def _wrap_on_tick():
    throw_if_not_main_thread()
    import pathlib,sys
    if pathlib.Path(sys.executable).name.casefold() == "TS4_x64.exe".casefold():
        dispatcher = MainThreadDispatcher()
        import sims4.core_services
        sims4.core_services.on_tick = dispatcher.wrap_on_tick(sims4.core_services.on_tick)

_wrap_on_tick()