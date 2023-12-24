from pydub import AudioSegment
import traceback


def convertFormatAndZip(inputFilePath, outputFilePath, convertedFormat="mp3", bitRate="32k"):
    """
    The function zip the MP3 format file. Require input file path, output file path. The parameter
     "bitRate" is chooseable, default is "32k". Lower than 32k, the size will not change.
    :param convertedFormat: the format after convert, should be same as outputfile postfix, default is mp3
    :param inputFilePath: path of the input file
    :param outputFilePath: path of the output file, postfix should be same as converted Format
    :param bitRate: the bit rate want to zip, default is 32k
    :return: no return
    """
    # When mp3 bit-rate is 64k, change 11.4MB -> 2.04MB
    # When mp3 bit-rate is 32k, change 11.4MB -> 1.02MB
    # When wav bit-rate is 32k, change 20.5MB -> 476KB
    # After 32k, the test audio does not express
    try:
        audio = AudioSegment.from_file(inputFilePath)
        compressed = audio.export(outputFilePath, format=convertedFormat, bitrate=bitRate)
    except Exception as e:
        print("There is something wrong with converting file format and zip it. There is the error message.")
        traceback.print_exc()




