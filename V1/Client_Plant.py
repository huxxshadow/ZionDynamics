import os
import time
import sherpa_ncnn
import sounddevice as sd
import Adafruit_DHT  # for humidity and temperature sensor
import soundfile as sf
import socket
from threading import Thread
import threading
from pydub import AudioSegment
import vlc

global signal
global skip

skip = False
signal = ""

experissonTime = {"微笑": 4.002, "流汗": 1.767, "哭哭": 1.106, "生气": 1.875,
                  "眨眼": 1.667}  # the time of each expression
code_path = os.path.dirname(os.path.abspath(__file__))
exit = False

makerobo_pin = 17
global humidity, temperature, control_1
humidity = 0
temperature = 0
control_1 = 0

global last_result, length_last
length_last = 0
last_result = ""


def makerobo_setup():
    """
    Do the initial setup to the makerobo.
    :return: None
    """
    global sensor
    sensor = Adafruit_DHT.DHT11


def create_recognizer():
    """
    The function is to initialize the model file path. Please replace the model files if needed.
    :return: None
    """
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


def receiveLongMsg():
    """
    The function receive the long message from the server.
    :return: Return the total received data in bytes format
    """
    totalData = bytes()
    totallen = int.from_bytes(sock.recv(4), byteorder='little')
    while totallen != 0:
        if totallen < 0:
            totalData = bytes()
            break
        data = sock.recv(1024)
        totallen -= len(data)
        totalData += data
    print(len(totalData))
    return totalData


def receiveShortMsg(len):
    """
    The function receive the short message from the server.
    :param len: The length of the message which will be set in the sock receive buffer.
    :return: Return the data received in bytes format.
    """
    data = sock.recv(len)
    return data


def getData():
    """
    The function fet the data from the server with the specifier.
    :return: None
    """
    print("********************************************************")
    global signal
    temp = receiveShortMsg(6).decode(encoding="utf-8")

    if temp != "nu":
        if temp in experissonTime.keys():
            signal = temp
        else:
            signal = ""
    print(signal)

    with open('received.mp3', 'wb') as file:
        data = receiveLongMsg()
        if len(data) == 0:
            global skip
            skip = True;
            return
        file.write(data)
        print("This is the write wav stage.")


def mp3_to_wav(mp3_path):
    """
    The function converts the mp3 file format to the WAV file format
    :param mp3_path: The audio path of the input mp3 file.
    :return: None
    """
    sound = AudioSegment.from_mp3(mp3_path)
    print(sound.frame_rate)
    sound.export("received.wav", format="wav")


def play_wav(file_path):
    """
    The function is to play the WAV file with input file path. The process will be ended when the audio played out.
    :param file_path: The file path of the WAV file.
    :return: None
    """
    data, fs = sf.read(file_path)
    # print(fs)
    # print("时间开始流动")
    sd.play(data, fs)
    sd.wait()
    event.set()
    # print("时间流动结束")


def processMsg():
    """
    The function process the message received form the server.
    :return: The input voice input with specifier and the content in String format.
    """
    global last_result, length_last
    event.clear()
    if len(last_result) - length_last < 6:
        event.set()
        time.sleep(2)
        return "voiceInput:"
    temp = last_result[length_last:len(last_result)]  # get the voice input
    length_last = len(last_result)
    event.set()
    print("This is the processMsg() stage")
    return "voiceInput:" + temp


def sendString(msg):
    """
    The function sends the input message to the server.
    :param msg: The message input to send.
    :return: None
    """
    print("this is the send message: " + msg)
    global control_1
    if control_1 == 1:
        control_1 == 0;
        msg += "\nhumidityInput:" + str(humidity) + ";" + str(temperature)  # add the humidity and temperature
    sock.sendall(bytes(msg, encoding="utf-8"))


def getHumiture(num):
    """
    The function fet the information about the Humiture.
    :param num: The sequence number of the sensor.
    :return: None
    """
    if num % 2 == 0:
        global humidity, temperature, control_1
        humidity, temperature = Adafruit_DHT.read_retry(sensor, makerobo_pin)
        control_1 = 1


class keepMonitor(Thread):
    """
    The Class used by a new thread keeps monitor the voice input from the user.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        """
        Main run function to start the Joy and do the initialization and monitors of settings and devices.
        :return: None
        """
        global last_result
        print("Started! Please speak")
        devices = sd.query_devices()  # get the devices
        print(devices)
        sd.default.device[1] = 0
        # sd.default.device[0] = 0
        sd.default.samplerate = 16000
        # sd.default.channels = 1, 2
        default_input_device_idx = sd.default.device[0]  # get the default device
        print(f'Use default device: {devices[default_input_device_idx]["name"]}')  # print the device name
        recognizer = create_recognizer()
        sample_rate = recognizer.sample_rate
        samples_per_read = int(0.3 * sample_rate)  # 0.1 second = 100 ms
        last_result = ""
        with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
            event.set()
            while not exit:
                if not event.is_set():  # if the network is not good, skip this loop
                    s.stop()
                event.wait()  # wait for the voice input
                s.start()
                if (len(last_result) > 500):
                    last_result = last_result[10:len(last_result)]  # delete the first 10 characters
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
    """
    The Class used a new thread keep receive the message from the server.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        """
        The main run function of receiving message. Initial the humidity and temperature sensor and do the monitor.
        :return: None
        """
        global skip
        makerobo_setup()  # initialize the humidity and temperature sensor
        event.wait()  # wait for the monitor to initialize
        loopNum = 0;
        while not exit:
            input_Msg = processMsg()
            if input_Msg == "voiceInput:":
                continue
            event.clear()
            sendString(input_Msg)  # send the voice input to the server
            time.sleep(0.01)
            msg = getData()
            if skip:  # if the network is not good, skip this loop
                print("网络出错了")
                skip = False
                continue
            mp3_to_wav("received.mp3")
            play_wav("received.wav")
            loopNum += 1
            getHumiture(loopNum)  # get the humidity and temperature


class keepPlayingV(Thread):
    """
    The Class with a new thread to play the video with received signal or waiting video.
    """
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        """
        The main run function of playing the media audio resources.
        :return: None
        """
        global signal
        instance = vlc.Instance()  # play the video
        player = instance.media_player_new()
        player.set_fullscreen(True)
        player.audio_set_mute(True)
        player.video_set_scale(0.85)
        media_list = instance.media_list_new()  # create a media list
        player_list = instance.media_list_player_new()
        player_list.set_media_player(player)
        bias = 0.02
        media = instance.media_new_path("微笑.mp4")  # add the video to the media list
        media_list.add_media(media)
        player_list.set_media_list(media_list)
        player_list.play()
        time.sleep(experissonTime["微笑"] - bias)
        while True:
            if signal != "":
                media = instance.media_new_path(signal + ".mp4")
                media_list.add_media(media)
                time.sleep(experissonTime[signal] - bias)
                signal = ""
            else:
                media = instance.media_new_path("微笑.mp4")
                media_list.add_media(media)
                time.sleep(experissonTime["微笑"] - bias)


# Do the socket connection.
sock = socket.socket()
sock.connect(('172.28.187.75', 9009))  # connect to the server
event = threading.Event()
event.clear()

tVideo = keepPlayingV("Playing_video")
tMonitor = keepMonitor("Monitor")
tRec = keepReceiveMsg("Receive_Msg")

tVideo.start()
tRec.start()
tMonitor.start()
