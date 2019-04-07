# Imports the Google Cloud client library
# from google.cloud import speech_v1p1beta1 as speech   # for short audio files
from google.cloud import speech                         # for long audio files
# from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech import enums
# from google.cloud.speech_v1p1beta1 import types
from google.cloud.speech import types
from google.protobuf.json_format import MessageToJson, MessageToDict
import io, os, json

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = os.path.join(
    os.path.dirname(__file__),
    '../audio-files/sample-audios/audio-full-sample.wav')
    # '../Audio-slicing/splitAudio/chunk0.wav')

# Loads the audio into memory
with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code='en-US',
    # enable_word_confidence=True,
    # enable_speaker_diarization=True,
    # diarization_speaker_count=3,
    # enable_word_time_offsets=True,
    # enable_automatic_punctuation=True,
    # audio_channel_count=2,
    # enable_separate_recognition_per_channel=True
    )

# Detects speech in the short audio file(less than 1 min)
response = client.recognize(config, audio)

for result in response.results:
    print(result.alternatives[0].transcript)

# response = MessageToDict(response)
# print(response)
# print(response)
# with open('data.json', 'w') as outfile:
#     json.dump(response, outfile)
