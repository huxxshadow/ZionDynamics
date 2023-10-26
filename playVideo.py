import threading
import vlc
from threading import Thread

class keepPlayingV(Thread):
    signal = 0

    def __init__(self, name, signal):
        super().__init__()
        self.name = name
        self.signal = signal

    def run(self):
        if self.signal == 0:
            self.playRepeatedly()
        else:
            self.playOnce(self.signal)

    def playRepeatedly(self):
        # main video
        p = vlc.MediaPlayer("C:\\Users\\Hp User\\Desktop\\test1.mp4")
        while True:
            p.play()

    def playOnce(self, signal):
        path = self.switch(signal)
        p = vlc.MediaPlayer(path)
        p.play()

    def switch(self, signal):
        if signal == 1:
            return "C:\\Users\\Hp User\\Desktop\\test2.mp4"
        elif signal == 2:
            return "C:\\Users\\Hp User\\Desktop\\test3.mp4"


t1 = threading.Thread()
t1.start()
t1.join()
t2 = threading.Thread(args=(1),)
t2.start()
t1.join()
