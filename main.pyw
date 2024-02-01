#! c:/Users/mark/Developer/Python/hl2_support_new/.venv/Scripts/pythonw.exe
import tkinter as tk
import os
from PIL import Image, ImageTk
import eventID
from FlexControl import FlexControl
from Thetis import Thetis

BG_COLOR = "#3d6466"

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.bind(eventID.EVENT, self.do_event)
        self.thetis = Thetis(self, 'localhost', 13013)
        self.flexControl = FlexControl(self, 'COM12', 9600)
        self.layout()
        self.iconphoto(False, self.image)

    def  layout(self):
        self.title("FlexControl")
        # self.geometry('250x112')
        logo = os.path.join(os.path.dirname(__file__), "flex_control.png")
        i = Image.open(logo)
        w,h = i.size
        w //= 4
        h //= 4
        self.image = ImageTk.PhotoImage(i.resize((w,h)))
        
        frame = tk.Frame(self, bg=BG_COLOR)
        frame.grid()
        tk.Label(frame, image=self.image, bg=BG_COLOR).grid(row=0, column=0, columnspan=2)
        tk.Label(frame, text='VFO A:', bg=BG_COLOR).grid(row=1, column=0, sticky='W')
        tk.Label(frame, text='Step:', bg=BG_COLOR).grid(row=2, column=0, sticky='W')
        self.freqa = tk.StringVar()
        tk.Label(frame, textvariable=self.freqa, bg=BG_COLOR).grid(row=1, column=1, sticky='E')
        self.step = tk.StringVar()
        tk.Label(frame, textvariable=self.step, bg=BG_COLOR).grid(row=2, column=1, sticky='E')

    def do_event(self, e):
        try:
            name, value = e.VirtualEventData
            match name:
                case eventID.FREQA:
                    self.freqa.set(f'{value:,}')
                case eventID.STEP:
                    self.step.set(f'{value:,}')
                case eventID.TURN:
                    self.thetis.turn(value)
                case eventID.BUTTON:
                    if value[1] == 'S':
                        match m := int(value[0]):
                            case 0:
                                self.quit()
                            case 1|2|3:
                                self.flexControl.updateButton(m-1)
                case eventID.QUIT:
                    self.quit()
            # print(f'{name} = {value}')
        except Exception as e:
            pass
##            print (e)
##            print (f'exc e.VirtualEventData: {e.VirtualEventData}')
 
    def heartbeat(self):
        self.thetis.heartbeat()
        self.after(100, self.heartbeat)

    def run(self):
        self.thetis.start()
        self.flexControl.start()
        self.after_idle(self.heartbeat)
        self.after_idle(lambda: self.eval("tk::PlaceWindow . center"))
        # self.after_idle(lambda: self.iconphoto(False, self.image))
        self.mainloop()
        self.thetis.stop()
        self.flexControl.stop()
        self.destroy()


def main():
    MainWindow().run()

if __name__ == '__main__':
    main()
