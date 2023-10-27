import threading
import vlc
from threading import Thread

class keepPlayingV(Thread):
    signal = 0

    # creating Instance class object
    player = vlc.Instance()

    # creating a new media list
    media_list = player.media_list_new()

    # creating a media player object
    media_player = player.media_list_player_new()

    # creating a new media - todo: media list
    MainMedia = player.media_new("C:\\Users\\Hp User\\Desktop\\test1.mp4")
    smile = player.media_new("...")

    # adding media to media list
    media_list.add_media(MainMedia)

    # setting media list to the mediaplayer
    media_player.set_media_list(media_list)

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
        # p = vlc.MediaPlayer("C:\\Users\\Hp User\\Desktop\\test1.mp4")
        # setting loop
        self.media_player.vlm_set_loop("mainLoop", True)
        self.player.play()

    def playOnce(self, signal):
        path = self.switch(signal)
        # p = vlc.MediaPlayer(path)
        # self.player.play()
        # p.play()
        # playing the media
        
        self.player.vlm_play_media("death_note")

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
