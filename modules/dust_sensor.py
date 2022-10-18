import time
import serial

class DUST:
    def __init__(self,port='/dev/ttyS0',baudrate=9600):
        self.port=port
        self.baudrate=baudrate
        self.setup()

    def setup(self):
        self.read_buffer=bytearray(40)
        self.serial=serial.Serial(self.port,self.baudrate,timeout=1)
        self.temp,self.hum,self.fmhds,self.pm2_5=None,None,None,None

    def __del__(self):
        self.serial.close()

    def notifyNextRead(self):
        self.serial.flushInput()

    def waitingFor40Byte(self):
        while(self.serial.in_waiting<=0):pass

    def readBuff(self):
        for i in range(40):
            self.read_buffer[i]=self.serial.read(1)
            time.sleep(0.01)

    def decodeReadBuff(self):
        PMS=0;FMHDS=0;TPS=0;HDS=0;CR2=0
        CR1=(self.read_buffer[38]<<8)+self.read_buffer[39]
        for i in range(38):CR2+=self.read_buffer[i]
        if CR1==CR2:
            PMSa=self.read_buffer[12];           #Read PM2.5 High 8-bit
            PMSb=self.read_buffer[13];           #Read PM2.5 Low 8-bit
            PMS=(PMSa<<8)+PMSb;                  #PM2.5 value
            FMHDSa=self.read_buffer[28];         #Read Formaldehyde High 8-bit
            FMHDSb=self.read_buffer[29];         #Read Formaldehyde Low 8-bit
            FMHDS=(FMHDSa<<8)+FMHDSb;            #Formaldehyde value
            TPSa=self.read_buffer[30];           #Read Temperature High 8-bit
            TPSb=self.read_buffer[31];           #Read Temperature Low 8-bit
            TPS=(TPSa<<8)+TPSb;                  #Temperature value
            HDSa=self.read_buffer[32];           #Read Humidity High 8-bit
            HDSb=self.read_buffer[33];           #Read Humidity Low 8-bit
            HDS=(HDSa<<8)+HDSb;                  #Humidity value
        self.temp,self.hum,self.fmhds,self.pm2_5=TPS/10.0,HDS/10.0,FMHDS,PMS

    def sample(self):
        self.notifyNextRead()
        self.waitingFor40Byte()
        self.readBuff()
        self.decodeReadBuff()

    def readTEMP(self):
        return self.temp

    def readHUM(self):
        return self.hum
    
    def readFMHDS(self):
        return self.fmhds

    def readPM2_5(self):
        return self.pm2_5