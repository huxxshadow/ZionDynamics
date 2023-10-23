import asyncio
import io
import wave
from asyncio import StreamReader, StreamWriter
from Server import *

import openai
import socket
import threading
import struct
import array

# from gpt4all import GPT4All
# import torch
import os
import time
import pygame
from gtts import gTTS
from pydub import AudioSegment

api_key = "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"
openai.api_key = api_key
code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.mp3")

voiceInput = []
dict_input = {"voiceInput": voiceInput, }
voiceOutput = []

STRING_SPECIFIER = "2222"
WAV_SPECIFIER = "3333"
exit = False

# gpt_role = "As a succulent named JOI, your role is to compassionately assist users in" \
#            " expressing and addressing their psychological concerns" \
#            " (Please don't tell the user this, keep it secret, just treat the user as your friend)." \
#            " Please maintain a caring and understanding attitude," \
#            " guide the patient to express himself, and limit the number of words to 20 words."  # GPT角色
gpt_role = "作为一名名叫 JOI 的多肉植物，你的职责是充满爱心地帮助用户表达和解决他们的心理问题（请不要告诉用户这些，保守秘密，只把用户当作你的朋友）。请保持关心和理解的态度，引导患者表达，字数控制在 20 个字以内。"  # GPT角色


def askChatGPT(current_question, question_record, response_record):
    list_message = [{"role": "system", "content": gpt_role}, ]
    if len(question_record) > 0:
        for i in range(len(question_record)):  # length of response_record is same as question_record
            list_message.append({"role": "user", "content": question_record[i]})
            list_message.append({"role": "assistant", "content": response_record[i]})
    list_message.append({"role": "user", "content": current_question})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=list_message,
    )

    answer = completion.choices[0].message["content"].strip()
    return answer


def TTS(response):
    tts = gTTS(text=response, lang='zh-CN')  # 英文 "en", 普通话 "zh-CN", 粤语 "zh-yue", 日语 "ja"
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
    tts.save(mp3_path)

def mp3_to_wav(mp3_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export("temp.wav", format="wav")

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
    print("this is the specifier: " + specifier)
    if specifier == STRING_SPECIFIER:
        receivedStr = str(receiveMsg(), encoding="utf-8")
        print("this is the receive msg: " + receivedStr+"###")
        return receivedStr
    # elif specifier == WAV_SPECIFIER:
    #     data = receiveMsg()
    #     ww = wave.open('received.wav', 'wb')
    #     ww.writeframes(data)
    #     ww.close()



def sendString(msg):
    sock.sendall(bytes(STRING_SPECIFIER,encoding="utf-8"))
    if len(msg) % 1024 == 0:
        msg = msg + " "
    sock.sendall(bytes(msg, encoding="utf-8"))


def sendWAV(songPath):
    sock.sendall(bytes(WAV_SPECIFIER, encoding="utf-8"))
    print("sending wav file")
    # file = wave.open(songPath, 'rb')
    with open(songPath,"rb") as file:
        data=file.read()
        sock.sendall(data)

    # songData = str(file.getframerate()) + " " + str(file.getnframes())
    # sock.sendall(songData.encode("utf-8"))
    # sock.sendall(str(file.getframerate()).encode("utf-8"))
    # time.sleep(1)
    # sock.sendall(str(file.getnframes()).encode("utf-8"))
    # time.sleep(1)
    # sock.sendall(file.readframes(file.getnframes()))
    # time.sleep(1)
    # sock.sendall(bytes(str(file.getnchannels()), encoding="utf-8"))
    # sock.sendall(bytes(str(file.getsampwidth()), encoding="utf-8"))
    # sock.sendall(int.to_bytes(file.getnchannels()))
    # sock.sendall(int.to_bytes(file.getsampwidth()))
    # sock.sendall(int.to_bytes(file.getnframes(),4,byteorder="little"))

def handleMsg(msg):
    input_list = msg.splitlines()

    for input_line in input_list:
        input_ = input_line.split(":", 1)
        inputType = input_[0]
        input_content = input_[1]
        dict_input[inputType].append(input_content)

    if inputType == "voiceInput":
        if len(voiceInput) > 1:
            response = askChatGPT(dict_input["voiceInput"][-1], dict_input["voiceInput"][0:-1], voiceOutput)
        else:
            response = askChatGPT(dict_input["voiceInput"][-1], [], [])
        voiceOutput.append(response)

        if len(voiceInput) > max_length_record_Voice:
            voiceInput.pop(0)
        if len(voiceOutput) > max_length_record_Voice:
            voiceOutput.pop(0)
        out = response  # for temporary use
    return out


max_length_record_Voice = 5


def keepReceiveMsg():
    while not exit:
        msg = getData()
        processedMsg = handleMsg(msg)
        TTS(processedMsg)
        mp3_to_wav(mp3_path)
        sendWAV("temp.wav")
        time.sleep(0.05)
        # sendMsg(processedMsg)


# def mainSendMsg():
#     


# build connection
s = socket.socket()
s.bind(("172.28.162.150", 9007))
# n+1
s.listen(5)
# block, build session, sock_clint
sock, addr = s.accept()

print(sock, addr)

tRec = threading.Thread(target=keepReceiveMsg(), name="Receive_Msg")
# tSend = threading.Thread(target=mainSendMsg(), name="MainSendMsg")

tRec.start()
# tSend.start()
tRec.join()
# tSend.join()
