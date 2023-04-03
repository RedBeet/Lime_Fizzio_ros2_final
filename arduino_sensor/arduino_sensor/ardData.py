import serial
import math

py_serial = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600
)

class ArduinoData:
    def __init__(self) -> None:
        pass
    def getArduino(self):
        while 1:
            if py_serial.readable():
                
                heights = py_serial.readline().decode('utf-8')
                print(heights)
                return heights
    
    def subVelocity(self, v, w):
        py_serial.write(f"  v  {round(v , 2)}  w  {round(w, 2)}".encode)