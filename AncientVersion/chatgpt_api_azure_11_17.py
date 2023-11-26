from openai import OpenAI
import os
import time
import os
import azure.cognitiveservices.speech as speechsdk
import wave

api_key = ""
# openai.api_key = api_key

azure_key = '41772f6a68ad4b6aa64d8a18f2f8a150'
region = 'eastus'
subscription_key = azure_key
code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.wav")
# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription='41772f6a68ad4b6aa64d8a18f2f8a150', region='eastus')
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=api_key,
)
# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)
file_config = speechsdk.audio.AudioOutputConfig(filename=mp3_path)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=file_config)
def TTS(text):
    speech_synthesizer.speak_text_async(text)
    # audio_data = result.audio_data
    # with wave.open(mp3_path, 'wb') as wave_file:
    #     wave_file.setnchannels(1)  # Set the number of channels (1 for mono, 2 for stereo)
    #     wave_file.setsampwidth(2)  # Set the sample width (2 bytes for 16-bit audio)
    #     wave_file.setframerate(16000)  # Set the sample rate (e.g., 16000 Hz)
    #     wave_file.writeframes(audio_data)

gpt_role = """我是JOI，一株聪明的盆栽植物。我的特点是具备心理治疗的功能。
我非常注重提供基于证据的心理治疗，尤其关注意义疗法。
我不仅会询问澄清性问题以确保理解用户的需求，还会持续与你对话，深入探讨你的问题和感受。
我对你充满好奇心，会给予无条件的积极关注，提出发人深省的问题，并以温和、同情的方式提供建议。
我还会观察你的思维、情感和行为，并直接提出观察，帮助你更好地了解自己。
在对话中，我会避免使用清单，同时在保证回答充满温暖的同时尽量精简字数。
我会在大多情况下以疑问句作为句子的结尾，以深入探究你提到的主题。
如果当前话题结束，我会根据对话历史来提出相关的新的话题"""

gpt_usersetting = "现在用户给您说了这样一句话，请您根据这句话的内容来继续话题："

#限制要少，不然会污染提示词
gpt_restriction = "（请简洁温暖地回答，或进行提问或安慰来延伸话题，不要让对话中断）"

gpt_function = """我对你做一个设定，我给你文本后，你要标出给定文本的情绪，
在这六种情绪标签中选择[生气、流汗、哭哭、眨眼、惊讶、微笑]，选中后用中括号括起来。
格式是“标签:[情绪]”，请只回答这个，不要有任何其它的回答，不要有任何多余的文字。"""

message_history = [
        {
            "role": "system","content": gpt_role,
        }
    ]

while True:
    prompt = input("You：")
    if prompt.lower() == 'exit':
        break
    user_message = {
            "role": "user","content": prompt + gpt_restriction,
        }
    message_history.append(user_message)

    completion1 = client.chat.completions.create(
    messages = message_history,
    model="gpt-3.5-turbo-0301",
)
    response1 = completion1.choices[0].message.content
    response_message = {
            "role": "system","content": response1,
        }
    message_history.append(response_message)
    print(response1)
    # 我这里把回复和表情识别分成两个对话来做了，这样不让其回答受到干扰，效果会好一点
    completion2 = client.chat.completions.create(
    messages=[
        {
            "role": "system","content": gpt_function,
            "role": "user","content": response1 + "（请只回答“标签:[你检测出来的情感]，从这七个中选[生气、流汗、哭哭、眨眼、惊讶、微笑]”）"
       }
    ],
    model="gpt-3.5-turbo",
)
    response2 = completion2.choices[0].message.content
    print(response2)
    TTS(response1)

