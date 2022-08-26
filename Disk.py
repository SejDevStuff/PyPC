import os

class Disk():
    def dbg_print(self, msg):
        print("[DISK] " + str(msg))

    def create_disk(self, diskpath, diskname, sz_bytes = 1048576):
        try:
            self.dbg_print("create_disk: making disk of size " + str(sz_bytes))

            if os.path.exists(diskpath):
                self.dbg_print("create_disk: disk path exists")
                return False
            
            os.mkdir(diskpath)

            with open(os.path.join(diskpath, "meta"), "w") as f:
                self.dbg_print("create_disk: writing meta")
                f.write("NAME="+str(diskname)+"\nSZ="+str(sz_bytes)+"\nVER=2")
            
            self.dbg_print("create_disk: writing zeros")

            dsk_path = os.path.join(diskpath, "DSK")
            with open(dsk_path, "ab") as f:
                for j in range(sz_bytes):
                    f.write(b'\x00')
            
            self.dbg_print("create_disk: done")
            return True
        except Exception as e:
            self.dbg_print("create_disk: uncaught exception. " + str(e))
    
    def load_disk(self, diskpath):
        try:
            self.dbg_print("load_disk: loading disk : " + str(diskpath))
            if not os.path.exists(os.path.join(diskpath, "meta")):
                self.reset()
                self.dbg_print("load_disk: corrupt disk (no meta)")
                return False
            self.dbg_print("load_disk: reading meta")

            with open(os.path.join(diskpath, "meta"), "r") as f:
                entries = f.readlines()
                for entry in entries:
                    if entry.strip() != "":
                        k, v = entry.split("=")
                        k = k.strip()
                        v = v.strip()
                        if k == "VER":
                            if v != "2":
                                self.dbg_print("load_disk: incompatible disk version")
                                return False
                        if k == "NAME":
                            self.diskName = v
                        if k == "SZ":
                            self.diskSize = int(v)
            
            if (self.diskName == None or self.diskSize == None):
                self.reset()
                self.dbg_print("load_disk: corrupt disk (corrupt meta)")
                return False
            
            self.dbg_print("load_disk: disk name: " + str(self.diskName) + ", disk sz: " + str(self.diskSize))
            
            self.dbg_print("load_disk: checking disk size")

            sz = os.path.getsize(os.path.join(diskpath, "DSK"))
            if sz != self.diskSize:
                self.dbg_print("load_disk: incorrect disk size")
                self.reset()
                return False
            
            self.diskPath = os.path.join(diskpath, "DSK")
            self.dbg_print("load_disk: disk loaded successfully")
            return True
        except Exception as e:
            self.dbg_print("load_disk: uncaught exception. " + str(e))

    def read_data(self, start_addr = 0, end_addr = 1):
        try:
            if (self.diskName == None or self.diskSize == None or self.diskPath == None):
                self.dbg_print("read_data: disk not properly loaded")
                return None
            if (start_addr < 0 or start_addr > self.diskSize):
                self.dbg_print("read_data: invalid start_addr")
                return None
            if (end_addr < 0 or end_addr > self.diskSize or end_addr < start_addr):
                self.dbg_print("read_data: invalid end_addr")
                return None
            
            self.dbg_print("read_data: reading bytes " + str(start_addr) + " -> " + str(end_addr))

            with open(self.diskPath, "rb") as f:
                f.seek(start_addr)
                return f.read(end_addr - start_addr)
            
        except Exception as e:
            self.dbg_print("read_data: uncaught exception. " + str(e))

    def write_data(self, addr = 0, byte_arr = [b'\x00']):
        try:
            if (self.diskName == None or self.diskSize == None or self.diskPath == None):
                self.dbg_print("write_data: disk not properly loaded")
                return False
            if (addr < 0):
                self.dbg_print("write_data: addr less than zero")
                return False
            if (addr > self.diskSize):
                self.dbg_print("write_data: requested byte outside range")
                return False
            if ((addr + len(byte_arr)) > self.diskSize):
                self.dbg_print("write_data: write buffer exceeds range")
                return False
            
            self.dbg_print("write_data: writing " + str(len(byte_arr)) + " bytes to addr=" + str(addr))

            with open(self.diskPath, "r+b") as f:
                f.seek(addr)
                for byte in byte_arr:
                    f.write(byte)
            return True

        except Exception as e:
            self.dbg_print("write_data: uncaught exception. " + str(e))

    def reset(self):
        self.diskName = None
        self.diskSize = None
        self.diskPath = None

    def __init__(self):
        self.diskName = None
        self.diskSize = None
        self.diskPath = None