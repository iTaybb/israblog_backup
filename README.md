# israblog_scrapper
A backup tool for Israblog
Useful for backing Israblog blogs until the site's going down (at 31/12/2017).

Run tui.py fur inteactive wizard for backing up, or scrapper.py for command-line options.
Works on Windows 7 and up, even though it can be made to work on Linux very easily.

Tested on Windows 10 with Python 3.5 and 3.6. Should work with any Windows 7 or better.
You'll have to install the plugins in the requirements.txt file.
Regarding Linux, it should work, but I didn't test it.

For building, you should also install the Windows 10 SDK, for the Universal CRT libraries to be available.
Without it, the build might not work on older Windows systems.
For more information, please see https://github.com/pyinstaller/pyinstaller/issues/1566

Thanks
Itay Brandes