# ts4 vscode debugging

this is a (wip) script mod for the sims 4 which allows you to attach vscode's debugger and use it to debug python scripts running in-game.

## usage

1. make sure you have python 3.7.9 installed
2. clone this repo into `Documents\Electronic Arts\The Sims 4\Mods`
3. start the game, enter live mode
4. `ctrl+shift+c` to bring up the cheat console
5. type `vscode.debug` and press enter. the first time you run this, the script will install `debugpy` in a temporary directory. future runs will reuse that and be faster
6. if it succeeded, you'll see the message `started debugpy on port 5678`
7. run the 'Attach' vscode launch config. there's an example in this repo at `.vscode/launch.json`

## prior art

as far as I'm aware the only way to debug scripts before this was to use pycharm pro. i referred to and was inspired by a mixture of these resources:

- [Sigma1202's video: 'Sims 4 tutorial - how to debug your script mod'](https://www.youtube.com/watch?v=RBnS8m0174U)
    - When I tried this, I got an error: `No module named pydevd_pycharm`. I was able to fix that by extracting `pydevd-pycharm.zip` and re-zipping it. (making sure the resulting zip has the same folder structure)
        - I think the problem might be that the pydevd-pycharm.egg contains a zip "archive comment" which according to the zipimport docs was not supported before python 3.8. i found this when I tried to use zipimport.zipimporter directly on the zip file, I got an error claiming it was "not a Zip file".
- [June Hanabi's 'The Sims 4 Modern Python Modding: Debugging' tutorial](https://medium.com/analytics-vidhya/the-sims-4-modern-python-modding-debugging-3736b37dbd9f)
- [June Hanabi's (no longer maintained) template](https://github.com/junebug12851/Sims4ScriptingBPProj)
- [mycroftjr's fork of June Hanabi's template](https://github.com/mycroftjr/Sims4ScriptingTemplate)
- [andrew's 'Getting Started with Python Scripting' tutorial](https://sims4studio.com/thread/15145/started-python-scripting)
