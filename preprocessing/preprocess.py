import librosa
import numpy as np
import matplotlib.pyplot as plt

audio = r"./Wavfiles/Cristina Vane - So Easy/bass.wav"

'''FUNCTION TO PREPROCESS AUDIO FILE AND TURN IT INTO MEL SPECTROGRAM'''
def preprocess(audio):
    # --- Perform STFT to convert audio to mel spectrogram S --- 
    y, sr = librosa.load(audio, sr=None)
    D = np.abs(librosa.stft(y))**2
    S = librosa.feature.melspectrogram(S=D, sr=sr)

    # --- Plot the spectrogram --- 
    fig, ax = plt.subplots()
    S_dB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_dB, x_axis='time',
                            y_axis='mel', sr=sr,
                            fmax=8000, ax=ax)
    fig.colorbar(img, ax=ax, format='%+2.0f dB')
    ax.set(title='Mel-frequency spectrogram')
    plt.show()
    return S

preprocess(audio)
