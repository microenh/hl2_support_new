from serial import Serial
import threading
from tkinter import Event

class Semicolon:
    def __init__(self, root, port, baud):
        self.root = root
        self.ser = Serial(port, baud, timeout=1)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.ser.close()

    def write(self, data):
        try:
            self.ser.write(data)
        except:
            pass

    def send(self, event, data):
        Event.VirtualEventData = data
        self.root.event_generate(event, when='tail')

    def run(self):
        while self.running:
            data = self.ser.read_until(b';')
            if len(data) > 0:
                try:
                    self.process(data.decode('utf-8'))
                except:
                    pass
