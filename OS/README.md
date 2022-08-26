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
Arguments required: --start-addr=**StartAddr** --disk-sz=**DiskSz** --fs=**FileSystem**<br>
What it does: *Creates a disk of size ``DiskSz`` at ``StartAddr`` with filesystem ``FileSystem``*
PyPC OS currently only supports the Simple File System (``SFS``)
### ``diskdefrag``
Arguments required: **none**<br>
What it does: *Defrags the currently loaded disk*
### ``read``
Arguments required: **filename**<br>
What it does: *Prints the contents of ``filename``*
### ``create``
Arguments required: **filename**, **data**<br>
What it does: *Creates a file of name ``filename`` with ``data``*
### ``rm``
Arguments required: **filename**<br>
What it does: *Removes ``filename`` and defrags your disk for you*

## What are 'disks'?
User Space Disks, or Disks for short, in a PyPC OS perspective is a smaller partition located inside the main emulator drive, where the user can store their files. System files are not stored inside these disks. 

## What is the Simple File System?
The Simple File System (SFS) is a very simple filesystem implementation which allows users to store files. Due to it's simplistic nature, SFS only supports basic commands (read, write, copy, paste, etc.) and does not support directories - all user files are located in one giant "pool" of data.