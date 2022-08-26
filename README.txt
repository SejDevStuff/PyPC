Modified OS.py

- [FSDrv] Wrote prototype working remove_file() implementation. 
The function can be called and used via code, but a command to wrap the function is not yet available.

- [FSDrv] Wrote prototype working defrag_dsk() implementation. 
The function can be called and used via code or via the "diskdefrag" command.

Modified Disk.py

- Better error messages.
Disk Errors now say the cause of the exception, rather than just saying "uncaught exception"