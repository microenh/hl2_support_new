from serial import Serial
import threading
from tkinter import Event

class Semicolon:
    lock = threading.Lock()
    def __init__(self, root, port, baud):
        self.root = root
        try:
            self.ser = Serial(port, baud, timeout=None, write_timeout=1)
        except Exception as e:
            # print(e)
            self.root.quit()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True
        self.thread.start()

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
            self.root.quit()

    def send(self, event, data):
        with Semicolon.lock:
            Event.VirtualEventData = data
            self.root.event_generate(event, when='tail')

    def run(self):
        while True:
            try:
                data = self.ser.read_until(b';')
                try:
                    self.process(data.decode('utf-8'))
                except:
                    pass
            except:
                break
