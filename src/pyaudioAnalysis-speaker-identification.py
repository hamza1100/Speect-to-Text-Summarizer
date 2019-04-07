from os import path
import sys
sys.path.append(path.abspath('../speaker-identification'))
from pyAudioAnalysis import audioTrainTest as aT

dir_1 = "../audio-files/audio-training-data/hamza"
dir_2 = "../audio-files/audio-training-data/talha"      
dir_3 = "../audio-files/audio-training-data/umar"

'''
This function is used as a wrapper to segment-based audio feature extraction and classifier training.
ARGUMENTS:
    list_of_dirs:        list of paths of directories. Each directory contains a signle audio class whose samples are stored in seperate WAV files.
    mt_win, mt_step:        mid-term window length and step
    st_win, st_step:        short-term window and step
    classifier_type:        "svm" or "knn" or "randomforest" or "gradientboosting" or "extratrees"
    model_name:        name of the model to be saved
RETURNS:
    None. Resulting classifier along with the respective model parameters are saved on files.
'''
aT.featureAndTrain([dir_1, dir_2, dir_3], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmMusicGenre3", True)

for i in range(10): 
    classify = aT.fileClassification("../Audio-slicing/splitAudio/chunk{}.wav".format(i), "svmMusicGenre3", "svm")
    if(classify[0] != -1):
        print(i, classify[2][int(classify[0])])
    else:
        print(classify)
