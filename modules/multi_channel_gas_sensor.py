import time
import board
from busio import I2C

class GAS:
    GM_102B=0x01 #NO2
    GM_302B=0x03 #C2H5CH
    GM_502B=0x05 #VOC
    GM_702B=0x07 #CO
    WARMING_UP=0xFE #START
    WARMING_DOWN =0xFF #STOP
    
    def __init__(self,addr=8):
        self.addr=addr
        self.setup()
        self.preheat()

    def setup(self):
        self.read_buff=bytearray(4)
        self.write_buff=bytearray(1)
        self.i2c=I2C(board.SCL, board.SDA)

    def __del__(self):
        self.unPreheat()
        self.i2c.deinit()

    def delay(self,ms):
        time.sleep(ms/1000)

    def setWriteBuff(self,HEX):
        self.write_buff[0]=HEX

    def writeOut(self):
        self.i2c.writeto(self.addr,self.write_buff,start=0,end=1)
        self.delay(1)

    def preheat(self):
        self.setWriteBuff(self.WARMING_UP)
        self.writeOut()
        
    def unPreheat(self):
        self.setWriteBuff(self.WARMING_DOWN)
        self.writeOut()

    def readIn(self):
        self.i2c.readfrom_into(self.addr,self.read_buff,start=0,end=4)
        self.delay(1)

    def decodeReadBuff(self):
        return int.from_bytes(self.read_buff,byteorder='little')

    def readModule(self,SIG):
        self.setWriteBuff(SIG)
        self.writeOut()
        self.readIn()
        return self.decodeReadBuff()

    def readNO2(self):
        return self.readModule(self.GM_102B)

    def readC2H5CH(self):
        return self.readModule(self.GM_302B)

    def readVOC(self):
        return self.readModule(self.GM_502B)

    def readCO(self):
        return self.readModule(self.GM_702B)