import os
import pydub
from pydub import AudioSegment
from pydub.silence import split_on_silence
import webrtcvad


def split_audio(file_name, min_silence_len=500, silence_thresh=-40):
    file_name = "/Users/jasonjiang/PycharmProject/pythonProject5/temp.wav"
    # 加载.wav文件
    audio = AudioSegment.from_wav(file_name)

    # 使用pydub库的split_on_silence函数来断句
    chunks = split_on_silence(audio,
                              min_silence_len=min_silence_len,
                              silence_thresh=silence_thresh)

    # 存储断句后的音频文件
    for i, chunk in enumerate(chunks):
        chunk.export(f"chunk_{i}.wav", format="wav")

    return [f"chunk_{i}.wav" for i in range(len(chunks))]


# 测试
file_name = "your_audio_file.wav"
split_audio(file_name)
