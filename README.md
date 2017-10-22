# BLAMER

Blamer (SVN Gutter) is a plugin for Sublime Text 3 that allows you to quickly discover who has authored a line of code, if it has been committed using SVN.

> For the VS Code version of this plugin, please see [Blamer-vs](https://github.com/BeauAgst/blamer-vs)

## Commands

`ctrl + alt + s`: Save the file and commit the project folder

`ctrl + alt + b`: Visualises the blame on the current file 
## Features

Coloured "pips" are placed against every line in a file. Any lines from the same commit will be the same colour. Clicking a commit-disc will show a popup with the date, committer's name, and their comment.

### Demo ###

![Demonstration of how Blamer works](http://www.beaugust.co.uk/img/demos/blamer.gif)

### How do I get set up? ###

If you are taking this project from Github:
* Clone project 
* Copy folder to `C:\Users\YOUR NAME\AppData\Roaming\Sublime Text 3\Packages`, where YOUR NAME is replaced with your Users' name
* Restart Sublime.



## Requirements

This extension requires that you have Tortoise SVN installed, with command-line tools.

## Known Issues

- Popups don't appear if a line is empty (Sublime issue)