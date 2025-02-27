import librosa
import os
import sys

folder_path = "./Wavfiles"
"""FUNCTION TO PERFORM SHORT-TIME FOURNIER TRANSFORM TO CONVERT INPUT AUDIO FILE TO OUTPUT MEL-SPECTROGRAM"""
def preprocess(dir_path):
    try:
        log_file = open("message.log","w")
        sys.stdout = log_file
        for filename in os.listdir(folder_path):
            nested_path = folder_path + "/" + filename
            print("Nested Path ==> ",nested_path)
            for songFiles in os.listdir(nested_path):
                print("Inside ==>", songFiles)                           # Filename inside songFiles (Example: bass.wav)
                file_path = os.path.join(folder_path,filename, songFiles)
                instrumentals = 0
                vocals = ()
                if 'vocals' in songFiles:
                    vocals = vocals + librosa.load(file_path)
                    print("Vocals ==>",vocals)
                # elif 'vocals' in songFiles:
                #     vocals = vocals + librosa.load(file_path)
                #     print("Vocals ==>",vocals)
                elif 'drums' or 'bass' or 'other' in songFiles:
                    print("Inside bass,drums,other" , songFiles)
                    if instrumentals == 0:
                        instrumentals = librosa.load(file_path)
                    else:
                        instrumentals = instrumentals + librosa.load(file_path)
                    print("Instrumentals ==>",instrumentals)
                
                print("File Path ==>",file_path)    
        log_file.close()
    except Exception as e:
        print("Error",e)


preprocess(folder_path)