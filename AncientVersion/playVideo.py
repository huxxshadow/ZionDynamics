global signal

# importing vlc module
import vlc
from threading import Thread
import time


class keepPlayingV(Thread):

    def __init__(self):
        super().__init__()
        # self.name = name

    def run(self):
        if (signal == 0):
            self.playRepeatedly()
        else:
            self.playOnce(signal)

    def playRepeatedly(self):
        # importing vlc module
        import vlc

        # importing time module
        import time

        # creating Instance class object
        player = vlc.Instance()

        # creating a new media list
        media_list = player.media_list_new()

        # creating a media player object
        media_player = player.media_list_player_new()

        # creating a new media
        media = player.media_new("C:\\Users\\Hp User\\Desktop\\test2.mp4")

        # adding media to media list
        media_list.add_media(media)

        # setting media list to the mediaplayer
        media_player.set_media_list(media_list)

        # setting loop
        player.vlm_set_loop("test2", True)

        # start playing video
        while True:
            media_player.play()
            time.sleep(5)  # I don't know why this is needed, my program doesn't work without it

    def playOnce(self, signal):
        # importing vlc module
        import vlc

        # importing time module
        import time

        # creating Instance class object
        player = vlc.Instance()

        # creating a new media list
        media_list = player.media_list_new()

        # creating a media player object
        media_player = player.media_list_player_new()

        # creating a new media
        media = player.media_new("C:\\Users\\Hp User\\Desktop\\"+ signal + ".mp4")

        # adding media to media list
        media_list.add_media(media)

        # setting media list to the mediaplayer
        media_player.set_media_list(media_list)

        # setting loop
        player.vlm_play_media("test3")
        # p = subprocess.Popen('vlc', 'home/pi/demo.mp3', '--loop')

        # start playing video
        media_player.play()

        # wait so the video can be played for 5 seconds
        # irrespective for length of video
        time.sleep(4)

