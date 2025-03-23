import vivlib2
import vivlib2.main_thread
actions = {}

def _get_client():
    vivlib2.main_thread.throw_if_not_main_thread()
    import services
    client = services.get_first_client()
    return client

_dispatcher = vivlib2.main_thread.MainThreadDispatcher()

# adapter for command implementations that I want to execute from a repl
def ClientAction(*aliases, command_type=None, command_restrictions=None, pack=None, console_type=None):
    def _decorator(func):
        def __d(*args, **kwargs):
            @vivlib2.log_exception_and_raise
            def _exec():
                client = _get_client()
                session_id = client.id
                return func(_connection=session_id)
            _dispatcher.run_on_main_thread(_exec)
        return __d
        
    return _decorator
            
            
