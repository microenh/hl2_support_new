from serial import Serial
import threading
from tkinter import Event
from datetime import datetime

class Semicolon:
    def __init__(self, root, port, baud):
        self.root = root
        try:
            self.ser = Serial(port, baud, timeout=None, write_timeout=1)
        except Exception as e:
            print(e)
            self.root.quit()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True
        self.thread.start()

    def check_alive(self, delta):
        if datetime.now().timestamp() - self.timestamp > delta:
            self.root.quit()

    def stop(self):
        try:
            self.ser.close()
            self.thread.join()
        except:
            pass

    def write(self, data):
        try:
            self.ser.write(data)
        except:
            pass

    def send(self, event, data):
        Event.VirtualEventData = data
        self.root.event_generate(event, when='tail')

    def run(self):
        while True:
            try:
                self.timestamp = datetime.now().timestamp()
                data = self.ser.read_until(b';')
                try:
                    self.process(data.decode('utf-8'))
                except:
                    pass
            except:
                break
