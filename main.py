import tkinter as tk
from FlexControl import FlexControl
from Thetis import Thetis
import os
from PIL import Image, ImageTk

def run():
    def update():
        thetis.query()
        window.after(100, update)

    def on_closing():
        thetis.stop()
        flexControl.stop()
        window.quit()


    thetis = Thetis('COM6')
    flexControl = FlexControl('COM7', thetis.onTurn, on_closing)
    window = tk.Tk()
    # window.title("FC")
    window.protocol('WM_DELETE_WINDOW', on_closing)
    # window.geometry('150x112')
    frame = tk.Frame(window)
    frame.pack(expand=True, fill='both')
    logo = os.path.join(os.path.dirname(__file__), "flex_control.png")
    image=ImageTk.PhotoImage(Image.open(logo))        
    tk.Label(frame, image=image).pack()

    thetis.start()
    flexControl.start()
    window.after_idle(update)
    window.mainloop()


if __name__ == '__main__':
    run()