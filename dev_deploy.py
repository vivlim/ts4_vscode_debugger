echo_commands = False
script_mod_prefix = 'viviridian_inspector_gadget'

import pathlib,os

this_path = pathlib.Path(__file__)

def shellexec(cmd):
    import subprocess,sys
    if echo_commands:
        print(f'exec: {cmd}')
    r = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    r.check_returncode()

def from_rel(p):
    target = this_path.parent.joinpath(p).resolve()
    if not target.exists():
        raise FileNotFoundError(f'File not found: {target}')
    return target

class Lazy:
    def __init__(self, value_fn):
        self.value_fn = value_fn
        self.value_fn_run = False
        self.value_fn_raised = None
        self.value = None

    
    def get(self):
        if self.value_fn_run:
            return self.value
        if self.value_fn_raised:
            raise self.value_fn_raised
        try:
            self.value = self.value_fn()
            self.value_fn_run = True
            return self.value
        except Exception as e:
            self.value_fn_raised = e
            raise e

def get_mods_path():
    import os, pathlib
    p = os.path.expanduser('~/Documents/Electronic Arts/The Sims 4/Mods')
    p = pathlib.Path(p)
    if not p.is_dir():
        raise Exception(f'{p} not found or is not a directory')
    return p

def match_script_mod_in_dir(dir: pathlib.Path):
    for p in dir.iterdir():
        if p.name.startswith(script_mod_prefix) and p.name.endswith('ts4script'):
            yield p

mods_path = get_mods_path()

for s in match_script_mod_in_dir(from_rel('out')):
    print(f'cleaning output dir: remove {str(s)}')
    s.unlink()

shellexec(['python', str(from_rel('build.py'))])

for s in match_script_mod_in_dir(mods_path):
    print(f'removing existing {str(s)}')
    s.unlink()

for s in match_script_mod_in_dir(from_rel('out')):
    import shutil
    target = mods_path.joinpath(s.name)
    print(f'copying {str(s)} to {target}')
    shutil.copyfile(s, target)

# Remove stage so the game doesn't try to use sources from that path.
shutil.rmtree(from_rel('stage'))