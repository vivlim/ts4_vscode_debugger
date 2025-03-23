import vivlib2

@vivlib2.lazy_global
def wrapped_layers():
    return {}

def show_all_wrapped_layers():
    import vivlib2, vivlib2.main_thread
    log = vivlib2.get_logger()
    wll = wrapped_layers()
    for wlname in wll:
        log.info(f"Enabling layer {wlname}")
        wl = wll[wlname]

        wl.client_enable() # internally dispatches to main thread - safe to call from any thread

@vivlib2.log_exception_and_raise
def block_debugvis_text():
    import debugvis,sims4,vivlib2
    orig_get_layer = debugvis.get_layer
    class WrappedLayer:
        def __init__(self, l, name=None):
            self.l = l
            self.name = name

        @vivlib2.log_exception_and_raise
        def open(self):
            return self.l.open()
        @vivlib2.log_exception_and_raise
        def clear(self):
            return self.l.clear()
        @vivlib2.log_exception_and_raise
        def commit(self):
            return self.l.commit()
        @vivlib2.log_exception_and_raise
        def add_segment(self, a, b, color):
            return self.l.add_segment(a, b, color)
        @vivlib2.log_exception_and_raise
        def add_point(self, a, b, color):
            return self.l.add_point(a, b, color)  
        def add_text_screen(self, *args, **kwargs):
            pass
        def add_text_world(self, *args, **kwargs):
            pass
        def add_text_object(self, *args, **kwargs):
            pass
        def _exec_client_cmd(self, cmd):
          import vivlib2, vivlib2.main_thread
          @vivlib2.log_exception_and_raise
          def _exec_on_main_thread(self):
              import services
              client = services.get_first_client()
              sims4.commands.client_cheat(cmd, client.id)
          main_thread.run_on_main_thread(_exec_on_main_thread)

        def client_enable(self):
          if not self.Name:
            raise Exception("Layer has no name attached")
          self._exec_client_cmd('debugvis.layer.enable {0}'.format(self.name))

        def client_disable(self):
          if not self.Name:
            raise Exception("Layer has no name attached")
          self._exec_client_cmd('debugvis.layer.disable {0}'.format(self.name))

    @vivlib2.log_exception_and_raise
    def get_wrapped_layer(*args, **kwargs):
        # TODO: handle case where args is empty ...
        l = orig_get_layer(*args, **kwargs)
        name = args[0]
        wl = WrappedLayer(l, name=name)
        return wl
    debugvis.get_layer = get_wrapped_layer

    OrigContext = debugvis.Context
    orig_context_init = OrigContext.__init__
    import vivlib2.debug_vis_wrapper
    wrapped_layers = vivlib2.debug_vis_wrapper.wrapped_layers()
    @vivlib2.log_exception_and_raise
    def wrapped_init(*args, **kwargs):
        orig_context_init(*args, **kwargs)
        name = args[1]
        wrapped_layers[name] = True
    debugvis.Context.__init__ = wrapped_init