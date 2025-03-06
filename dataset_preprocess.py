import librosa
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pydub import AudioSegment

folder_path = "./Wavfiles"

# --- Connfigure ffmpeg ---
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"  # Or check using `which ffmpeg`
AudioSegment.converter = ffmpeg_path

# --- Max NP array size --- 
np.set_printoptions(threshold=sys.maxsize)

print(f"Using ffmpeg from: {AudioSegment.converter}")

"""FUNCTION TO PERFORM SHORT-TIME FOURNIER TRANSFORM TO CONVERT INPUT AUDIO FILE TO OUTPUT MEL-SPECTROGRAM"""
def dataset_preprocess(dir_path):
    try:
        log_file = open("message.log","w")
        sys.stdout = log_file
        
        # --- Initialize dataframe to store spectrograms and their labels--- 
        df = pd.DataFrame()
 
        # --- Loop through every subfolder(song) in the dataset --- 
        for song in os.listdir(dir_path):
            nested_path = dir_path + "/" + song
            print("Nested Path ==> ",nested_path)

            # --- Checker if an instrumental file was hit ---
            instrumentals = False

            # --- Loop through every feature in the subfolder(song) ---
            for songFiles in os.listdir(nested_path):
                # --- Get the song name and directory in a string --- 
                print("Inside ==>", songFiles)                        
                file_path = os.path.join(dir_path,song, songFiles)
                

                # --- Transform vocal audio --- 
                if 'vocals' in songFiles:
                    # --- Load vocal file --- 
                    y, sr = librosa.load(file_path, sr=None)
                    
                    # --- Perform STFT to convert audio to mel spectrogram S --- 
                    D = np.abs(librosa.stft(y))**2
                    S_vocal = librosa.feature.melspectrogram(S=D, sr=sr)

                    # --- Add spectrogram to dataframe --- 
                    new_row = {'label': 'vocal', 'spectrogram': S_vocal}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

                    
                # --- Transform instrumentals --- 
                elif ('drums' or 'bass' or 'other' in songFiles) and instrumentals == False:
                    # --- Merge drums, bass, and other files --- 
                    drums = nested_path + "/" + "drums.wav"
                    bass = nested_path + "/" + "bass.wav"
                    other = nested_path + "/" + "other.wav"

                    drums_Segment = AudioSegment.from_file(drums)
                    bass_Segment = AudioSegment.from_file(bass)
                    other_Segment = AudioSegment.from_file(other)

                    combined = drums_Segment.overlay(bass_Segment).overlay(other_Segment)
                    
                    # --- EXPORT TO TEMP AUDIO AND LOAD TO LIBROSA
                    # Export to a temporary WAV file
                    temp_wav_path = "temp_mixed.wav"
                    combined.export(temp_wav_path, format="wav")

                    # Load into librosa
                    y, sr = librosa.load(temp_wav_path, sr=None)  # sr=None keeps the original sample rate
                    
                    # --- Perform STFT to convert audio to mel spectrogram S --- 
                    D = np.abs(librosa.stft(y))**2
                    S_instrumental = librosa.feature.melspectrogram(S=D, sr=sr)

                    # --- Add spectrogram to dataframe --- 
                    new_row = {'label': 'instrumental', 'spectrogram': S_instrumental}
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)


                    instrumentals = True
        log_file.close()
        
        # --- Write dataframe to csv dataset ---
        df.to_csv('dataset.csv', index=False) 

    except Exception as e:
        print("Error",e)


dataset_preprocess(folder_path)