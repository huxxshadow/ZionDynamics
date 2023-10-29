# importing vlc module
import vlc

# importing time module
import time

# signal = "test3"


instance = vlc.Instance()

player=instance.media_player_new()
player.set_fullscreen(True)
player.video_set_scale(1)
media_list = instance.media_list_new()

player_list = instance.media_list_player_new()
player_list.set_media_player(player)

media = instance.media_new_path("微笑.mp4")

media_list.add_media(media)
# vlc.Media.get_duration()
# vlc.MediaPlayer.get_length()
# vlc.MediaListPlayer.get_media_player()
# player_list.set_media_list(media_list)

# setting loop
# instance.vlm_play_media("test3")

# start playing video


player_list.set_media_list(media_list)
print(media_list.count())
player_list.play()
time.sleep(8)

media_list.add_media(instance.media_new_path("流汗.mp4"))

# player_list.set_media_list(media_list)
time.sleep(8)







# wait so the video can be played for 5 seconds
# irrespective for length of video
time.sleep(4)
# import vlc
# import time
#
# Instance = vlc.Instance()
# player = Instance.media_player_new()
#
# Media = Instance.media_new('微笑.mp4')
# player.set_media(Media)
#
# player.play()
# time.sleep(1)
#
# player.set_fullscreen(True)