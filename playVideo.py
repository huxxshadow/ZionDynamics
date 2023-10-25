# class Video(object):
#     def __init__(self,path):
#         self.path = path
#
#     def play(self):
#         from os import startfile
#         startfile(self.path)
#
# class Movie_MP4(Video):
#     type = 'MP4'
#
# movie = Movie_MP4(r'0af4fdca8d0a62772eba074344790e70.mp4')
# movie.play()

import vlc

p = vlc.MediaPlayer("test.mp3")
p.play()