import tkinter as tk
import os
from PIL import Image, ImageTk

from FlexControl import FlexControl, FC_TURN
from Thetis import Thetis, THETIS_DATA

BG_COLOR = "#3d6466"
QUIT_EVENT = '<<QUIT>>'

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.bind(FC_TURN, self.fc_turn)
        self.bind(QUIT_EVENT, lambda a: self.quit())
        self.bind(THETIS_DATA, self.thetis_data)
        self.thetis = Thetis(self, 'COM6', 115200)
        self.flexControl = FlexControl(self, 'COM7', 9600)
        self.layout()

    def  layout(self):
        # self.title("FC")
        # self.geometry('150x112')
        frame = tk.Frame(self, bg=BG_COLOR)
        frame.pack(expand=True, fill='both')
        logo = os.path.join(os.path.dirname(__file__), "flex_control.png")
        self.image=ImageTk.PhotoImage(Image.open(logo))        
        tk.Label(frame, image=self.image, bg=BG_COLOR).pack()

    def queue_quit(self):
        self.event_generate(QUIT_EVENT, when='tail')

    def fc_turn(self, e):
        self.thetis.turn(e.VirtualEventData)

    def thetis_data(self, e):
        name, value = e.VirtualEventData
        # print(f'{name} = {value}')
 
    def heartbeat(self):
        # self.thetis.heartbeat()
        self.after(100, self.heartbeat)

    def run(self):
        self.thetis.start()
        self.flexControl.start()
        # self.after_idle(self.heartbeat)
        self.mainloop()
        self.thetis.stop()
        self.flexControl.stop()
        self.destroy()


if __name__ == '__main__':
    MainWindow().run()