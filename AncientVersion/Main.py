#
#
# import Adafruit_DHT
# import time
# import sherpa_ncnn
# import sys
import sounddevice as sd
import soundfile as sf

def play_wav(file_path):
    print(sd.query_devices())
    data, fs = sf.read(file_path)
    sd.play(data, fs)
    sd.wait()
    print("done")

play_wav("received.wav")




#
# def  sound_setup():
#     devices = sd.query_devices()
#     print(devices)
#     default_input_device_idx = sd.default.device[0]
#     print(f'Use default device: {devices[default_input_device_idx]["name"]}')
#     recognizer = sherpa_ncnn.Recognizer(
#         tokens="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/tokens.txt",
#         encoder_param="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/encoder_jit_trace-pnnx.ncnn.param",
#         encoder_bin="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/encoder_jit_trace-pnnx.ncnn.bin",
#         decoder_param="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/decoder_jit_trace-pnnx.ncnn.param",
#         decoder_bin="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/decoder_jit_trace-pnnx.ncnn.bin",
#         joiner_param="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/joiner_jit_trace-pnnx.ncnn.param",
#         joiner_bin="./sherpa-ncnn-conv-emformer-transducer-2022-12-06/joiner_jit_trace-pnnx.ncnn.bin",
#         num_threads=4,
#     )
#     sample_rate = recognizer.sample_rate
#     samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms
#     last_result = ""
#
#
#
#
# def makerobo_setup():
# 	global sensor
# 	sensor = Adafruit_DHT.DHT11
#
#
#
#
# def sound_loop(recognizer, sample_rate, samples_per_read, last_result):
#     with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
#         while True:
#             samples, _ = s.read(samples_per_read)  # a blocking read
#             samples = samples.reshape(-1)
#             recognizer.accept_waveform(sample_rate, samples)
#             result = recognizer.text
#             if last_result != result:
#                 last_result = result
#                 print("\r{}".format(result), end="", flush=True)
#
# def main():
#
#     pass
#
# if __name__ == '__main__':
# 	makerobo_setup()
# 	try:
# 		main()
# 	except KeyboardInterrupt:  # 当按下Ctrl+C时，将执行destroy()子程序。
# 		destroy()