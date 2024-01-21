import serial
import threading
from tkinter import Event


# Sending from FlexControl to host:
# All commands terminate with ';' (no returns or line feeds)
# U; - knob CW (single tick) -- U02; U03; U04; etc - multiticks
# D; - knob CCW (single tick) -- D02; D03; D04; etc - multiticks
# S; - short press, main knob
# L; - long press, main knob
# C; - fast double click, main knob

# The fast knob codes reflect multiple encoder ticks between USB polling times,
# so the knob should be able to keep track of fast spinning.

# XnS; - normal press, key n=1,2,3
# XnL; - long press
# XnC; - fast double click
# e.g. 
#    U; (frequency up one tick)
#    X2S; (normal press, button 2)

# Sending from host to FlexControl:
# Ixyz;  where x,y,z = 1 or 0 for LED 0, 1, 2 on or off
# e.g.
#    I001; set right hand LED on
#    I000; set all LEDs off
#    I111; set all LEDs on


class FlexControl:
    def __init__(self, port, root):
        self.root = root
        self.port = port

    def start(self):
        self.ser = serial.Serial(self.port, 9600, timeout=1)
        self.running = True
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.ser.close()

    def update_leds(self, left, middle, right):
        self.ser.write(f"I{left:d}{middle:d}{right:d};".encode())

    def run(self):
        while self.running:
            data = self.ser.read_until(b';')
            if len(data) > 0:
                Event.VirtualEventData = data.decode('utf-8')
                self.root.event_generate('<<FC>>', when='tail')


