import logging

# decorator for lazy globals, shared with vivlib
def lazy_global(func):
    key = f"_vivlib_lazy_global_{func.__name__}"
    def _lazy_get_or_init():
        if not key in globals():
            globals()[key] = func()
        return globals()[key]
    return _lazy_get_or_init


def log_exception(func):
    def _do_log(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            try:
                import traceback
                tb = traceback.format_exc()
                get_logger().error(tb) # there is probably a more idiomatic way to log this, looking at the other parameters available
            except: pass
    return _do_log

def log_exception_and_raise(func):
    def _do_log(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            try:
                import traceback
                tb = traceback.format_exc()
                get_logger().error(tb) # there is probably a more idiomatic way to log this, looking at the other parameters available
            except: 
                try:
                    get_logger().error("error when logging exception...")
                except:
                    pass
            finally:
                raise e

    return _do_log


class CallbackLogHandler(logging.Handler):
    def __init__(self, queue, level=logging.NOTSET):
        super().__init__(level)
        self._callbacks = []
        self.level = level

    def emit(self, record):
        for callback in self._callbacks:
            if record.levelno >= self.level:
                try:
                    callback(record.getMessage())
                except:
                    pass

class HollowLogger(logging.Logger):
    def __init__(self, *args,):
        super().__init__(*args)
        self._cb_handler = CallbackLogHandler(None, level=logging.NOTSET)
        self.addHandler(self._cb_handler)
    def add_callback(self, callback):
        self._cb_handler._callbacks.append(callback)
    
@lazy_global
def hollow_logger():
    return HollowLogger("vivlib2")

def get_logger() -> logging.Logger:
    try:
        import vivlib
        return vivlib.get_logger()
    except:
        return hollow_logger()