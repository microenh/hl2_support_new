from Semicolon import Semicolon

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

FC_TURN = '<<FC_TURN>>'
# fc_button = '<<FC_BUTTON>>'

class FlexControl(Semicolon):

    def clearLEDs(self):
        self.leds = [False] * 3
        self.update_leds()

    def start(self):
        self.clearLEDs()
        super().start()

    def stop(self):
        self.clearLEDs()
        super().stop()

    def update_leds(self):
        self.write(f'I{self.leds[0]:d}{self.leds[1]:d}{self.leds[2]:d};'.encode())

    def process(self, data):
        match data[0]:
            case 'D'|'U':
                if len(data) > 2:
                    mult = int(data[1:-1])
                else:
                    mult = 1
                if data[0] == 'D':
                    mult = -mult
                self.send(FC_TURN, mult)

            case 'S':
                self.root.queue_quit()

            # case 'C'|'L'|'S':
            #     self.send(fc_button, ('0', data[0]))

            case 'X':
                if data[2] == 'S':
                    self.leds[i] = not self.leds[(i := int(data[1]) - 1)]
                    self.update_leds()
