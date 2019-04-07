from piwho import recognition

recog = recognition.SpeakerRecognizer()

recog.speaker_name = 'client'
recog.train_new_data('audio-files/audio-training-data/client')
recog.speaker_name = 'umar'
recog.train_new_data('audio-files/audio-training-data/umar')
recog.speaker_name = 'talha'
recog.train_new_data('../audio-files/audio-training-data/talha')
recog.speaker_name = 'hamza'
recog.train_new_data('../audio-files/audio-training-data/hamza')

identifiedSpeakers = []
identifiedSpeakers = recog.identify_speaker('../Audio-slicing/splitAudio/chunk0.wav')
print(identifiedSpeakers)
print("\n")
dictn = recog.get_speaker_scores()
print(dictn)
