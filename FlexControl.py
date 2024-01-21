import serial
import threading


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
    def __init__(self, port, onTurn, doQuit):

        self.onTurn = onTurn
        self.doQuit = doQuit

        self._leftLED = False
        self._middleLED = False
        self._rightLED = False

        self._ser = serial.Serial(port, 9600, timeout=1)
        self._update_leds_()

    def start(self):
        self._running = True
        self._thread = threading.Thread(target = self.run)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._leftLED = self._middleLED = self._rightLED = False
        self._update_leds_()
        self._running = False
        try:
            self._thread.join()
        except:
            pass
        self._ser.close()

    def _update_leds_(self):
        try:
            self._ser.write(("I%d%d%d;" % (self._leftLED, self._middleLED, self._rightLED)).encode())
        except:
            pass

    @property
    def leftLED(self):
        return self._leftLED

    @leftLED.setter
    def leftLED(self, value):
        self._leftLED = value
        self._update_leds_()

    @property
    def middleLED(self):
        return self._middleLED

    @middleLED.setter
    def middleLED(self, value):
        self._middleLED = value
        self._update_leds_()

    @property
    def rightLED(self):
        return self._rightLED

    @rightLED.setter
    def rightLED(self, value):
        self._rightLED = value
        self._update_leds_()

    def run(self):
        while self._running:
            data = self._ser.read_until(b';')
            if len(data) > 0:
                self._handle_line(data.decode())

    def _click(self):
        self.doQuit()

    def _press(self):
        pass

    def _double(self):
        pass

    def _turn(self, mult):
        self.onTurn(mult)

    def _leftClick(self):
        self.leftLED = not self._leftLED

    def _leftPress(self):
        pass

    def _leftDouble(self):
        pass

    def _middleClick(self):
        self.middleLED = not self._middleLED

    def _middlePress(self):
        pass

    def _middleDouble(self):
        pass

    def _rightClick(self):
        self.rightLED = not self._rightLED

    def _rightPress(self):
        pass

    def _rightDouble(self):
        pass


    def _handle_line(self, data):
        d = str(data)
        match d[0]:
            case 'S':
                self._click()
            case 'L':
                self._press()
            case 'C':
                self._double()
            case 'D'|'U':
                if len(d) > 2:
                    mult = int(d[1:-1])
                else:
                    mult = 1
                if d[0] == 'D':
                    mult = -mult
                self._turn(mult)

            case 'X':
                match d[1]:
                    case '1':
                        match d[2]:
                            case 'S':
                                self._leftClick()
                            case 'L':
                                self._leftPress()
                            case 'C':
                                self._leftDouble()
                    case '2':
                        match d[2]:
                            case 'S':
                                self._middleClick()
                            case 'L':
                                self._middlePress()
                            case 'C':
                                self._middleDouble()
                    case '3':
                        match d[2]:
                            case 'S':
                                self._rightClick()
                            case 'L':
                                self._rightPress()
                            case 'C':
                                self._rightDouble()
