import pydub
from pydub.playback import play
import soundfile

sound = pydub.AudioSegment.from_file("../audio-files/audio-training-data/Bakhtiyar/bakhtiyar5.mp3")

# sound = pydub.AudioSegment.from_file("../audio-files/sample-audios/Conversation-Audio-Sample.m4a") 
# sound = sound[0:58000]

try:
    sound.export("../audio-files/audio-training-data/Bakhtiyar/bakhtiyar5.wav", format="wav")

    # sound.export("../audio-files/output-files/Output.wav", format="wav")
    # data, samplerate = soundfile.read('../audio-files/output-files/Output.wav')
    # soundfile.write('../audio-files/output-files/Output.wav', data, samplerate, subtype='PCM_16')
    print("success")
except err: 
    print(err)