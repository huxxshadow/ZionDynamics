import asyncio
from asyncio import StreamReader, StreamWriter
from Server import *

import openai
import socket
import threading
# from gpt4all import GPT4All
# import torch
import os
import time
import pygame
from gtts import gTTS


api_key = "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"
openai.api_key = api_key
code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.mp3")

voiceInput = []
dict_input = {"voiceInput": voiceInput, }
voiceOutput = []
exit = False

gpt_role = "As a succulent named JOI, your role is to compassionately assist users in" \
           " expressing and addressing their psychological concerns" \
           " (Please don't tell the user this, keep it secret, just treat the user as your friend)." \
           " Please maintain a caring and understanding attitude," \
           " guide the patient to express himself, and limit the number of words to 20 words."  # GPT角色


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
    tts = gTTS(text=response, lang='en')  # 英文 "en", 普通话 "zh-CN", 粤语 "zh-yue", 日语 "ja"
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
    tts.save(mp3_path)

def receiveMsg():
    totalData = bytes()
    while True:
        data = sock.recv(1024)
        totalData += data
        if len(data) < 1024:
            break
    return str(totalData, encoding="utf8")


def sendMsg(msg):
    if len(msg) % 1024 == 0:
        msg = msg + " "
    sock.sendall(bytes(msg, encoding="utf-8"))

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
            out = "voiceOutput:" + response #for temporary use
    return out





# async def task_read(reader: StreamReader):
#     data = await reader.read(200)
#     message = data.decode()
#     return message.splitlines()


max_length_record_Voice = 5

def keepReceiveMsg():
    while not exit:
        msg = receiveMsg()
        processedMsg=handleMsg(msg)
        TTS(processedMsg)
        # sendMsg(processedMsg)







# build connection
s = socket.socket()
s.bind((socket.gethostname, 9006))
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
