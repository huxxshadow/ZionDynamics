
import socket
import threading
import time

from LLM import *
from TTS import *
from SupplemntaryTool import *



# code_path = os.path.dirname(os.path.abspath(__file__))
# mp3_path = os.path.join(code_path, "temp.mp3")

# initial parameters
voiceInput = []
humidityInput = []
dict_input = {"voiceInput": voiceInput, "humidityInput": humidityInput}
emotion_tag=["生气","流汗","哭哭","眨眼","惊讶","微笑"]
voiceOutput = []

exit = False

#humidifier initial parameters
global control_2, t1
control_2 = 0
t1 = time.time()

global expSignal
expSignal = ""



def getData():
    """
    The function get the data from the server.
    :return: The received String from the server in String format.
    """
    totalData = bytes()
    while True:
        data = sock.recv(1024)
        totalData += data
        if len(data) < 1024:
            break

    receivedStr = str(totalData, encoding="utf-8")
    print("this is the receive msg: " + receivedStr + "###")
    return receivedStr

@timer
def sendString(msg):
    """
    The function send the message with String format to the client.
    :param msg: The message which should be sent to the client in String format.
    :return: None
    """
    # send the string to the client
    # if len(msg) == 4:
    #     if msg[0] == "[" and msg[3] == "]":  # if the string is an expression
    #         print("发送" + msg[1:3])
    #         send = msg[1:3].encode("utf-8")
    #         print(len(send))
    #         sock.sendall(send)
    #     else:
    #         print("发送wrong")
    #         send = "nu".encode("utf-8")
    #         sock.sendall(send)
    # # if len(msg) % 1024 == 0:
    # else:  # if the string is a normal string
    #     print("发送null")
    #     send = "nu".encode("utf-8")
    #     sock.sendall(send)

    if len(msg) == 2:
        print("发送" + msg)
        send = msg.encode("utf-8")
        print(len(send))
        sock.sendall(send)
    else:
        print("发送null")
        send = "nu".encode("utf-8")
        sock.sendall(send)





@timer
def sendWAV(songPath):
    """
    The function send WAV file to the client.
    :param songPath: The path of the WAV file.
    :return: None
    """
    print("try to send mp3 file")
    with open(songPath, "rb") as wavfile:  # read the mp3 file
        input_wav = wavfile.read()
    sock.sendall(int.to_bytes(len(input_wav), 4, byteorder="little"))
    time.sleep(0.05)
    sock.sendall(input_wav)
    print(len(input_wav))
    print("finished sending mp3 file")

# @timer
def handleMsg(msg):
    """
    The function handle the message from the client with specifier.
    :param msg: The received message including voice, humidity.
    :return: None
    """
    input_list = msg.splitlines()
    out = ""
    for input_line in input_list:
        input_ = input_line.split(":", 1)  # get the input type and input content
        inputType = input_[0]
        input_content = input_[1]
        dict_input[inputType].append(input_content)

        if inputType == "voiceInput":  # if the input is a voice
            if len(voiceInput) > 1:
                response,feeling = askChatGPT(dict_input["voiceInput"][-1], dict_input["voiceInput"][0:-1], voiceOutput)
            else:
                response,feeling = askChatGPT(dict_input["voiceInput"][-1], [], [])
            voiceOutput.append(response)

            if len(voiceInput) > max_length_record_Voice:
                voiceInput.pop(0)
            if len(voiceOutput) > max_length_record_Voice:
                voiceOutput.pop(0)
            # global expSignal
            # expSignal = response[len(response) - 4:len(response)]  # get the expression signal
            # if expSignal[0] == "[" and expSignal[3] == "]":
            #     out += response[0:len(response) - 4]  # get the response without the expression signal
            # else:
            out += response
            global expSignal
            expSignal=None
            for tag in emotion_tag:
                if tag in feeling:
                    expSignal= tag
                    break
        if inputType == "humidityInput":  # if the input is a humidity
            hum = input_content.split(";")
            humidity = hum[0]
            temperature = hum[1]
            if (float(temperature) > 28):
                out += f"警告警告,温度已达{temperature},请调整至合适温度"  # if the temperature is too high, then give a warning
            global t1
            t2 = time.time()
            if float(humidity) > 80:
                t1 = time.time()
            if t2 - t1 > 10:
                timeInSecond = t2 - t1  # get the time interval between the current time and the time
                hours = int(timeInSecond / 3600)
                minutes = int((timeInSecond - hours * 3600) / 60)
                seconds = int(timeInSecond - hours * 3600 - minutes * 60)  #
                if hours == 0 and minutes != 0:
                    out += f"警告警告,距离上次浇水时间已过去{minutes}分{seconds}秒,请及时浇水"
                elif minutes == 0:
                    out += f"警告警告,距离上次浇水时间已过去{seconds}秒,请及时浇水"
    return out


max_length_record_Voice = 5  # the max length of the voice record


def keepReceiveMsg():
    """
    The function keep receive the message from the client and send expression signal and mp3 file.
    :return: None
    """
    while not exit:
        msg = getData()
        print(msg)
        processedMsg = handleMsg(msg)  # handle the message
        message = TTS(processedMsg)
        sendString(expSignal)  # send the expression signal
        time.sleep(0.01)
        sendWAV("temp.mp3")  # send the mp3 file
        time.sleep(0.02)


# do the socket connection
s = socket.socket()
s.bind(("172.28.163.131", 9008))  # bind the socket
s.listen(5)
sock, addr = s.accept()
print(sock, addr)  # accept the connection
tRec = threading.Thread(target=keepReceiveMsg(), name="Receive_Msg")
tRec.start()
tRec.join()
