from serial import Serial
import threading
from tkinter import Event
from telnetlib import Telnet
from eventID import EVENT


class Semicolon:
    lock = threading.Lock()
    def __init__(self, root, port, baud):
        self.root = root
        self.port = port
        try:
            if port[:3] == 'COM':
                self.ser = Serial(port, baud, timeout=None, write_timeout=1)
            else:
                self.ser = Telnet(port, baud)
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

    def send(self, data):
        with self.lock:
            Event.VirtualEventData = data
            self.root.event_generate(EVENT, when='tail')

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

if __name__ == '__main__':
    from main import main
    main()
