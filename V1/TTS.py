import azure.cognitiveservices.speech as speechsdk
from SupplemntaryTool import *

# get the License
azure_key = '834cf1d719644bc98ee2ea9e74557625'
region = 'eastus'
subscription_key = azure_key
speech_config = speechsdk.SpeechConfig(subscription='834cf1d719644bc98ee2ea9e74557625', region='eastus')
speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"  # set the voice type

# speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff44100Hz16BitMonoPcm)
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio48Khz96KBitRateMonoMp3)  # set the output format
file_config = speechsdk.audio.AudioOutputConfig(filename="temp.mp3")  # set the output file name

# @timer
def TTS(textResponse):
    """
    The function is to convert the String format to mp3 format.
    :param textResponse: The string input.
    :return: The mp3 format of the audio according to the input text String.
    """
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    result = speech_synthesizer.speak_text_async(textResponse).get()
