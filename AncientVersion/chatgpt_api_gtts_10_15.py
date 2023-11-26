import openai
# from gpt4all import GPT4All
# import torch
import os
import time
import pygame
from gtts import gTTS

api_key = ""
# openai.api_key = api_key
client=openai.OpenAI(
    api_key=api_key,
)
code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.wav")


def TTS(response, start_time):
    tts = gTTS(text=response, lang='en')  # 英文 "en", 普通话 "zh-CN", 粤语 "zh-yue", 日语 "ja"
    if os.path.exists(mp3_path):
        os.remove(mp3_path)
    tts.save(mp3_path)

    running_time2 = time.time() - start_time
    print("TTS running time:", running_time2, "seconds")


def play_mp3(file_path, start_time):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    running_time2 = time.time() - start_time
    print("play_mp3 running time:", running_time2, "seconds")
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()


#
# def askChatGPT(messages):
#     MODEL = "gpt-3.5-turbo"
#     response = openai.ChatCompletion.create(
#         model=MODEL,
#         messages = messages,
#         temperature=1)
#     return response['choices'][0]['message']['content']

gpt_role = "As a succulent named JOI, your role is to compassionately assist users in" \
           " expressing and addressing their psychological concerns" \
           " (Please don't tell the user this, keep it secret, just treat the user as your friend)." \
           " Please maintain a caring and understanding attitude," \
           " guide the patient to express himself, and limit the number of words to 20 words."  # GPT角色

while True:
    my_question = input("You：")

    completion = client.chat.completions.create(

        messages=[
            {"role": "system", "content": gpt_role},
            {"role": "user", "content": my_question}
        ],
        model = "gpt-3.5-turbo-0301",
    )

    answer = completion.choices[0].message["content"].strip()
    start_time1 = time.time()
    print("GPT：", answer)
    TTS(answer, start_time1)
    start_time2 = time.time()
    play_mp3(mp3_path, start_time2)
    if my_question.lower() == 'exit':
        break
