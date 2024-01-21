import serial
import threading

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
    step_value = (1,2,10,25,50,100,250,500,1_000,2_000,2_500,5_000,6_250,9_000,10_000,12_500,
        15_000,20_000,25_000,30_000,50_000,100_000,250_000,500_000,1_000_000,10_000_000)

    def __init__(self, port):
        self._ser = serial.Serial(port, 115200, timeout=1)
        self._frequency = 0
        self._step = 0

    def start(self):
        self._running = True
        self._thread = threading.Thread(target = self.run)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()
        self._ser.close()

    def query(self):
        try:
            self._ser.write(Thetis.queryStr)
        except:
            pass

    def setVFOA(self, freq):
        try:
            self._ser.write(('ZZFA%011d;' % freq).encode())
        except:
            pass

    def onTurn(self, mult):
        step_inc = Thetis.step_value[self._step]
        self._frequency = (self._frequency // step_inc) * step_inc
        freq = self._frequency + mult * step_inc
        freq = min(max(freq, 100), 30_000_000)
        self.setVFOA(freq)

    def run(self):
        while self._running:
            data = self._ser.read_until(b';')
            if len(data) > 0:
                self._handle_line(data.decode())

    def _handle_line(self, data):
        d = str(data)
        if d[:4] == 'ZZFA':
            self._frequency = int(d[4:15])
        elif d[:4] == 'ZZAC':
            self._step = int(d[4:6])


