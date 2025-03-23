from pathlib import Path
import typing

unstage_sources_after_compile = True

class SpecificPythonVersion:
    def __init__(self, version: str, path: Path):
        self.version = version
        self.path = path
        pass
    
    def run_script(self, script_filename: Path):
        import subprocess,sys
        print(f'using python {self.version}: {repr(str(self.path))} {repr(str(script_filename))}')
        r = subprocess.run([self.path.absolute(), script_filename.absolute()], stdout=sys.stdout, stderr=sys.stderr)
        r.check_returncode()

class ScriptToCompile:
    def __init__(self, source: str):
        self.source = source
        if not self.source.endswith('.py'):
            raise Exception(f'Can only compile .py files, this is {self.source}')
        self.target = Path(str(self.source) + 'c')

    def compile(self):
        print(f'compiling: {self.source}')
        import py_compile,os
        any_success = False
        for o in [2,1,0]:
            print(f'  attempting optimize={o}')
            try:
                pyc_filename = py_compile.compile(self.source, doraise=True, optimize=o)
                any_success = True

                os.rename(pyc_filename, self.target)
                break
            except Exception as e:
                print(f'    failed: {e}')
        if not any_success:
            raise Exception(f'Failed to compile {self.source}')
            


def compile_scripts_with_python(stage: Path, workdir: Path, glob, version: str):
    py = get_specific_python(version)
    script_fn = generate_build_script(stage, workdir, glob, py)

    # before compiling, make sure there no __pycache__s
    for pycache in stage.glob('**/__pycache__'):
        for f in pycache.iterdir():
            raise Exception(f'pycache dir {pycache} unexpectedly contains files before build')
        pycache.rmdir()

    py.run_script(script_fn)

    # make sure all __pycache__ are empty and remove them
    for pycache in stage.glob('**/__pycache__'):
        for f in pycache.iterdir():
            raise Exception(f'pycache dir {pycache} unexpectedly contains files after build')
        pycache.rmdir()
    
    # make sure all .py have a corresponding .pyc
    for py_file in stage.glob('**/*.py'):
        corresponding_pyc = Path(str(py_file) + 'c')
        if corresponding_pyc.exists() and corresponding_pyc.is_file():
            if unstage_sources_after_compile:
                py_file.unlink()

def generate_build_script(stage: Path, workdir: Path, glob, py: SpecificPythonVersion) -> Path:
    script_fn = workdir.joinpath('generated_build_script.py')

    def path_str(path: Path) -> str:
        return repr(str(path))

    header = f'''
import sys
sys.path.append({path_str(Path(__file__).parent.absolute())})
from compile import ScriptToCompile, compile_scripts

scripts = [
'''
    footer = f'''
]

compile_scripts(scripts)

'''

    with script_fn.open(mode='w') as script:
        script.write(header)
        for path in stage.glob(glob):
            script.write(f'ScriptToCompile({path_str(path)}),\n')
        script.write(footer)
    
    return script_fn

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

def compile_scripts(scripts: typing.List[ScriptToCompile]):
    for s in scripts:
        try:
            s.compile()
        except Exception as e:
            print(f'Failed to compile {s}: {e}')
            raise e
