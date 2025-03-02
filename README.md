# ts4 vscode debugging

this is a (wip) script mod for the sims 4 which allows you to attach vscode's debugger and use it to debug python scripts running in-game.

## usage

1. make sure you have python 3.7.9 installed
2. clone this repo into `Documents\Electronic Arts\The Sims 4\Mods`
3. start the game, enter live mode
4. `ctrl+shift+c` to bring up the cheat console
5. type `vscode.debug` and press enter. the first time you run this, the script will install `debugpy` in a temporary directory. future runs will reuse that and be faster
6. if it succeeded, you'll see the message `started debugpy on port 5678`
7. run the 'Attach' vscode launch config