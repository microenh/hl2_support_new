import tkinter as tk
from FlexControl import FlexControl, fc_turn_event, fc_button_event
from Thetis import Thetis, thetis_freq_event, thetis_step_event
import os
from PIL import Image, ImageTk

BG_COLOR = "#3d6466"

def run():

    leds = [False] * 3
    run.frequency = 100
    run.step = 1

    def update():
        thetis.check_alive(1)
        thetis.query()
        window.after(100, update)

    def updateLEDs():
        flexControl.update_leds(*leds)

    def on_thetis_freq(e):
        run.frequency = e.VirtualEventData

    def on_thetis_step(e):
        run.step = e.VirtualEventData
    
    def on_fc_turn(e):
        mult = e.VirtualEventData
        run.frequency = (run.frequency // run.step) * run.step
        freq = run.frequency + mult * run.step
        freq = min(max(freq, 100), 30_000_000)
        thetis.setVFOA(freq)

    def on_fc_button(e):
        button, press = e.VirtualEventData
        if press == 'S':
            match (button):
                case '0':
                    window.quit()
                case '1'|'2'|'3':
                    which = int(button) - 1
                    leds[which] = not leds[which]
                    updateLEDs()
        
    window = tk.Tk()

    window.bind(fc_turn_event, on_fc_turn)
    window.bind(fc_button_event, on_fc_button)

    window.bind(thetis_freq_event, on_thetis_freq)
    window.bind(thetis_step_event, on_thetis_step)

    thetis = Thetis(window, 'COM6', 115200)
    flexControl = FlexControl(window, 'COM7', 9600)

    window.protocol('WM_DELETE_WINDOW', window.quit)
    # window.title("FC")
    # window.geometry('150x112')
    frame = tk.Frame(window, bg=BG_COLOR)
    frame.pack(expand=True, fill='both')
    logo = os.path.join(os.path.dirname(__file__), "flex_control.png")
    image=ImageTk.PhotoImage(Image.open(logo))        
    tk.Label(frame, image=image, bg=BG_COLOR).pack()

    thetis.start()
    flexControl.start()
    updateLEDs()
    window.after_idle(update)
    window.mainloop()
    leds[0] = leds[1] = leds[2] = False
    updateLEDs()
    thetis.stop()
    flexControl.stop()
    window.destroy()


if __name__ == '__main__':
    run()