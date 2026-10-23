import numpy as np  
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

pipeline.position = 3087000

inputarray = pipeline.position * np.hanning(1024)
magnitude = np.fft.rfft(inputarray * 1024)

print(magnitude)
index = np.argmax(magnitude[1:513])
frequency = 

print(frequency)
