import librosa
import os

folder_path = "./Wavfiles"
"""FUNCTION TO PERFORM SHORT-TIME FOURNIER TRANSFORM TO CONVERT INPUT AUDIO FILE TO OUTPUT MEL-SPECTROGRAM"""
def preprocess(dir_path):
    try:
        for filename in os.listdir(folder_path):
            print("Inside ==>", filename)
            file_path = os.path.join(folder_path, filename)
            print("Audio ==>",file_path)
        # --- Pass audio file to STFT function and assign output to mel_spectrogram ---
            audio, sr = librosa.load(file_path)
            print("Audio ==>",audio)
            # --- Retrun mel spectrogram ---
    except Exception as e:
        print("Error",e)


preprocess(folder_path)