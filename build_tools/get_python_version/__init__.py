import pathlib

class SpecificPythonVersion:
    def __init__(self, version: str, path: pathlib.Path):
        self.version = version
        self.path = path
        pass
    
    def run_script(self, script_filename: pathlib.Path):
        import subprocess
        print(f'using python {self.version}: {repr(str(self.path))} {repr(str(script_filename))}')
        subprocess.check_call([self.path.absolute(), script_filename.absolute()])

def get_specific_python(version: str) -> SpecificPythonVersion:
    import os,winreg

    def try_get_python_from_registry(key, sub_key):
        try:
            k = winreg.OpenKey(key, sub_key)
            try:
                result = winreg.QueryValueEx(k, "ExecutablePath")
                return result[0]
            finally:
                winreg.CloseKey(k)
        except:
            return None

    # keys that may contain a python path - https://stackoverflow.com/a/648552
    for key, sub_key in [
        (winreg.HKEY_LOCAL_MACHINE, f'Software\\Python\\PythonCore\\{version}\\InstallPath'),
        (winreg.HKEY_CURRENT_USER, f'Software\\Python\\PythonCore\\{version}\\InstallPath'),
        (winreg.HKEY_LOCAL_MACHINE, f'Software\\Wow6432Node\\Python\\PythonCore\\{version}\\InstallPath'),
    ]:
        pp = try_get_python_from_registry(key, sub_key)
        if pp and os.path.exists(pp):
            import pathlib
            py_path = pathlib.Path(pp)
            if py_path.exists():
                return SpecificPythonVersion(version, py_path)
            raise Exception(f'Python was found at {py_path.absolute()} but doesn\'t seem to actually exist')


    raise Exception(f"Did not find python {version} install in registry")