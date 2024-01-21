import tkinter as tk
from FlexControl import FlexControl
from Thetis import Thetis
import os
from PIL import Image, ImageTk

def run():
    step_value = (1,2,10,25,50,100,250,500,1_000,2_000,2_500,5_000,6_250,9_000,10_000,12_500,
        15_000,20_000,25_000,30_000,50_000,100_000,250_000,500_000,1_000_000,10_000_000)

    leds = [False] * 3
    run.frequency = 0
    run.step = 0

    def update():
        thetis.query()
        window.after(100, update)

    def updateLEDs():
        flexControl.update_leds(*leds)

    def on_fc(e):
        d = e.VirtualEventData
        match d[0]:
            case 'S':
                window.quit()
            # case 'L':
            #     pass
            # case 'C':
            #     pass
            case 'D'|'U':
                if len(d) > 2:
                    mult = int(d[1:-1])
                else:
                    mult = 1
                if d[0] == 'D':
                    mult = -mult
                turn(mult)

            case 'X':
                ledNo = None
                match d[2]:
                    case 'S':
                        ledNo = None
                        match d[1]:
                            case '1'|'2'|'3':
                                ledNo = int(d[1]) - 1
                                leds[ledNo] = not leds[ledNo]
                                updateLEDs()
                    # case 'L':
                    #     pass
                    # case 'C':
                    #     pass

    def on_thetis(e):
        d = e.VirtualEventData
        if d[:4] == 'ZZFA':
            run.frequency = int(d[4:15])
        elif d[:4] == 'ZZAC':
            run.step = int(d[4:6])
    
    def turn(mult):
        step_inc = step_value[run.step]
        run.frequency = (run.frequency // step_inc) * step_inc
        freq = run.frequency + mult * step_inc
        freq = min(max(freq, 100), 30_000_000)
        thetis.setVFOA(freq)


    window = tk.Tk()
    window.bind('<<FC>>', on_fc)
    window.bind('<<THETIS>>', on_thetis)
    thetis = Thetis(window, 'COM6')
    flexControl = FlexControl(window, 'COM7')
    # window.title("FC")
    window.protocol('WM_DELETE_WINDOW', window.quit)
    # window.geometry('150x112')
    frame = tk.Frame(window)
    frame.pack(expand=True, fill='both')
    logo = os.path.join(os.path.dirname(__file__), "flex_control.png")
    image=ImageTk.PhotoImage(Image.open(logo))        
    tk.Label(frame, image=image).pack()

    thetis.start()
    flexControl.start()
    updateLEDs()
    window.after_idle(update)
    window.mainloop()
    leds[0] = leds[1] = leds[2] = False
    updateLEDs()
    thetis.stop()
    flexControl.stop()


if __name__ == '__main__':
    run()