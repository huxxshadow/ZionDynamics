import openai
import os
import time
import os
import azure.cognitiveservices.speech as speechsdk
import wave

api_key = "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"
openai.api_key = api_key

azure_key = '41772f6a68ad4b6aa64d8a18f2f8a150'
region = 'eastus'
subscription_key = azure_key
code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.wav")

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription='41772f6a68ad4b6aa64d8a18f2f8a150', region='eastus')

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)
file_config = speechsdk.audio.AudioOutputConfig(filename=mp3_path)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=file_config)
def TTS(text, start_time):
    speech_synthesizer.speak_text_async(text)
    # audio_data = result.audio_data
    # with wave.open(mp3_path, 'wb') as wave_file:
    #     wave_file.setnchannels(1)  # Set the number of channels (1 for mono, 2 for stereo)
    #     wave_file.setsampwidth(2)  # Set the sample width (2 bytes for 16-bit audio)
    #     wave_file.setframerate(16000)  # Set the sample rate (e.g., 16000 Hz)
    #     wave_file.writeframes(audio_data)
    running_time2 = time.time() - start_time
    print("TTS running time:", running_time2, "seconds")

gpt_role = "现在假设你assistant的名字改为JOI，是一盆智能的植物，"\
            "JOI将称呼用户为主人。"\
            "你要关心和倾听用户的想法和感受，表达同理心，"\
            "然后通过疑问句或冷读术引导用户表达和倾诉，"\
            "并限制每次回答的字数在20字以内。"\
            "根据上述回答的情感,从以下列表里[生气,流汗,哭哭,眨眼,惊讶,微笑]只挑选一个可以概括的内容的字符串在回答末尾用中括号围起来加上"

while True:
    my_question = input("You：")

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",
        messages=[
            {"role": "system", "content": gpt_role},
            {"role": "user", "content": my_question}
        ]
    )

    answer = completion.choices[0].message["content"].strip()
    start_time1 = time.time()
    print("GPT：", answer)
    TTS(answer, start_time1)
    start_time2 = time.time()
    if my_question.lower() == 'exit':
        break
