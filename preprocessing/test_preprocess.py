from preprocess import preprocess
import numpy as np
import matplotlib.pyplot as plt

plt.imshow(preprocess, cmap='viridis')
plt.colorbar()

plt.title("Mel-Spectrogram of Audio File")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

plt.show()