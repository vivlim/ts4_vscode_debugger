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