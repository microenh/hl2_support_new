import tkinter as tk
from FlexControl import FlexControl
from Thetis import Thetis

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
    window.title("FlexControl Interface")
    window.protocol('WM_DELETE_WINDOW', on_closing)
    window.geometry('320x240')

    thetis.start()
    flexControl.start()
    window.after_idle(update)
    window.mainloop()


if __name__ == '__main__':
    run()