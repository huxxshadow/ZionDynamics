# import asyncio
# import io
import os
import time
# import wave

# import numpy as np
import sherpa_ncnn
# import sys
import sounddevice as sd
# import Adafruit_DHT
import soundfile as sf
# from gtts import gTTS

# import pygame
import socket
from threading import Thread
import threading

from pydub import AudioSegment

import vlc

# import struct
# import pickle
# import logging
# import base64
# from config_ import record_filler_len, data_package_size
global signal
global skip
skip=False
signal = ""

# experissonIdle={"静态1":"./expressions/ ","静态2":" ","静态3":" "}
experissonTime={"微笑":4.002,"流汗":1.767,"哭哭":1.106,"生气":1.875,"眨眼":1.667}


code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.mp3")
STRING_SPECIFIER = "2222"
WAV_SPECIFIER = "3333"
exit = False

makerobo_pin = 17
global humidity,temperature,control_1
humidity=0
temperature=0
control_1=0

# def makerobo_setup():
# 	global sensor
# 	sensor = Adafruit_DHT.DHT11

# logging.basicConfig(format='[%(name)s] %(levelname)s: %(message)s', level=logging.INFO)
# logger = logging.getLogger("客户端")


# def TTS(response, start_time):
#     tts = gTTS(text=response, lang='en')  # 英文 "en", 普通话 "zh-CN", 粤语 "zh-yue", 日语 "ja"
#     if os.path.exists(mp3_path):
#         os.remove(mp3_path)
#     tts.save(mp3_path)

# running_time2 = time.time() - start_time
# print("TTS running time:", running_time2, "seconds")


# def play_mp3(file_path):
#     pygame.init()
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play()
#     # running_time2 = time.time() - start_time
#     # print("play_mp3 running time:", running_time2, "seconds")
#     while pygame.mixer.music.get_busy():
#         continue
#
#     pygame.mixer.music.stop()
#     pygame.mixer.quit()
#     pygame.quit()


def create_recognizer():
    # Please replace the model files if needed.
    # See https://k2-fsa.github.io/sherpa/ncnn/pretrained_models/index.html
    # for download links.
    recognizer = sherpa_ncnn.Recognizer(
        tokens="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/tokens.txt",
        encoder_param="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/encoder_jit_trace-pnnx.ncnn.param",
        encoder_bin="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/encoder_jit_trace-pnnx.ncnn.bin",
        decoder_param="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/decoder_jit_trace-pnnx.ncnn.param",
        decoder_bin="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/decoder_jit_trace-pnnx.ncnn.bin",
        joiner_param="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/joiner_jit_trace-pnnx.ncnn.param",
        joiner_bin="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/joiner_jit_trace-pnnx.ncnn.bin",
        num_threads=4,
    )
    return recognizer


# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection("192.168.137.1", 9006)
#     print(f'Send to server: {message!r}')
#
#     writer.write(message.encode())
#     await writer.drain()
#
#     data = await reader.read(200)
#     output = data.decode()
#
#     print(f'Received from server: {output!r}')
#     TTS(output.split(":", 1)[1], 0)
#     play_mp3(mp3_path)
#     writer.close()
#     await writer.wait_closed()


# def soundInput_initial():
#     devices = sd.query_devices()
#     print(devices)
#     default_input_device_idx = sd.default.device[0]
#     print(f'Use default device: {devices[default_input_device_idx]["name"]}')
#     recognizer = create_recognizer()
#     sample_rate = recognizer.sample_rate
#     samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
#     global last_result
#     last_result = ""
#     return recognizer, sample_rate, samples_per_read


# def sound_echo(recognizer, sample_rate, samples_per_read):
#     global last_result
#     with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
#         samples, _ = s.read(samples_per_read)  # a blocking read
#         samples = samples.reshape(-1)
#         recognizer.accept_waveform(sample_rate, samples)
#         result = recognizer.text
#         # if last_result != result:
#         #     last_result = result
#         #     print("\r{}".format(result), end="", flush=True)
#         return result


def receiveLongMsg():
    totalData = bytes()
    totallen=int.from_bytes(sock.recv(4), byteorder='little')
    # sock.settimeout(5)
    while totallen!=0:
        # try:
            if totallen<0:
                totalData=bytes()
                break
            data = sock.recv(1024)
            # print(len(data))
            totallen-=len(data)
            # if not data:
            #     break
            totalData += data
            # if len(data) < 1024:
            #     break
        # except socket.timeout:
        #     # Handle timeout by retransmitting the lost package
        #     sock.send(b'RETRANSMIT')
    print(len(totalData))
    return totalData

def receiveShortMsg(len):
    data = sock.recv(len)
    return data

# def receiveWAV(path):
#     with open(path, "wb") as wf:
#         while True:
#             data_package = sock.recv(data_package_size)
#             write_package_to_file(wf, data_package)
#             # 文件传输结束
#             if not data_package:
#                 logger.info(f"{path} 下载完成！！")
#                 break


def getData():
    print("********************************************************")
    global signal
    temp=receiveShortMsg(6).decode(encoding="utf-8")
    if temp!="nu":
        if temp in experissonTime.keys():
            signal=temp
        else:
            signal=""
    print(signal)
    # specifier = str(receiveMsg(), encoding="utf-8")
    # print("receive the specifier: " + specifier)
    # # if specifier == STRING_SPECIFIER:
    # #     receivedStr = str(receiveMsg(), encoding="utf-8")
    # #     print(receivedStr)
    # #     return receivedStr
    #
    # if specifier == WAV_SPECIFIER:
        # array with parameters

        # ww = wave.open('received.wav', 'wb')
        # ww.setnchannels(1)
        # ww.setsampwidth(2)
        # songData = str(receiveMsg().decode('utf-8'))
        # songData = songData.split()
        # framerate = songData[0]
        # ww.setframerate(int(framerate))
        # ww.setnframes(int(songData[1]))
        # songs = receiveMsg()
        # ww.writeframes(songs)
        # ww.close()
        # print("received wav file")

    with open('received.mp3', 'wb') as file:
        data = receiveLongMsg()
        if len(data)==0:
            global skip
            skip=True;
            return
        file.write(data)
        print("This is the write wav stage.")
            # print(data)
        # sf.write('received.wav', np.frombuffer(literal_eval(str(receiveMsg(), encoding='utf-8')), samplerate=44100))
        # rate = pickle.loads(receiveMsg())
        # print(rate)
        # re1 = receiveMsg()
        # print(re1)
        # print(str(len(re1)))
        # data = pickle.loads(re1)
        # soundfile.write('received.wav', data,  samplerate=rate)
    # receiveWAV('received.wav')

def mp3_to_wav(mp3_path):
    sound = AudioSegment.from_mp3(mp3_path)
    print(sound.frame_rate)
    sound.export("received.wav", format="wav")




def play_wav(file_path):
    data, fs = sf.read(file_path)

    print(fs)
    print("时间开始流动")
    sd.play(data, fs)
    sd.wait()
    event.set()
    print("时间流动结束")


def processMsg():
    global last_result, length_last
    event.clear()
    if len(last_result)-length_last<6:
        event.set()
        time.sleep(2)
        return "voiceInput:"

    temp = last_result[length_last:len(last_result)]
    length_last = len(last_result)
    event.set()
    print("This is the processMsg() stage")
    return "voiceInput:" + temp


def sendString(msg):
    print("this is the send message: " + msg)
    # sock.sendall(bytes(STRING_SPECIFIER, encoding="utf-8"))
    # time.sleep(0.1)
    global control_1
    if control_1==1:
        control_1==0;
        msg+="\nhumidityInput:"+str(humidity)+";"+str(temperature)
    # if len(msg) % 1024 == 0:
    #     msg = msg + " "
    sock.sendall(bytes(msg, encoding="utf-8"))

# def getHumiture(num):
#     if num%2==0:
#         global humidity,temperature,control_1
#         humidity, temperature = Adafruit_DHT.read_retry(sensor, makerobo_pin)
#         control_1=1

class keepMonitor(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        global last_result
        print("Started! Please speak")
        devices = sd.query_devices()
        print(devices)
        sd.default.device[1] = 0
        # sd.default.device[0] = 0
        sd.default.samplerate = 16000
        # sd.default.channels = 1, 2
        default_input_device_idx = sd.default.device[0]

        print(f'Use default device: {devices[default_input_device_idx]["name"]}')

        recognizer = create_recognizer()
        sample_rate = recognizer.sample_rate
        samples_per_read = int(0.3 * sample_rate)  # 0.1 second = 100 ms
        last_result = ""
        with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
            event.set()

            while not exit:
                if not event.is_set():
                    s.stop()
                event.wait()
                s.start()
                if(len(last_result)>500):
                    last_result=last_result[10:len(last_result)]

                event.wait()
                samples, _ = s.read(samples_per_read)  # a blocking read
                samples = samples.reshape(-1)
                if not event.is_set():
                    continue
                recognizer.accept_waveform(sample_rate, samples)
                result = recognizer.text
                if not event.is_set():
                    continue
                if last_result != result:
                    last_result = result

                    # print("\r{}".format(result), end="", flush=True)


class keepReceiveMsg(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        global skip
        makerobo_setup()
        event.wait()  # wait for the monitor to initialize
        loopNum=0;
        while not exit:
            input_Msg = processMsg()
            if input_Msg == "voiceInput:":
                continue
            print("receive kazhu difang 1")
            event.clear()
            sendString(input_Msg)
            time.sleep(0.01)
            print("receive kazhu difang 2")

            msg = getData()
            if skip:
                print("网络出错了")
                skip=False
                continue
            print("receive kazhu difang 3")
            mp3_to_wav("received.mp3")
            # time.sleep(0.1)
            play_wav("received.wav")
            print("sssssssssssssss")
            # loopNum+=1
            # getHumiture(loopNum)

class keepPlayingV(Thread):


    def __init__(self, name):
        super().__init__()
        self.name = name


    def run(self):
        global signal
        instance = vlc.Instance()
        player = instance.media_player_new()
        player.set_fullscreen(True)
        player.audio_set_mute(True)
        player.set_scale(0.85)
        media_list = instance.media_list_new()
        player_list = instance.media_list_player_new()
        player_list.set_media_player(player)
        bias=0.02
        media = instance.media_new_path("微笑.mp4")
        media_list.add_media(media)
        player_list.set_media_list(media_list)
        player_list.play()
        time.sleep(experissonTime["微笑"]-bias)
        while True:
            if signal!="":
                media = instance.media_new_path(signal+".mp4")
                media_list.add_media(media)
                time.sleep(experissonTime[signal]-bias)
                signal=""
            else:
                media = instance.media_new_path("微笑.mp4")
                media_list.add_media(media)
                time.sleep(experissonTime["微笑"]-bias)








global last_result, length_last
length_last = 0
last_result = ""

# print(sd.query_devices())
# sd.default.device[1] = 4

sock = socket.socket()
sock.connect(('172.28.187.75', 9009))
event=threading.Event()
event.clear()

tVideo=keepPlayingV("Playing_video")
tMonitor = keepMonitor("Monitor")
tRec = keepReceiveMsg("Receive_Msg")


# tSend = threading.Thread(target=mainSendMsg(), name="MainSendMsg")
tVideo.start()
tRec.start()
tMonitor.start()


# tSend.start()


# tSend.join()

# recognizer, sample_rate, samples_per_read = soundInput_initial()
#
# while True:
#     try:
#         recognizer = create_recognizer()
#         result = sound_echo(recognizer, sample_rate, samples_per_read)
#     except KeyboardInterrupt:
#         print("\nCaught Ctrl + C. Exiting")
#
#     send_msg = "voiceInput:" + result
#     asyncio.run(tcp_echo_client(send_msg))
