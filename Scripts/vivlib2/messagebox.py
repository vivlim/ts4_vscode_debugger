def show_messagebox(title, body):
    try:
        from external_python_utils import PackageDir
        package_dir = PackageDir("vscode_debug", output, external_python_path)
        package_dir.from_external_python_import("ctypes")
        package_dir.ensure_in_search_path()
        import ctypes

        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, title, body, 0)
    except:
        pass

def CatchAndMsgBox(title):
    def _deco(func):
        def __d(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                import traceback
                tb = traceback.format_exc()
                show_messagebox(title, tb)
        return __d
    return _deco
