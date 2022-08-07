Modified OS.py

- [FSDrv] Wrote prototype working create_file() implementation. 
The function can be called and used via code, but a command to wrap the function is not yet available.

- Added 'ls' command. 
This command will list the contents of the disk.

Modified FlashScript.py

- Added minify support.
FlashScript now tries to save as much space as possible (and also protects the source code a bit) by minifying your source code before compiling it.
You can pass the "nominify" argument to the command to tell FlashScript to not minify your code.