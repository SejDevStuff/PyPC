import sys
import pygame
import math

import RAM

pygame.init()

size = (800,800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Screen")

class Video():
    def dbg_print(self, msg):
        print("[VIDEO] " + str(msg))

    def __init__(self, ram: RAM.RAMDisk):
        self.init = False
        self.ram = ram

        if (ram.sz < 160000):
            self.dbg_print("not enough memory, at least 160,000 bytes required")
            return
        
        # Clear VRAM
        self.vram_start_addr = ram.sz - 160000
        self.vram_end_addr = ram.sz
        __empty_bytes__ = []
        for i in range(160000):
            __empty_bytes__.append(b'\x00')
        self.ram.write_range(self.vram_start_addr, __empty_bytes__)
        self.dbg_print("memory address " + str(self.vram_start_addr) + " to " + str(self.vram_end_addr) + " reserved for video")
        self.kpBuf = 0
        self.init = True

    def getKeyPressed(self):
        kp = self.kpBuf
        self.kpBuf = 0
        return kp

    def tick(self):
        if not self.init:
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.init = False
            if event.type == pygame.KEYDOWN:
                self.kpBuf = event.key

        screen.fill((0,0,0))

        vram_contents = self.ram.read_range(self.vram_start_addr, self.vram_end_addr)
        vram_arr = [i.to_bytes(1, sys.byteorder) for i in vram_contents]

        for index, byte in enumerate(vram_arr):
            y = math.floor(index / 400)
            x = index - (y * 400)
            x *= 2
            y *= 2
            if byte == b'\x00':
                pygame.draw.rect(screen, (0,0,0), (x, y, 2,2))
            elif byte == b'\x01':
                pygame.draw.rect(screen, (255,255,255), (x, y, 2,2))
            else:
                self.dbg_print("tick: invalid byte " + str(byte) + " at addr " + str(index+160000))
                self.init = False
    
        pygame.display.flip()
        return True

    def quit(self):
        pygame.quit()