import os
from traceback import print_exc

class RAMDisk():
    def dbg_print(self, msg):
        print("[RAMDISK] " + str(msg))

    def __init__(self, sz = 1024):
        self.dbg_print("creating ramdisk of size " + str(sz))
        self.__RAM__ = bytearray(sz)
        self.sz = sz
    
    def write_byte_to_loc(self, addr = 0, byte = b'\x00'):
        try:
            if (addr > self.sz):
                self.dbg_print("write_byte_to_loc: requested byte outside range")
                return False
            
            if (addr < 0):
                self.dbg_print("write_byte_to_loc: addr less than zero")
                return False

            self.__RAM__[addr] = byte[0]
            return True
        except Exception as e:
            self.dbg_print("write_byte_to_loc: uncaught exception")
    
    def read_byte_from_loc(self, addr = 0):
        try:
            if (addr > self.sz):
                self.dbg_print("read_byte_from_loc: requested byte outside range")
                return None
            
            if (addr < 0):
                self.dbg_print("read_byte_from_loc: addr less than zero")
                return None

            return bytes(self.__RAM__[addr])
        except:
            self.dbg_print("read_byte_from_loc: uncaught exception")
    
    def write_range(self, start_addr = 0, byte_arr = [b'\x00']):
        try:
            if (start_addr > self.sz):
                self.dbg_print("write_range: requested byte outside range")
                return False
            if (start_addr < 0):
                self.dbg_print("write_range: start_addr less than zero")
                return False
            if ((start_addr + len(byte_arr)) > self.sz):
                self.dbg_print("write_range: write buffer exceeds range")
                return False

            index = start_addr
            for byte in byte_arr:
                self.__RAM__[index] = byte[0]
                index += 1
            
            return True
        except:
            self.dbg_print("write_range: uncaught exception")

    def read_range(self, start_addr = 0, end_addr = 1):
        try:
            if (start_addr > self.sz):
                self.dbg_print("read_range: requested byte outside range")
                return None
            if (start_addr < 0):
                self.dbg_print("read_range: start_addr less than zero")
                return None
            if (end_addr < 0):
                self.dbg_print("read_range: end_addr less than zero")
                return None
            if (end_addr > self.sz):
                self.dbg_print("read_range: requested byte outside range")
                return None
            if (end_addr < start_addr):
                self.dbg_print("read_range: end_addr must be bigger than start_addr")
                return None

            return self.__RAM__[start_addr:(end_addr+1)]
        except:
            self.dbg_print("read_range: uncaught exception")