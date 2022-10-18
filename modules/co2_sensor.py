import serial

class CO2:
    def __init__(self,port='/dev/ttyUSB0',baudrate=9600):
        self.port=port
        self.baudrate=baudrate

    def setup(self):
        self.read_buffer=None
        self.next_read_command=bytearray(b'\xFF\x01\x86\x00\x00\x00\x00\x00\x79')
        self.serial=serial.Serial(self.port,self.baudrate,timeout=1,write_timeout=1)

    def __del__(self):
        self.serial.close()

    def notifyNextRead(self):
        self.serial.write(self.next_read_command)

    def waitingFor9Byte(self):
        while(self.serial.in_waiting<9):pass

    def readBuff(self):
        self.read_buffer=self.serial.read(9)

    def decodeReadBuff(self):
        low=int(self.read_buffer[3])
        high=int(self.read_buffer[2])
        return high*256+low

    def readCO2(self):
        self.notifyNextRead()
        self.waitingFor9Byte()
        self.readBuff()
        return self.decodeReadBuff()