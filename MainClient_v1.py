# import asyncio
# import io
import os
import time
# import wave

# import numpy as np
import sherpa_ncnn
# import sys
import sounddevice as sd

import soundfile as sf
# from gtts import gTTS

# import pygame
import socket
from threading import Thread
import threading
# import struct
# import pickle
# import logging
# import base64
# from config_ import record_filler_len, data_package_size

code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.mp3")
STRING_SPECIFIER = "2222"
WAV_SPECIFIER = "3333"
exit = False

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


def soundInput_initial():
    devices = sd.query_devices()
    print(devices)
    default_input_device_idx = sd.default.device[0]
    print(f'Use default device: {devices[default_input_device_idx]["name"]}')
    recognizer = create_recognizer()
    sample_rate = recognizer.sample_rate
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
    global last_result
    last_result = ""
    return recognizer, sample_rate, samples_per_read


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


def receiveMsg():
    totalData = bytes()
    totallen=int.from_bytes(sock.recv(1024), byteorder='little')
    # sock.settimeout(5)
    while totallen!=0:
        # try:
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


# def write_package_to_file(writer, data_package):
#     # 将1024个字节 base64编码数据解码为 768个字节utf8数据
#     recv_data = base64.b64decode(data_package)
#     logger.debug(f"接收的数据为: {recv_data}")
#     logger.debug(f"接收的数据长度为: {len(recv_data)}")
#
#     # 字节流读取数据
#     recv_data_stream = io.BytesIO(recv_data)
#     # 返回一个对应于缓冲区内容的可读写视图而不必拷贝其数据
#     recv_data_stream = recv_data_stream.getvalue()
#
#     # 获取填充字符的长度和记录填充字符所占用的长度 根据字节截取想要的数据
#     fill_char_len = recv_data_stream[-record_filler_len:].decode()
#     cut_len = int(fill_char_len) + record_filler_len
#     recv_real_data = recv_data[:-cut_len]
#     # 返回数据包的字节数据
#     writer.write(recv_real_data)


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

    with open('received.wav', 'wb') as file:
        data = receiveMsg()
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






def play_wav(file_path):
    data, fs = sf.read(file_path)
    event.clear()
    print(fs)
    print("时间开始流动")
    sd.play(data, fs)
    sd.wait()
    event.set()
    print("时间流动结束")


def processMsg():
    global last_result, length_last
    event.clear()
    if len(last_result)-length_last<3:
        event.set()
        return "voiceInput:"

    temp = last_result[length_last:len(last_result)]
    length_last = len(last_result)
    event.set()
    print("This is the processMsg() stage")
    return "voiceInput:" + temp


def sendString(msg):
    print("this is the send message: " + msg)
    sock.sendall(bytes(STRING_SPECIFIER, encoding="utf-8"))
    time.sleep(0.1)
    if len(msg) % 1024 == 0:
        msg = msg + " "
    sock.sendall(bytes(msg, encoding="utf-8"))



class keepMonitor(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        global last_result
        print("Started! Please speak")
        recognizer = create_recognizer()
        sample_rate = recognizer.sample_rate
        samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
        last_result = ""
        with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
            event.set()
            while not exit:
                event.wait()
                if(len(last_result)>500):
                    last_result=last_result[10:len(last_result)]

                samples, _ = s.read(samples_per_read)  # a blocking read
                samples = samples.reshape(-1)
                recognizer.accept_waveform(sample_rate, samples)
                result = recognizer.text
                if last_result != result:
                    last_result = result
                    # print("\r{}".format(result), end="", flush=True)


class keepReceiveMsg(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        event.wait()  # wait for the monitor to initialize
        while not exit:
            input_Msg = processMsg()
            if input_Msg == "voiceInput:":
                continue
            print("receive kazhu difang 1")
            sendString(input_Msg)
            time.sleep(0.05)
            print("receive kazhu difang 2")
            msg = getData()
            print("receive kazhu difang 3")
            play_wav("received.wav")
            print("sssssssssssssss")
            # time.sleep(4)
            # processedMsg = handleMsg(msg)
            # TTS(processedMsg)
            # sendMsg(processedMsg)
            # time.sleep(5)
            # print("the sleep 5s hou")


global last_result, length_last
length_last = 0
last_result = ""

# print(sd.query_devices())
# sd.default.device[1] = 4

sock = socket.socket()
sock.connect(('172.28.165.132', 9008))
event=threading.Event()
event.clear()
tMonitor = keepMonitor("Monitor")
tRec = keepReceiveMsg("Receive_Msg")


# tSend = threading.Thread(target=mainSendMsg(), name="MainSendMsg")
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
