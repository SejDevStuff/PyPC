# Simple OS, made for the PyPC
# https://github.com/SejDevStuff/PyPC

import sys
import queue
from string import punctuation
from tkinter import ON

from pygame import Cursor

class Alphabet():
    def __init__(self, video, ram):
        self.v = video
        self.r = ram
        self.ab = {}

        '''
        Pixel offsets for letters and symbols. You get a 3 by 5 area.
        
        Offsets are as follows:
        [  0  ] [  1  ] [  2  ]
        [ 400 ] [ 401 ] [ 402 ]
        [ 800 ] [ 801 ] [ 802 ]
        [1200 ] [1201 ] [1202 ]
        [1600 ] [1601 ] [1602 ]
        
        The numbers in the square brackets below are the pixels that should be WHITE
        For example, for "A", the top three pixels should be white, hence you
        would add the numbers 0, 1 and 2, and so on.
        '''

        self.ab["a"] = [0,1,2,400,402,800,801,802,1200,1202,1600,1602]
        self.ab["b"] = [0,1,2,400,402,800,801,802,1200,1202,1600,1601,1602]
        self.ab["c"] = [1,2,400,800,1200,1601,1602]
        self.ab["d"] = [0,1,400,402,800,802,1200,1202,1600,1601]
        self.ab["e"] = [0,1,2,400,800,801,1200,1600,1601,1602]
        self.ab["f"] = [0,1,2,400,800,801,1200,1600]
        self.ab["g"] = [0,1,2,400,800,802,1200,1202,1600,1601,1602]
        self.ab["h"] = [0,2,400,402,800,801,802,1200,1202,1600,1602]
        self.ab["i"] = [0,1,2,401,801,1201,1600,1601,1602]
        self.ab["j"] = [1,2,402,802,1202,1600,1601,1602]
        self.ab["k"] = [0,400,800,1200,1600,401,2,1201,1602]
        self.ab["l"] = [0,400,800,1200,1600,1601,1602]
        self.ab["m"] = [0,2,400,401,402,800,801,802,1200,1202,1600,1602]
        self.ab["n"] = [0,1,2,400,402,800,802,1200,1202,1600,1602]
        self.ab["o"] = [0,1,2,400,402,800,802,1200,1202,1600,1601,1602]
        self.ab["p"] = [0,1,2,400,402,800,801,802,1200,1600]
        self.ab["q"] = [0,1,2,400,402,800,801,802,1202,1602]
        self.ab["r"] = [0,1,2,400,402,800,801,802,1200,1201,1600,1602]
        self.ab["s"] = [0,1,2,400,800,801,802,1202,1600,1601,1602]
        self.ab["t"] = [0,1,2,401,801,1201,1601]
        self.ab["u"] = [0,2,400,402,800,802,1200,1202,1600,1601,1602]
        self.ab["v"] = [0,2,400,402,800,802,1200,1201,1202,1601]
        self.ab["w"] = [0,2,400,402,800,801,802,1200,1201,1202,1600,1602]
        self.ab["x"] = [0,2,400,402,801,1200,1202,1600,1602]
        self.ab["y"] = [0,2,400,402,800,801,802,1201,1601]
        self.ab["z"] = [0,1,2,402,801,1200,1600,1601,1602]

        self.ab["."] = [1601]
        self.ab[","] = [1601,2000]
        self.ab["!"] = [1,401,801,1601]
        self.ab[":"] = [401,1201]
        self.ab["-"] = [800,801,802]
        self.ab["_"] = [1600,1601,1602]
        self.ab["["] = [0,1,2,400,800,1200,1600,1601,1602]
        self.ab["]"] = [0,1,2,402,802,1202,1600,1601,1602]
        self.ab[">"] = [0,401,802,1201,1600]
        self.ab["<"] = [2,401,800,1201,1602]
        self.ab["^"] = [1,400,402]
        self.ab["'"] = [1,401]
        self.ab['"'] = [0,2,400,402]
        self.ab["{"] = [1,2,401,800,1201,1601,1602]
        self.ab["}"] = [0,1,401,802,1201,1600,1601]
        self.ab["\\"] = [0,400,801,1201,1602]
        self.ab["/"] = [2,402,801,1201,1600]
        self.ab[";"] = [401,1201,1600]
        self.ab["??"] = [1,2,400,800,801,1200,1600,1601,1602]
        # @ and $ impossible
        self.ab["%"] = [0,402,801,1200,1602]
        self.ab["+"] = [401,800,801,802,1201]
        self.ab["="] = [400,401,402,1200,1201,1202]

        self.ab["0"] = [1,400,402,800,802,1200,1202,1601]
        self.ab["1"] = [1,400,401,801,1201,1600,1601,1602]
        self.ab["2"] = [0,1,402,801,1200,1600,1601,1602]
        self.ab["3"] = [0,1,402,801,1202,1600,1601]
        self.ab["4"] = [0,2,400,402,800,801,802,1202,1602]
        self.ab["5"] = [1,2,400,800,801,802,1202,1600,1601]
        self.ab["6"] = [0,1,2,400,800,801,802,1200,1202,1600,1601,1602]
        self.ab["7"] = [0,1,2,402,801,1201,1601]
        self.ab["8"] = [0,1,2,400,402,800,801,802,1200,1202,1600,1601,1602]
        self.ab["9"] = [0,1,2,400,402,800,801,802,1202,1600,1601,1602]
        
        # Invalid is just all of the pixels being white, making a white box
        self.ab["__invalid__"] = [0,1,2,400,401,402,800,801,802,1200,1201,1202,1600,1601,1602]

    def print_chr(self, char, x, y):
        '''
        print_chr prints a single character.

        First, it works out where in Video RAM (VRAM) it should insert a 0x01 byte (telling the graphics
        driver to display a white pixel), by doing some maths using the X and Y coordinates.
        Then it checks if the character exists in the alphabet dictionary above, and if it does not and if it is
        not a space, it will display the "__invalid__" character (a fully white block). If the character is a space,
        it will leave it alone, if the character exists in the dictionary, it will set the starting address + the pixel
        offsets (the numbers in the brackets in the dictionary above) to 0x01, making it a white pixel. This will display
        the character
        '''
        start = self.v.vram_start_addr + ((y*400)-400)+x+3
        char = char.lower()
        if char != " ":
            l_dat = self.ab["__invalid__"]
            if char in self.ab:
                l_dat = self.ab[char]
                for addr in l_dat:
                    self.r.write_byte_to_loc(start + addr, b'\x01')
            for addr in l_dat:
                self.r.write_byte_to_loc(start + addr, b'\x01')
    
    def print_str(self, str, x, y):
        '''
        print_str prints an entire string. It takes care of incrementing the X and Y coordinates and also has word wrapping
        so if a string overflows, it moves onto the next line. print_str uses the print_chr function to actually print the
        characters.
        '''
        i = 0
        _x = x
        for char in str:
            if ((_x+(i*4)+8) >= 400):
                _x = x
                y += 10
                i = 0
            self.print_chr(char, _x + (i * 4), y)
            i += 1
    
    def drawBox(self, sx, sy, dx, dy, byte):
        '''
        drawBox draws a box from (sx, sy) to (dx, dy) by setting all the addresses in VRAM that fall into the coordinate 
        range to a byte determined by the "byte" parameter
        '''
        start = self.v.vram_start_addr + ((sy*400)-400)+sx
        end = self.v.vram_start_addr + ((dy*400)-400)+dx
        for i in range(end-start):
            self.r.write_byte_to_loc(start + i, byte)

class Filesystem():
    def __init__(self, disk) -> None:
        self.d = disk
        self.diskLoaded = False
        self.diskAddrStart = 0
        self.diskAddrEnd = 0

    def sfs_init(self, addr, sz):
        __empty__ = [b'\x01', b'\x02', b'\x03']
        entriesBytes = int(0).to_bytes(8, byteorder='big')
        entriesByteArray = [i.to_bytes(1, sys.byteorder) for i in entriesBytes]
        for eb in entriesByteArray:
            __empty__.append(eb)
        for i in range(sz - 11):
            __empty__.append(b'\x00')
        self.d.write_data(addr, __empty__)
        OneLineDown()
        Alpha.print_str("SFS_INIT: Wrote " + str(sz) + " bytes", 10, CursorY)

    def get_entry_list(self, silence_dfrag = False):
        entryList = {"Entries":[], "LastAddr":0}
        self.load_entries()
        Disk = self.d.read_data(self.diskAddrStart + 8, self.diskAddrEnd)
        Disk = [i.to_bytes(1, sys.byteorder) for i in Disk]
        addr = 0
        name_reached = False
        entries_read = 0
        entry_name = ""
        entry_start = 0
        defrag_warning_set = False

        while addr < len(Disk):
            byte = Disk[addr]
            if byte == b'\x0f':
                if not name_reached:
                    name_reached = True
                    entry_start = addr
                    addr += 1
                else:
                    addr += 1
                    name_reached = False
                    entrySz_Bytes = self.d.read_data(self.diskAddrStart + 8 + addr, self.diskAddrStart + 8 + addr + 8)
                    entrySz_ByteString = bytearray()
                    for eb in entrySz_Bytes:
                        entrySz_ByteString.append(eb)
                    entrySz = int.from_bytes(entrySz_ByteString, byteorder='big')
                    entries_read += 1
                    entryList["Entries"].append({"EntryName":entry_name, "EntryAddr":entry_start, "EntrySz":len(entry_name)+2+8+entrySz, "DataAddr": addr + 8, "DataSz": entrySz})
                    addr += entrySz + 8
                    entry_name = ""
            else:
                if byte == b'\x00':
                    if not defrag_warning_set and (entries_read > 0) and (entries_read != self.entries) and not silence_dfrag:
                        OneLineDown()
                        Alpha.print_str("[!] You need to defrag your disk, run 'diskdefrag' when you can", 10, CursorY)
                        defrag_warning_set = True
                if name_reached:
                    entry_name += byte.decode('utf-8')
                addr += 1
        
        if entries_read > 0:
            entryList["LastAddr"] = entryList["Entries"][-1]["EntryAddr"] + entryList["Entries"][-1]["EntrySz"]
        else:
            entryList["LastAddr"] = 0
        return entryList

    def ls_entries(self):
        entryList = self.get_entry_list()
        OneLineDown()
        Alpha.print_str("Directory Listing", 10, CursorY)
        OneLineDown()
        for entry in entryList["Entries"]:
            OneLineDown()
            Alpha.print_str(entry["EntryName"], 10, CursorY)

    def defrag_dsk(self):
        OneLineDown()
        Alpha.print_str("Defragmenting disk ...", 10, CursorY)
        disk = []
        _fragdisk = self.d.read_data(self.diskAddrStart + 8, self.diskAddrEnd)
        _fragdisk_bytes = [i.to_bytes(1, sys.byteorder) for i in _fragdisk]
        entryList = self.get_entry_list(True)
        for addr, byte in enumerate(_fragdisk_bytes):
            entryByte = False
            for entry in entryList["Entries"]:
                if addr >= entry["EntryAddr"] and addr < entry["EntryAddr"] + entry["EntrySz"]:
                    disk.append(byte)
                    entryByte = True
            if not entryByte:
                if byte != b"\x00":
                    disk.append(byte)
        BytesAtEnd = (self.diskAddrEnd - self.diskAddrStart + 8) - len(disk)
        for i in range(BytesAtEnd):
            disk.append(b"\x00")
        self.d.write_data(self.diskAddrStart + 8, disk)

    def get_contents_of_file(self, fn):
        entryList = self.get_entry_list()
        fileExists = False
        dataAddr = 0
        dataSz = 0
        for entry in entryList["Entries"]:
            name = entry["EntryName"]
            if fn == name:
                fileExists = True
                dataAddr = entry["DataAddr"]
                dataSz = entry["DataSz"]
                break
        if not fileExists:
            OneLineDown()
            Alpha.print_str("ERR: File does not exist", 10, CursorY)
            return
        return self.d.read_data(self.diskAddrStart + 8 + dataAddr, self.diskAddrStart + 8 + dataAddr + dataSz).decode()

    def remove_file(self, fn):
        entryList = self.get_entry_list()
        fileExists = False
        entryAddr = 0
        entrySz = 0
        for entry in entryList["Entries"]:
            name = entry["EntryName"]
            if fn == name:
                fileExists = True
                entryAddr = entry["EntryAddr"]
                entrySz = entry["EntrySz"]
                break
        if not fileExists:
            OneLineDown()
            Alpha.print_str("ERR: File does not exist", 10, CursorY)
            return
        
        OneLineDown()
        Alpha.print_str("Deleting file '" + str(fn) + "'", 10, CursorY)

        # Zero out the entry
        __empty_bytes__ = []
        for i in range(entrySz):
            __empty_bytes__.append(b"\x00")
        self.d.write_data(self.diskAddrStart + 8 + entryAddr, __empty_bytes__)

        # Update entry list
        self.entries -= 1
        entriesBytes = int(self.entries).to_bytes(8, byteorder='big')
        entriesByteArray = [i.to_bytes(1, sys.byteorder) for i in entriesBytes]
        self.d.write_data(self.diskAddrStart, entriesByteArray)

        # Defrag Disk
        self.defrag_dsk()

    def create_file(self, fn, data):
        entryList = self.get_entry_list()

        for entry in entryList["Entries"]:
            name = entry["EntryName"]
            if fn == name:
                OneLineDown()
                Alpha.print_str("ERR: File already exists", 10, CursorY)
                return

        if any(p in fn for p in punctuation):
            OneLineDown()
            Alpha.print_str("ERR: Illegal file name", 10, CursorY)
            return

        addr = entryList["LastAddr"]

        OneLineDown()
        Alpha.print_str("--> Writing file data at addr=" + str(addr), 10, CursorY)

        byte_arr = []

        for char in data:
            hex = "{:02x}".format(ord(char))
            byte_arr.append(bytes.fromhex(hex))
        
        FILENAME_BYTES = [b'\x0f']
        for char in fn:
            hex = "{:02x}".format(ord(char))
            FILENAME_BYTES.append(bytes.fromhex(hex))
        FILENAME_BYTES.append(b'\x0f')

        data_sz = int(len(byte_arr))
        szBytes = int(data_sz).to_bytes(8, byteorder='big')
        szByteArray = [i.to_bytes(1, sys.byteorder) for i in szBytes]

        if ((8 + addr + len(FILENAME_BYTES) + 8 + len(byte_arr)) > self.diskSz):
            OneLineDown()
            Alpha.print_str("There is not enough disk space to perform this action", 10, CursorY)
            return

        self.d.write_data(self.diskAddrStart + 8 + addr, FILENAME_BYTES)
        self.d.write_data(self.diskAddrStart + 8 + addr + len(FILENAME_BYTES), szByteArray)
        self.d.write_data(self.diskAddrStart + 8 + addr + len(FILENAME_BYTES) + 8, byte_arr)

        self.entries += 1
        entriesBytes = int(self.entries).to_bytes(8, byteorder='big')
        entriesByteArray = [i.to_bytes(1, sys.byteorder) for i in entriesBytes]

        self.d.write_data(self.diskAddrStart, entriesByteArray)
    
    def load_entries(self):
        entries_bytes = self.d.read_data(self.diskAddrStart, self.diskAddrStart + 8)
        entries_bytestring = bytearray()
        for eb in entries_bytes:
            entries_bytestring.append(eb)
        self.entries = int.from_bytes(entries_bytestring, byteorder='big')

    def load_disk(self, addr):
        Sz_Bytes = self.d.read_data(int(addr), int(addr) + 16)
        Sz_Bytestring = bytearray()
        for byte in Sz_Bytes:
            Sz_Bytestring.append(byte)
        Sz = int.from_bytes(Sz_Bytestring, byteorder='big')
        self.diskSz = Sz
        OneLineDown()
        Alpha.print_str("Disk Size: " + str(Sz), 10, CursorY)

        NewAddr = int(addr) + 16
        Disk = self.d.read_data(NewAddr, NewAddr + Sz)
        MagicNumber = Disk[0:3]
        if (MagicNumber != b'\x01\x02\x03'):
            OneLineDown()
            Alpha.print_str("ERR: Invalid magic bytes", 10, CursorY)
            return
        
        entries_bytes = self.d.read_data(NewAddr + 3, NewAddr + 11)
        entries_bytestring = bytearray()
        for eb in entries_bytes:
            entries_bytestring.append(eb)
        self.entries = int.from_bytes(entries_bytestring, byteorder='big')

        self.diskLoaded = True
        self.diskAddrStart = NewAddr + 3
        self.diskAddrEnd = NewAddr + 3 + (Sz - 11)

        OneLineDown()
        Alpha.print_str("Entries="+str(self.entries), 10, CursorY)
        OneLineDown()
        Alpha.print_str("Loaded disk!", 10, CursorY)

    def create_disk(self, addr, sz, fs):
        if fs.upper() not in ["SFS"]:
            OneLineDown()
            Alpha.print_str("ERR: Unsupported filesystem", 10, CursorY)
            return
        else:
            if ((addr + 16 + sz) > Disk.diskSize):
                OneLineDown()
                Alpha.print_str("ERR: Disk space too large", 10, CursorY)
                return
            szBytes = int(sz).to_bytes(16, byteorder='big')
            szByteArray = [i.to_bytes(1, sys.byteorder) for i in szBytes]
            OneLineDown()
            Alpha.print_str("Writing disk meta...", 10, CursorY)
            self.d.write_data(int(addr), szByteArray)
            self.sfs_init(int(addr)+16,int(sz))

# Shift Table: what to change values to if shift is on
ShiftTable = {
    ord("0"): ord(")"),
    ord("1"): ord("!"),
    ord("2"): ord("@"),
    ord("3"): ord("??"),
    ord("4"): ord("$"),
    ord("5"): ord("%"),
    ord("6"): ord("^"),
    ord("7"): ord("&"),
    ord("8"): ord("*"),
    ord("9"): ord("("),
    ord("-"): ord("_"),
    ord("="): ord("+"),
    ord("["): ord("{"),
    ord("]"): ord("}"),
    ord(":"): ord(";"),
    ord("'"): ord('"'),
    ord("\\"): ord("|"),
    ord(","): ord("<"),
    ord("."): ord(">"),
    ord("/"): ord("?")
}

KeyBuffer = ""
CursorY = 30
Shift = False
Control = False

Video = None
RAM = None
FileSys = None
Alpha = None
Disk = None

run = True

def WrongParameters(reqParams):
    OneLineDown()
    Alpha.print_str("ERR: Wrong amount of parameters. This command requires " + str(reqParams) + " parameter/s", 10, CursorY)

def ParseCommands(command):
    '''
    Simple command parsing function
    '''
    global CursorY
    alpha = Alpha
    v = Video
    r = RAM
    if command.strip() == "":
        return
    else:
        cmd = command.split(" ")
        if (cmd[0] == "clear"):
            if (len(cmd) > 1):
                WrongParameters(0)
                return
            alpha.drawBox(10,30,400,400,b'\x00')
            CursorY = 16
            return
        elif (cmd[0] == "ls"):
            if (len(cmd) > 1):
                WrongParameters(0)
                return
            if FileSys.diskLoaded == False:
                OneLineDown()
                alpha.print_str("No disk is loaded. Use the 'diskld' command to load a disk, or 'diskc' to create one", 10, CursorY)
                return
            FileSys.ls_entries()
        elif (cmd[0] == "diskld"):
            if len(cmd) != 2:
                WrongParameters(1)
                return
            if FileSys.diskLoaded == True:
                OneLineDown()
                alpha.print_str("[Warning] A disk was already loaded.", 10, CursorY)
            dsk_addr = 0
            try:
                dsk_addr = int(cmd[1])
            except:
                OneLineDown()
                alpha.print_str("ERR: Wrong parameter. This command requires 1 parameter: [INT]DiskAddr", 10, CursorY)
                return
            OneLineDown()
            alpha.print_str("Loading disk starting at byte " + str(dsk_addr) + " ...", 10, CursorY)
            FileSys.load_disk(dsk_addr)

        elif (cmd[0] == "diskc"):
            if (len(cmd) != 4):
                WrongParameters(3)
                return
            byte_start = 0
            dsk_sz = 0
            filesystem = "SFS"
            try:
                for arg in cmd[1:]:
                    a, v = arg.split("=")
                    if a == None or v == None:
                        OneLineDown()
                        alpha.print_str("ERR: Error parsing parameter", 10, CursorY)
                        return
                    if a == "--start-addr":
                        byte_start = int(v)
                    elif a == "--disk-sz":
                        dsk_sz = int(v)
                    elif a == "--fs":
                        if v.upper() not in ["SFS"]:
                            OneLineDown()
                            alpha.print_str("ERR: Error 'FS' must be one of: SFS", 10, CursorY)
                            return
                        filesystem = v
                OneLineDown()
                alpha.print_str("Creating a disk of size " + str(dsk_sz) + ", at addr " + str(byte_start) + " with fstype " + str(filesystem) + " ...", 10, CursorY)
            
                try:
                    FileSys.create_disk(byte_start, dsk_sz, filesystem)
                except Exception as e:
                    OneLineDown()
                    alpha.print_str("ERR: Error whilst running create_disk(): " + str(e), 10, CursorY)

            except:
                OneLineDown()
                alpha.print_str("ERR: This command requires 3 parameters. [INT]StartAddr, [INT]DiskSz, [CHAR]FileSystem", 10, CursorY)
                return
        
        elif (cmd[0] == "diskdefrag"):
            if FileSys.diskLoaded == False:
                OneLineDown()
                alpha.print_str("No disk is loaded. Use the 'diskld' command to load a disk, or 'diskc' to create one", 10, CursorY)
                return
            FileSys.defrag_dsk()
        
        elif (cmd[0] == "read"):
            if (len(cmd) != 2):
                WrongParameters(1)
                return
            if FileSys.diskLoaded == False:
                OneLineDown()
                alpha.print_str("No disk is loaded. Use the 'diskld' command to load a disk, or 'diskc' to create one", 10, CursorY)
                return
            contents = FileSys.get_contents_of_file(cmd[1])
            if contents != None:
                OneLineDown()
                alpha.print_str(contents, 10, CursorY)

        elif (cmd[0] == "create"):
            if (len(cmd) != 3):
                WrongParameters(2)
                return
            if FileSys.diskLoaded == False:
                OneLineDown()
                alpha.print_str("No disk is loaded. Use the 'diskld' command to load a disk, or 'diskc' to create one", 10, CursorY)
                return
            FileSys.create_file(cmd[1], cmd[2])
        
        elif (cmd[0] == "rm"):
            if (len(cmd) != 2):
                WrongParameters(1)
                return
            if FileSys.diskLoaded == False:
                OneLineDown()
                alpha.print_str("No disk is loaded. Use the 'diskld' command to load a disk, or 'diskc' to create one", 10, CursorY)
                return
            FileSys.remove_file(cmd[1])

        else:
            OneLineDown()
            alpha.print_str("ERR: Unknown command", 10, CursorY)

def OneLineDown():
    '''
    OneLineDown moves the cursor 1 character block down, it also takes care of moving everything up if we run out of space
    at the bottom
    '''
    global CursorY
    video = Video
    ram = RAM
    alpha = Alpha
    CursorY += 7
    if (CursorY >= 400):
        '''
        If we run out of space, move everything up a line.
        '''
        CursorY -= 7

        '''
        In essence, this chunk of code takes all the bytes that fall into the range (10,44) to (400,400) and writes them
        to the bytes that fall into the range (10,30) to (400,386) and then uses drawBox() to draw a black box from
        (10,394) to (400,400). This gives the illusion that everything has moved up one line and the topmost line has been
        deleted. It also frees up a line at the bottom.
        '''
        start = video.vram_start_addr + ((37*400)-400)+10
        end = video.vram_start_addr + (400 * 400)
        vram_contents = ram.read_range(start, end)
        __BYTES__ = [i.to_bytes(1, sys.byteorder) for i in vram_contents]
        topline = video.vram_start_addr + ((30*400)-400)+10
        ram.write_range(topline, __BYTES__)
        alpha.drawBox(10,(400-6),400,400,b'\x00')

def MAIN(cpu, ram, disk, td, video, q: queue.Queue):
    '''
    This is the main function called by the "CPU" of PyPC when a program is loaded
    '''
    global KeyBuffer, CursorY, Shift, Control, Alpha, FileSys, Video, RAM, Disk
    alpha = Alphabet(video, ram)
    fsdrv = Filesystem(disk)

    Alpha = alpha
    FileSys = fsdrv
    Video = video
    RAM = ram
    Disk = disk

    while run:
        alpha.drawBox(200,10,400,15,b'\x00')
        alpha.print_str("OS v2.0", 10, 10)
        alpha.drawBox(10,20,390,20,b'\x01')

        alpha.print_chr(">", 10, CursorY)
        alpha.print_str(KeyBuffer, 15, CursorY)

        ShiftCtrlString = ""
        if (Shift):
            ShiftCtrlString += "[Shift]"
        if (Control):
            ShiftCtrlString += " [Control]"
        
        alpha.print_str(ShiftCtrlString, 400 - (len(ShiftCtrlString) * 5), 10)
        
        KeyPressed = q.get()

        # Change value if shift is on
        if (Shift):
            if KeyPressed in ShiftTable:
                KeyPressed = ShiftTable[KeyPressed]
            Shift = False
        
        # Ctrl + C
        if (Control):
            if KeyPressed == ord("c") or KeyPressed == ord("C"):
                alpha.print_str("^C", 15 + (len(KeyBuffer) * 5), CursorY)
                OneLineDown()
                KeyBuffer = ""
                KeyPressed = 0
            Control = False

        if (KeyPressed >= 33 and KeyPressed <= 126):
            if (len(KeyBuffer) < (90)):
                KeyBuffer += chr(KeyPressed)
        if (KeyPressed == 32):
            KeyBuffer += " "
        if (KeyPressed == 8):
            alpha.drawBox(15,CursorY,(15+(len(KeyBuffer)*5)),CursorY+5,b'\x00')
            KeyBuffer = KeyBuffer[:-1]
        if KeyPressed == 13 or KeyPressed == 10:
            try:
                ParseCommands(KeyBuffer)
            except Exception as e:
                OneLineDown()
                alpha.print_str("Error whilst running command: " + str(e), 10, CursorY)
            OneLineDown()
            OneLineDown()
            KeyBuffer = ""
        if KeyPressed == 9990:
            Control = not Control
        if KeyPressed == 9991:
            Shift = not Shift