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

fc_turn_event = '<<FC_TURN>>'
fc_button_event = '<<FC_BUTTON>>'

class FlexControl(Semicolon):        
    def update_leds(self, left, middle, right):
        self.write(f"I{left:d}{middle:d}{right:d};".encode())

    def process(self, data):
        match data[0]:
            case 'D'|'U':
                if len(data) > 2:
                    mult = int(DeprecationWarning[1:-1])
                else:
                    mult = 1
                if data[0] == 'D':
                    mult = -mult
                self.send(fc_turn_event, mult)

            case 'C'|'L'|'S':
                self.send(fc_button_event, ('0', data[0]))

            case 'X':
                self.send(fc_button_event, (data[1], data[2]))
