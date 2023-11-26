import asyncio
import os
import time

import sherpa_ncnn
import sys
import sounddevice as sd
from gtts import gTTS
import pygame

code_path = os.path.dirname(os.path.abspath(__file__))
mp3_path = os.path.join(code_path, "mp3.mp3")




# def TTS(response, start_time):
#     tts = gTTS(text=response, lang='en')  # 英文 "en", 普通话 "zh-CN", 粤语 "zh-yue", 日语 "ja"
#     if os.path.exists(mp3_path):
#         os.remove(mp3_path)
#     tts.save(mp3_path)

    # running_time2 = time.time() - start_time
    # print("TTS running time:", running_time2, "seconds")


def play_mp3(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    # running_time2 = time.time() - start_time
    # print("play_mp3 running time:", running_time2, "seconds")
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.music.stop()
    pygame.mixer.quit()
    pygame.quit()


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


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection("192.168.137.1", 9006)
    print(f'Send to server: {message!r}')

    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(200)
    output = data.decode()

    print(f'Received from server: {output!r}')
    TTS(output.split(":", 1)[1], 0)
    play_mp3(mp3_path)
    writer.close()
    await writer.wait_closed()


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


if __name__ == '__main__':
    recognizer, sample_rate, samples_per_read = soundInput_initial()

    while True:
        try:
            recognizer = create_recognizer()
            result = sound_echo(recognizer, sample_rate, samples_per_read)
        except KeyboardInterrupt:
            print("\nCaught Ctrl + C. Exiting")

        send_msg = "voiceInput:" + result
        asyncio.run(tcp_echo_client(send_msg))
