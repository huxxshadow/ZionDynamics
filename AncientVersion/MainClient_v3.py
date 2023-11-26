import os
import time
import sherpa_ncnn
import sounddevice as sd
import Adafruit_DHT
import soundfile as sf
import socket
from threading import Thread
import threading
from pydub import AudioSegment
import vlc


global signal
global skip

skip=False
signal = ""

experissonTime={"微笑":4.002,"流汗":1.767,"哭哭":1.106,"生气":1.875,"眨眼":1.667}
code_path = os.path.dirname(os.path.abspath(__file__))
exit = False

makerobo_pin = 17
global humidity,temperature,control_1
humidity=0
temperature=0
control_1=0

global last_result, length_last
length_last = 0
last_result = ""

def makerobo_setup():
	global sensor
	sensor = Adafruit_DHT.DHT11
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
def receiveLongMsg():
    totalData = bytes()
    totallen=int.from_bytes(sock.recv(4), byteorder='little')
    while totallen!=0:
        if totallen<0:
            totalData=bytes()
            break
        data = sock.recv(1024)
        totallen-=len(data)
        totalData += data
    print(len(totalData))
    return totalData
def receiveShortMsg(len):
    data = sock.recv(len)
    return data

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
    with open('received.mp3', 'wb') as file:
        data = receiveLongMsg()
        if len(data)==0:
            global skip
            skip=True;
            return
        file.write(data)
        print("This is the write wav stage.")
def mp3_to_wav(mp3_path):
    sound = AudioSegment.from_mp3(mp3_path)
    print(sound.frame_rate)
    sound.export("received.wav", format="wav")
def play_wav(file_path):
    data, fs = sf.read(file_path)
    # print(fs)
    # print("时间开始流动")
    sd.play(data, fs)
    sd.wait()
    event.set()
    # print("时间流动结束")
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
    global control_1
    if control_1==1:
        control_1==0;
        msg+="\nhumidityInput:"+str(humidity)+";"+str(temperature)
    sock.sendall(bytes(msg, encoding="utf-8"))
def getHumiture(num):
    if num%2==0:
        global humidity,temperature,control_1
        humidity, temperature = Adafruit_DHT.read_retry(sensor, makerobo_pin)
        control_1=1
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
            event.clear()
            sendString(input_Msg)
            time.sleep(0.01)
            msg = getData()
            if skip:
                print("网络出错了")
                skip=False
                continue
            mp3_to_wav("received.mp3")
            play_wav("received.wav")
            loopNum+=1
            getHumiture(loopNum)

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
        player.video_set_scale(0.85)
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

sock = socket.socket()
sock.connect(('172.28.187.75', 9009))
event=threading.Event()
event.clear()

tVideo=keepPlayingV("Playing_video")
tMonitor = keepMonitor("Monitor")
tRec = keepReceiveMsg("Receive_Msg")

tVideo.start()
tRec.start()
tMonitor.start()

