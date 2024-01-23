from Semicolon import Semicolon
from datetime import datetime

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

THETIS_DATA = '<<THETIS_DATA>>'

QUERY_STR = 'ZZFA;ZZAC;'.encode()
STEP = (1,2,10,25,50,100,250,500,1_000,2_000,2_500,5_000,6_250,9_000,10_000,12_500,
    15_000,20_000,25_000,30_000,50_000,100_000,250_000,500_000,1_000_000,10_000_000)

class Thetis(Semicolon):
    def __init__(self, root, port, baud):
        self.timestamp = datetime.now().timestamp()
        super().__init__(root, port, baud)
        
    def heartbeat(self):
        if (new_timestamp := datetime.now().timestamp()) - self.timestamp > 1:
            self.root.queue_quit()
        self.timestamp = new_timestamp
        self.write(QUERY_STR)
 
    def turn(self, mult):
        self.freqa = (self.freqa // self.step) * self.step
        freq = self.freqa + mult * self.step
        freq = min(max(freq, 100), 30_000_000)
        self.write(f'ZZFA{freq:011};'.encode())

    def update(self, field, value):
        if value != self.__dict__.get(field, None):
            self.__dict__[field] = value
            self.send(THETIS_DATA, (field, value))

    def process(self, data):
        if len(data) > 5:
            match (data[:4]):
                case 'ZZFA':
                    self.update('freqa', int(data[4:15]))
                case 'ZZAC':
                    self.update('step', STEP[int(data[4:6])])
