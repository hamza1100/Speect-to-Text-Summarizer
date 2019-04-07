# Library Imports
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.protobuf.json_format import MessageToDict
from pydub import AudioSegment, silence
from pydub.silence import split_on_silence
from pyAudioAnalysis import audioTrainTest as aT
from Text_Summarization import generate_summary as GenerateSummary
import io, os, json
from os import path
import sys
sys.path.append(path.abspath('../speaker-identification'))


# Speech to text with speaker recognition
class voice_notes:
    # Instantiate a Libraries
    client = speech.SpeechClient()

    # sound_file = AudioSegment.from_wav("./audio_before_slicing.wav")
    sound_file = AudioSegment.from_wav("../../audio-files/sample-audios/audio-full-sample.wav")
    No_Of_Chunks = len(silence.detect_nonsilent(sound_file,min_silence_len=1000,silence_thresh=-30))
    full_response = None

    def __init__(self):
        print("  Welcome to Voice Notes\n--------------------------")

    #  slice audio into multiple chunks and export them as .wav files
    def slice_Audio_Into_AudioChunks(self):
        chunks = self.Split_Audio_Chunk()
        for i, chunk in enumerate(chunks):
            out_file = "./splitAudio/chunk{0}.wav".format(i)
            print("exporting", out_file)
            chunk.export(out_file, format="wav")

    # split audio on non silence then extract last 2 second of each chunk to make
    # chunk1 + (<last 2 seconds of chunk1> + chunk2) + (<last 2 seconds of chunk2> + chunk3) + ...
    def Split_Audio_Chunk(self):
        chunks = []
        second_of_silence = AudioSegment.silent(duration=200)
        nonsilent_list = silence.detect_nonsilent(self.sound_file,min_silence_len=1000, 
        silence_thresh=-30)
        # silence_thresh=self.sound_file.dBFS)
        #  append first chunk directly
        chunks.append(second_of_silence + 
        self.sound_file[nonsilent_list[0][0]: nonsilent_list[0][1]] + 
        second_of_silence)
        # we have to skip first element so loop starting from index 1 and append last 2second chunks
        for nonsilent_chunk in nonsilent_list[1:]:
            start = nonsilent_chunk[0]-2000
            end = nonsilent_chunk[1]
            chunk = second_of_silence + self.sound_file[start: end] + second_of_silence
            chunks.append(chunk)
        return chunks

    # Return offets of audio chunks 
    def Find_Chunks_Offset(self):
        last_word_offsets = []
        config = types.RecognitionConfig(language_code='en-US', enable_word_confidence=True, enable_word_time_offsets=True)
        self.full_response = self.Speech_To_Text_Long('gs://voice-notes-cloud-storage/Final-audio.wav') 
        for i in range(self.No_Of_Chunks):
            file_name = os.path.join(os.path.dirname(__file__),'./splitAudio/chunk{}.wav'.format(i))
            with io.open(file_name, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)
            sentence_response = self.client.recognize(config, audio)
            word_object = sentence_response.results[0].alternatives[0].words[0]
            word_found = self.Find_Word_In_Text(word_object.word, self.full_response)
            if(word_found):
                word_found = MessageToDict(word_found)
                word_offset = word_found['endTime']
                last_word_offsets.append(word_offset)
            else:
                last_word_offsets.append(None)
        return last_word_offsets

    # Return word object if found in full audio text
    def Find_Word_In_Text(self, word_in_text, text):
        for result in text.results:
            for word_object in result.alternatives[0].words:
                if(word_in_text == word_object.word):
                    return word_object

    # convert audio(>1 min) into text
    def Speech_To_Text_Long(self, audio_uri):
            audio = types.RecognitionAudio(uri=audio_uri)
            config = types.RecognitionConfig(language_code='en-US', enable_word_time_offsets=True,
                audio_channel_count=2, enable_separate_recognition_per_channel=True)
            operation = self.client.long_running_recognize(config, audio)
            print('Waiting for operation to complete...')
            response = operation.result(timeout=90)
            return response

    # Train model with speaker`s audio 
    def Train_Speakers(self):
        dir_1 = "../../audio-files/audio-training-data/hamza"
        dir_2 = "../../audio-files/audio-training-data/talha"      
        dir_3 = "../../audio-files/audio-training-data/umar"
        aT.featureAndTrain(
            [dir_1, dir_2, dir_3],          #list_of_dirs 
            1.0, 1.0,                       #mt_win, mt_step
            aT.shortTermWindow, aT.shortTermStep,   #st_win, st_step
            "svm",                  # classifier_type 
            "svmMusicGenre3",       # model_name
            True)                   # compute_beat

    # Identify speakers in the given audio 
    def Identify_Speakers(self, file_path=""):
        if(file_path):
            classify = aT.fileClassification(file_path, "svmMusicGenre3", "svm")
        else:
            speakers = []
            for i in range(self.No_Of_Chunks): 
                classify = aT.fileClassification("../Audio-slicing/splitAudio/chunk{}.wav".format(i), "svmMusicGenre3", "svm")
                if(classify[0] != -1):
                    speakers.append(classify[2][int(classify[0])])
                else:
                    print(classify)
        return speakers

    # generate meeting minutes with speaker tags
    def Generate_Manuscript(self):
        # Opening File for writing
        text_file = open("Manuscript.txt", "w")
        sentences = []
        speakers = self.Identify_Speakers()
        offsets = self.Find_Chunks_Offset()
        filtered_speakers = []
        filtered_offsets = []
        for i, val in enumerate(offsets):
            if(offsets[i] != None):
                filtered_speakers.append(speakers[i])
                filtered_offsets.append(offsets[i])
        initial_k = 0
        for i in range(len(filtered_offsets)):
            words_in_sentence = []            
            for j, result in enumerate(self.full_response.results):
                for k in range(initial_k, len(result.alternatives[0].words)):
                    word_object = result.alternatives[0].words[k]
                    word_object = MessageToDict(word_object)
                    if float(word_object['endTime'][:-1]) <= float(filtered_offsets[i][:-1]):
                        words_in_sentence.append(word_object['word'])
                    else:
                        initial_k = k
                        break
            sentences.append( dict(words=words_in_sentence, label=filtered_speakers[i] ))
        for sentence in sentences:
            if(len(sentence['words']) == 0):
                continue
            text_file.write(sentence['label'] + ': ')
            for word in sentence['words']:
                text_file.write(word + ' ')
            text_file.write('\n')
        return sentences

    # generate meeting summary from given audio 
    def Generate_Summary(self, path):
        GenerateSummary(path)

if __name__ == '__main__':
    vn_instance = voice_notes()

    # To generate manuscript
    vn_instance.Generate_Manuscript()

    # To generate summary
    vn_instance.Generate_Summary('sample-text.txt')

