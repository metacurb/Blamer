# BLAMER #

Blamer is a plugin for Sublime Text 3 that allows you to quickly discover who has authored a line of code, if it has been committed using SVN.

Coloured discs are placed against every line in a file. Any lines from the same commit will be the same colour. Clicking a commit-disc will show a popup with the date, committer's name, and their comment.

### Demo ###

![Demonstration of how Blamer works](http://www.beaugust.co.uk/img/demos/blamer.gif)

### How do I get set up? ###

* Clone project 
* Copy folder to `C:\Users\YOUR NAME\AppData\Roaming\Sublime Text 3\Packages`, where YOUR NAME is replaced with your Users' name
* Inside the Blamer folder is another folder called Blamer. Copy that folder to `C:\Users\YOUR NAME\AppData\Local\Sublime Text 3\Cache`, following the same principle above. 
* Restart Sublime.

### How do I use it? ###

Once Sublime Text is open, navigate to Preferences > Package Settings > Blamer > Settings - Default. In here you will find 3 options -

* `root_folder`: You need to change this to the name of your V10 folder (case sensitive)
* `auto_blame`: Set this to **true** or **false**. If true, files will auto-blame as soon as they're opened.
* `auto_blame_format`: Set this to the file format that you want to blame. Set it to ***** to blame ALL file-types.

Once you have adjusted your preferences, you're all set.

### Shortcuts ###

* `ctrl + alt + s`: Save the file and commit the project folder
* `ctrl + alt + b`: Refreshes the blame on the current file, or generates it if you have `auto_blame` set to **false**.