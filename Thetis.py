from datetime import datetime

from Semicolon import Semicolon
from eventID import ThetisEvent

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


QUERY_STR = b'ZZDU;'

STEP_AMT = (1,2,10,25,50,100,250,500,1_000,2_000,2_500,5_000,6_250,9_000,10_000,12_500,
    15_000,20_000,25_000,30_000,50_000,100_000,250_000,500_000,1_000_000,10_000_000)

class Thetis(Semicolon):
    def __init__(self, root, port, baud):
        super().__init__(root, port, baud)
        self.write('AI0;')
        
    def heartbeat(self):
        self.write(QUERY_STR)
        pass
 
    def turn(self, mult):
        s = b'ZZSA;' if mult < 0 else b'ZZSB;'
        self.write(s * abs(mult))

    def doFA(self, data):
        f = int(data[:11])
        self.send((ThetisEvent.FREQA.value, f))

    def doAC(self, data):
       s = STEP_AMT[int(data[:2])]
       self.send((ThetisEvent.STEP.value, s))


    def doDU(self, data):
        i = data.split(':')
        self.doFA(i[31])
        self.doAC(i[13])
        

    def doZZ(self, data):
        match (data[2:4]):
            case 'FA' :
                self.doFA(data[4:])                
            case 'AC':
                self.doAC(data[4:])
            case 'DU':
                self.doDU(data[4:])
            case _:
                print('doZZ', data)
                

    def process(self, data):
##        if data[-4:-2] == 'AI':
##            self.doDU(data[:-4])
##            return
        match data[:2]:
            case 'ZZ':
                self.doZZ(data)
            case 'FA' :
                self.doFA(data[2:])
            case _:
                print(f'Unknown {len(data)} {data}')

if __name__ == '__main__':
    from main import main
    main()

