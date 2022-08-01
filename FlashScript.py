import py_compile
import os
import sys
import tempfile
import Disk

td = tempfile.TemporaryDirectory()

fp1 = None
if (len(sys.argv) < 3):
    fp1 = input("Filepath to compile: ")
else:
    fp1 = sys.argv[1]

dp = "./Disk"
if not (os.path.exists(dp)):
    dp = input("Path to disk: ")

byte_start = 0
if (len(sys.argv) < 3):
    byte_start = input("Disk byte start: ")
else:
    byte_start = sys.argv[2]

if not (os.path.exists(fp1)):
    print("E1: File doesn't exist")
    sys.exit(1)

if not (os.path.exists(dp)):
    print("E2: Disk doesn't exist")
    sys.exit(1)

disk = Disk.Disk()

if not (disk.load_disk(dp)):
    print("E3: Cannot load disk")
    sys.exit(1)

_Compiled = os.path.join(td.name, os.path.basename(fp1) + ".pyc")
print("Compiled File Path: " + str(_Compiled))

py_compile.compile(fp1, _Compiled)

__byte_arr__ = []

with open(_Compiled, "rb") as f:
    while 1:
        byte = f.read(1)
        if not byte:
            break
        __byte_arr__.append(byte)

print("Total Size: " + str(len(__byte_arr__)))
print("Writing to disk ...")

_SZ = int(len(__byte_arr__))
_SZ_Bytes = _SZ.to_bytes(16, byteorder='big')
_SZ_Bytes_Array = [i.to_bytes(1, sys.byteorder) for i in _SZ_Bytes]

if ((int(byte_start) + _SZ + 16) > disk.diskSize):
    print("E5: Program too big error")
    sys.exit(1)

if not (disk.write_data(int(byte_start), _SZ_Bytes_Array)):
    print("E4: Disk write error")
    sys.exit(1)

if not (disk.write_data(int(int(byte_start)+16), __byte_arr__)):
    print("E4: Disk write error")
    sys.exit(1)

print("Done.")