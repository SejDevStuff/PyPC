# PyPC OS

## Commands
### ``clear``
Arguments required: **none**<br>
What it does: *Clears the screen*
### ``ls``
Arguments required: **none**<br>
What it does: *Lists the files inside the currently loaded disk (Directories not currently supported)*
### ``diskld``
Arguments required: **disk_addr**<br>
What it does: *Loads the disk located at ``disk_addr``*
### ``diskc``
Arguments required: **StartAddr, DiskSz, FileSystem**<br>
What it does: *Creates a disk of size ``DiskSz`` at ``StartAddr`` with filesystem ``FileSystem``*
PyPC OS currently only supports the Simple File System (``SFS``)

## What are 'disks'?
User Space Disks, or Disks for short, in a PyPC OS perspective is a smaller partition located inside the main emulator drive, where the user can store their files. System files are not stored inside these disks. 

## What is the Simple File System?
The Simple File System (SFS) is a very simple filesystem implementation which allows users to store files. Due to it's simplistic nature, SFS only supports basic commands (read, write, copy, paste, etc.) and does not support directories - all user files are located in one giant "pool" of data.