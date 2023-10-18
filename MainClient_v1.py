import asyncio
import os
import time
import wave

import sherpa_ncnn
import sys
import sounddevice as sd
import soundfile as sf
from gtts import gTTS
import pygame
import socket
import threading

code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.mp3")
STRING_SPECIFIER = "2222"
WAV_SPECIFIER = "3333"
exit = False

now: time.time()



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
    samples_per_read = int(3 * sample_rate)  # 0.1 second = 100 ms
    global last_result
    last_result = ""
    return recognizer, sample_rate, samples_per_read


def sound_echo(recognizer, sample_rate, samples_per_read):
    global last_result
    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        samples, _ = s.read(samples_per_read)  # a blocking read
        samples = samples.reshape(-1)
        recognizer.accept_waveform(sample_rate, samples)
        result = recognizer.text
        # if last_result != result:
        #     last_result = result
        #     print("\r{}".format(result), end="", flush=True)
        return result


def receiveMsg():
    totalData = bytes()
    while True:
        data = sock.recv(1024)
        totalData += data
        if len(data) < 1024:
            break
    return totalData


def getData():
    specifier = str(receiveMsg(), encoding="utf-8")
    if specifier == STRING_SPECIFIER:
        receivedStr = str(receiveMsg(), encoding="utf-8")
        print(receivedStr)
        return receivedStr

    elif specifier == WAV_SPECIFIER:
        data = receiveMsg()
        ww = wave.open('received.wav', 'wb')
        ww.writeframes(data)
        ww.close()
def play_wav(file_path):
    data,fs=sf.read(file_path)
    sd.play(data,fs)
    event.clear()
    sd.wait()
    event.set()

def processMsg():
    global last_result,length_last
    event.clear()
    temp=last_result[length_last:len(last_result)]
    length_last=len(last_result)
    event.set()
    return "voiceInput:"+temp

def sendString(msg):
    sock.sendall(STRING_SPECIFIER)
    if len(msg) % 1024 == 0:
        msg = msg + " "
    sock.sendall(bytes(msg, encoding="utf-8"))

def keepMonitor():
    global last_result
    print("Started! Please speak")
    recognizer = create_recognizer()
    sample_rate = recognizer.sample_rate
    samples_per_read = int(3 * sample_rate)  # 0.1 second = 100 ms
    last_result = ""
    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while not exit:
            event.wait()
            samples, _ = s.read(samples_per_read)  # a blocking read
            samples = samples.reshape(-1)
            recognizer.accept_waveform(sample_rate, samples)
            result = recognizer.text
            if last_result != result:
                last_result = result
                print("\r{}".format(result), end="", flush=True)


def keepReceiveMsg():
    while not exit:
        msg = getData()
        play_wav("received.wav")
        input_Msg = processMsg()
        sendString(input_Msg)
        # processedMsg = handleMsg(msg)
        # TTS(processedMsg)
        # sendMsg(processedMsg)


if __name__ == '__main__':
    sock = socket.socket()
    sock.connect(('192.168.137.203', 9006))
    event=threading.Event()

    tMonitor = threading.Thread(target=keepMonitor, name="Monitor")
    tRec = threading.Thread(target=keepReceiveMsg(), name="Receive_Msg")
    # tSend = threading.Thread(target=mainSendMsg(), name="MainSendMsg")

    tRec.start()
    # tSend.start()
    tRec.join()

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
