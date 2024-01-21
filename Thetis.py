import serial
import threading
from tkinter import Event

# Query Thetis:
# ZZIF;

# ZZIF
#     P1 P1 P1 P1 P1 P1 P1 P1 P1 P1 P1   11 chars VFO A frequency in Hz, leading 0's
#     P2 P2 P2 P2                         4 chars frequency step size (step <= 10,000)
#     P3 P3 P3 P3 P3 P3                   6 chars RIT/XIT leading + or -
#     P4                                  0/1 RIT OFF/ON
#     P5                                  0/1 XIT ON/OFF
#     P6                                  0 unused
#     P7 P7                               00 unused
#     P8                                  0/1 MOX OFF/ON
#     P9                                  1 char mode
#     P10                                 0 unused
#     P11                                 0 unused
#     P12                                 0/1 split OFF/ON
#     P13                                 0 unused
#     P14 P14                             00 unused
#     P15;                                0 unused

# Frequency Step:
# 0000      1 Hz
# 0001      2 Hz
# 1000     10 Hz
# 0010     25 Hz
# 1001     50 Hz
# 1010    100 Hz
# 0011    250 Hz
# 1011    500 Hz
# 1100  1,000 Hz
# 0100  2,000 Hz
# 0101  2,500 Hz
# 1101  5,000 Hz
# 1110  6,250 Hz
# 0110  9,000 Hz
# 0111 10,000 Hz

# 0000      1 Hz
# 0001      2 Hz
# 0010     25 Hz
# 0011    250 Hz
# 0100  2,000 Hz
# 0101  2,500 Hz
# 0110  9,000 Hz
# 0111 10,000 Hz
# 1000     10 Hz
# 1001     50 Hz
# 1010    100 Hz
# 1011    500 Hz
# 1100  1,000 Hz
# 1101  5,000 Hz
# 1110  6,250 Hz

# ZZFA00000000000; Set VFO A frequency

class Thetis:
    queryStr = b'ZZFA;ZZAC;'
    
    def __init__(self, port, root):
        self.root = root
        self.port = port

    def start(self):
        self.ser = serial.Serial(self.port, 115200, timeout=1)
        self.running = True
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.ser.close()

    def query(self):
        try:
            self.ser.write(Thetis.queryStr)
        except:
            pass

    def setVFOA(self, freq):
        try:
            self.ser.write(f'ZZFA{freq:011};'.encode())
        except:
            pass

    def run(self):
        while self.running:
            data = self.ser.read_until(b';')
            if len(data) > 0:
                Event.VirtualEventData = data.decode('utf-8')
                self.root.event_generate('<<THETIS>>', when='tail')



