Modified OS.py

- [Bugfixes] Fixed bugs with Filesystem Driver (FSDrv) and also worked on improvements to make system more stable

- [FSDrv] Wrote prototype working get_contents_of_file() implementation. 
The function can be called and used via code or via the "read" command. With that, SFS should be finished. Future commands simply use these three functions. For example: "mv" simply remove the current file and create a new one with a new name and the same contents, etc.

- New command: read (wrapper for get_contents_of_file())

- New command: create (wrapper for create_file())

- New command: rm (wrapper for remove_file())

Modified Disk.py

- Disabled the "reading bytes [...]" debug message as it can get quite spammy