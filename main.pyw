#! c:/Users/mark/Developer/Python/hl2_support_new/.venv/Scripts/pythonw.exe
import tkinter as tk
import os
from PIL import Image, ImageTk
from eventID import ThetisEvent, EVENT
from FlexControl import FlexControl
from Thetis import Thetis

BG_COLOR = "#3d6466"

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.data = [None] * (len(ThetisEvent) + 1)
        self.protocol('WM_DELETE_WINDOW', self.quit)
        self.bind(EVENT, self.do_event)
        self.thetis = Thetis(self, 'localhost', 13013)
        # self.thetis = Thetis(self, 'COM6', 115_200)
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


    def data_changed(self, key, value):
        if result := self.data[key] != value:
            self.data[key] = value
        return result

    def do_event(self, e):
        try:
            name, value = e.VirtualEventData
            match name:
                case ThetisEvent.FREQA.value:
                    if self.data_changed(name, value):
                        self.freqa.set(f'{value:,}')
                case ThetisEvent.STEP.value:
                    if self.data_changed(name, value):
                        self.step.set(f'{value:,}')
                case ThetisEvent.TURN.value:
                    self.thetis.turn(value)
                case ThetisEvent.BUTTON.value:
                    if value[1] == 'S':
                        match m := int(value[0]):
                            case 0:
                                self.quit()
                            case 1|2|3:
                                self.flexControl.updateButton(m-1)
                case ThetisEvent.QUIT.value:
                    self.quit()
            # print(f'{name} = {value}')
        except Exception as e:
            pass
##            print (e)
##            print (f'exc e.VirtualEventData: {e.VirtualEventData}')
 
    def heartbeat(self):
        self.thetis.heartbeat()
        self.after(1000, self.heartbeat)

    def run(self):
        self.thetis.start()
        self.flexControl.start()
        self.after_idle(self.heartbeat)
        self.after_idle(lambda: self.eval("tk::PlaceWindow . center"))
        self.mainloop()
        self.thetis.stop()
        self.flexControl.stop()
        self.destroy()


def main():
    MainWindow().run()

if __name__ == '__main__':
    main()
