import RAM
import Disk
import Video
import CPU

import tempfile
import os
import threading
import sys

def main():
    print("Starting emulator...")
    td = tempfile.TemporaryDirectory()
    rdsz = 262144

    ram = RAM.RAMDisk(rdsz)
    disk = Disk.Disk()
    video = Video.Video(ram)

    if not os.path.exists("./Disk"):
        print("Disk doesn't exist. Creating...")
        diskName = input("Disk Name? : ")
        diskSz = input("Disk Size (bytes)? [Def: 1048576] : ")
        disk.create_disk("./Disk", diskName, int(diskSz))
    
    disk.load_disk("./Disk")
    cpu = CPU.CPU(ram, disk, video, td)

    # load bootloader
    cpu.set_exec_parameters(0)

    CPU_PROCESS = threading.Thread(target=cpu.process_next, args=())
    CPU_PROCESS.daemon = True
    CPU_PROCESS.start()

    keepRunning = True

    while True:
        #ram.write_byte_to_loc((ram.sz - 160000) + random.randint(0,159999), b'\x01')

        if not (CPU_PROCESS.is_alive()) and keepRunning:
            CPU_PROCESS.run()

        if not video.tick():
            keepRunning = False
            print("--- Closing Emulator ---")
            video.quit()
            break
    
    sys.exit(0)

if __name__ == "__main__":
    main()