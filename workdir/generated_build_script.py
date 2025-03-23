
import sys
sys.path.append('C:\\Users\\vivlim\\Documents\\Electronic Arts\\The Sims 4\\Mods\\ts4_vscode_debugger\\build_tools')
from compile import ScriptToCompile, compile_scripts

scripts = [
ScriptToCompile('C:\\Users\\vivlim\\Documents\\Electronic Arts\\The Sims 4\\Mods\\ts4_vscode_debugger\\stage\\inspector_gadget.py'),
ScriptToCompile('C:\\Users\\vivlim\\Documents\\Electronic Arts\\The Sims 4\\Mods\\ts4_vscode_debugger\\stage\\vivlib2\\draw.py'),
ScriptToCompile('C:\\Users\\vivlim\\Documents\\Electronic Arts\\The Sims 4\\Mods\\ts4_vscode_debugger\\stage\\vivlib2\\main_thread.py'),
ScriptToCompile('C:\\Users\\vivlim\\Documents\\Electronic Arts\\The Sims 4\\Mods\\ts4_vscode_debugger\\stage\\vivlib2\\queues.py'),
ScriptToCompile('C:\\Users\\vivlim\\Documents\\Electronic Arts\\The Sims 4\\Mods\\ts4_vscode_debugger\\stage\\vivlib2\\__init__.py'),

]

compile_scripts(scripts)

