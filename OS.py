# Simple OS, made for the PyPC
# https://github.com/SejDevStuff/PyPC

import sys
import queue

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
        self.ab["£"] = [1,2,400,800,801,1200,1600,1601,1602]
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

# Shift Table: what to change values to if shift is on
ShiftTable = {
    ord("0"): ord(")"),
    ord("1"): ord("!"),
    ord("2"): ord("@"),
    ord("3"): ord("£"),
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

def ParseCommands(command, alpha, v, r):
    '''
    Simple command parsing function
    '''
    global CursorY
    if command.strip() == "":
        return
    else:
        cmd = command.split(" ")
        if (cmd[0] == "clear"):
            alpha.drawBox(10,30,400,400,b'\x00')
            CursorY = 16
            return
        else:
            OneLineDown(v, r, alpha)
            alpha.print_str("ERR: Unknown command", 10, CursorY)

def OneLineDown(video, ram, alpha):
    '''
    OneLineDown moves the cursor 1 character block down, it also takes care of moving everything up if we run out of space
    at the bottom
    '''
    global CursorY
    CursorY += 14
    if (CursorY >= 400):
        '''
        If we run out of space, move everything up a line.
        '''
        CursorY -= 14

        '''
        In essence, this chunk of code takes all the bytes that fall into the range (10,44) to (400,400) and writes them
        to the bytes that fall into the range (10,30) to (400,386) and then uses drawBox() to draw a black box from
        (10,394) to (400,400). This gives the illusion that everything has moved up one line and the topmost line has been
        deleted. It also frees up a line at the bottom.
        '''
        start = video.vram_start_addr + ((44*400)-400)+10
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
    global KeyBuffer, CursorY, Shift, Control
    alpha = Alphabet(video, ram)
    while True:
        alpha.drawBox(200,10,400,15,b'\x00')
        alpha.print_str("OS v1.0", 10, 10)
        alpha.drawBox(10,20,390,20,b'\x01')
        alpha.print_chr(">", 10, CursorY)
        alpha.print_str(KeyBuffer, 15, CursorY)

        ShiftCtrlString = ""
        if (Shift):
            ShiftCtrlString += "[Shift] On."
        if (Control):
            ShiftCtrlString += " [Control] On."
        
        alpha.print_str(ShiftCtrlString, 200, 10)
        
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
                OneLineDown(video, ram, alpha)
                KeyBuffer = ""
                KeyPressed = 0

        if (KeyPressed >= 33 and KeyPressed <= 126):
            if (len(KeyBuffer) < (90)):
                KeyBuffer += chr(KeyPressed)
        if (KeyPressed == 32):
            KeyBuffer += " "
        if (KeyPressed == 8):
            alpha.drawBox(15,CursorY,(15+(len(KeyBuffer)*5)),CursorY+5,b'\x00')
            KeyBuffer = KeyBuffer[:-1]
        if KeyPressed == 13 or KeyPressed == 10:
            ParseCommands(KeyBuffer, alpha, video, ram)
            OneLineDown(video, ram, alpha)
            KeyBuffer = ""
        if KeyPressed == 9990:
            Control = not Control
        if KeyPressed == 9991:
            Shift = not Shift