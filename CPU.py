import RAM
import Disk
import Video

import random
import os
import marshal
import sys
import types

class CPU():
    def dbg_print(self, msg):
        print("[CPU] " + str(msg))

    def __init__(self, ram: RAM.RAMDisk, disk: Disk.Disk, video: Video.Video, td: str) -> None:
        self.ram = ram
        self.disk = disk
        self.td = td
        sys.path.insert(0, self.td.name)
        self.video = video
        self.exec_start = 0
        self.exec = False
    
    def set_exec_parameters(self, start: int):
        self.exec_start = start
        self.exec = True
    
    def process_next(self):
        if (not self.exec):
            return
        
        Sz_Bytes = self.disk.read_data(self.exec_start, self.exec_start + 16)

        if (Sz_Bytes == None):
            self.dbg_print("process_next: error whilst processing instruction")
            self.exec = False
            self.video.init = False
            return
        
        Sz_Bytestring = bytearray()

        for byte in Sz_Bytes:
            Sz_Bytestring.append(byte)
                
        Sz = int.from_bytes(Sz_Bytestring, byteorder='big')
        self.dbg_print("process_next: sz="+str(Sz))

        if (Sz == 0):
            self.dbg_print("process_next: no program found")
            self.exec = False
            self.video.init = False
            return

        Program = self.disk.read_data(self.exec_start + 16, self.exec_start + 16 + Sz)

        if (Program == None):
            self.dbg_print("process_next: error whilst processing instruction")
            self.exec = False
            self.video.init = False
            return

        Program_Bytes = [i.to_bytes(1, sys.byteorder) for i in Program]
        Pfp = os.path.join(self.td.name, str(random.randint(10000,99999))) + ".pyc"

        with open(Pfp, "wb") as f:
            for byte in Program_Bytes:
                f.write(byte)
        
        self.dbg_print("program file path: " + str(Pfp))

        pf = open(Pfp, 'rb')
        pf.seek(16)
        code_obj = marshal.load(pf)
        m = types.ModuleType("PyPC_CPU_Module", "Standard PyPC CPU Module")
        exec(code_obj, m.__dict__)

        m.MAIN(self, self.ram, self.disk, self.td, self.video)

        self.exec = False