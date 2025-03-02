# SPDX-SnippetCopyrightText: 2025 viviridian
# SPDX-License-Identifier: MIT OR Apache-2.0

import sims4.commands
import typing

# If the script can't find your python 3.7 instance automatically, set this
external_python_path = None
# external_python_path = "C:\\Users\\you\\AppData\\Local\\Programs\\Python\\Python37\\python.exe"

@sims4.commands.Command('vscode.debug.helloworld', command_type=sims4.commands.CommandType.Live)
def hello_world(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("hello world")

def ensure_modules_importable():
    import os,sys
    modules_path = os.path.dirname(__file__)
    if not os.path.exists(modules_path):
        raise Exception(f'missing modules path: {modules_path}')

    if not modules_path in sys.path:
        sys.path.append(modules_path)

@sims4.commands.Command('vscode.debug', command_type=sims4.commands.CommandType.Live)
def start_vscode_debugger(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output("starting debugger...")

    try:
        ensure_modules_importable()
        from external_python_utils import PackageDir, WantedPackage

        # the port debugpy will listen on
        debugpy_port = 5678

        package_dir = PackageDir("vscode_debug", output, external_python_path)
        package_dir.pip_packages([
            WantedPackage(name="debugpy", version="1.5.1")
        ])
        package_dir.from_external_python_import("ctypes")
        package_dir.ensure_in_search_path()
        
        # ready to actually try importing now.
        output("attempting to import debugpy")

        import debugpy
        output("imported debugpy")
        # we need to tell debugpy what python.exe to use to run the debug server - otherwise it will try to use TS4_x64.exe which will fail
        debugpy.configure({
            "python": package_dir.external_python_path, # PackageDir will attempt to detect python's location, so prefer that
        })
        debugpy.listen(debugpy_port)
        output(f'started debugpy on port {str(debugpy_port)}')

    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        output(f'failed with a {type(e)}: {e}')

        # print traceback line by line so it isn't truncated.
        for line in tb.splitlines():
            output(line)
