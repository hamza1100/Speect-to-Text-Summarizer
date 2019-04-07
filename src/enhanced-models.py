# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    # from google.cloud import speech
    # from google.cloud.speech import enums
    # from google.cloud.speech import types
    from google.cloud import speech_v1p1beta1 as speech
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types
    from google.protobuf.json_format import MessageToJson, MessageToDict
    import io, os, json

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        language_code='en-US',
        # enable_word_confidence=True,
        # enable_speaker_diarization=True,
        # diarization_speaker_count=3,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
        # audio_channel_count=2,
        # enable_separate_recognition_per_channel=True        
        )

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    # response = MessageToJson(response)
    # print(response)
    # with open('data.json', 'w') as outfile:
    #     json.dump(response, outfile)
    # response = MessageToDict(response)
    for result in response.results:
        print(result.alternatives[0].transcript)
    # print(response)
    # with open('data.json', 'w') as outfile:
    #     json.dump(response, outfile)

# [END speech_transcribe_async_gcs]

transcribe_gcs("gs://voice-notes-cloud-storage/audio-full-sample.wav")
# transcribe_gcs("gs://voice-notes-cloud-storage/Final-audio.wav")
