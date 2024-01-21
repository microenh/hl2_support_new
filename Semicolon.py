import serial
import threading
from tkinter import Event


class Semicolon:
    def __init__(self, root, port):
        self.root = root
        self.port = port

    def start(self):
        self.ser = serial.Serial(self.port, self.baud(), timeout=1)
        self.running = True
        self.thread = threading.Thread(target=self.run)
        # self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        self.ser.close()

    def run(self):
        while self.running:
            data = self.ser.read_until(b';')
            if len(data) > 0:
                Event.VirtualEventData = data.decode('utf-8')
                self.root.event_generate(self.event(), when='tail')