import numpy as np
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

# task 5

# frequency is f = bin position * sample rate / window size
# so bin position = f * window size / sample rate

# task asks for 2 numbers to split, thats why no mid

bassFreq = 250
trebleFreq = 4000
# rounding for whole bin number
bassbinEdge = round(bassFreq * 1024 / 22050) 
treblebinEdge = round(trebleFreq * 1024 / 22050)

print("Bass bin " + str(bassbinEdge))
print("Treble bin " + str(treblebinEdge))

# task 6
print("------------------")

pipeline.position = 3087000

inputarray = pipeline.signal[pipeline.position:pipeline.position + 1024] * np.hanning(1024)
magnitude = np.abs(np.fft.rfft(inputarray))

midMagnitude = magnitude[bassbinEdge:treblebinEdge] # mid i think (i was right)
bassMagnitude = magnitude[1:bassbinEdge] # bass 
trebleMagnitude = magnitude[treblebinEdge:] # treble

# im taking "which band dominates" to mean how many bins fit in 512 (half the window size)

print("Treble bins " + str(len(trebleMagnitude)))
print("Mid bins " + str(len(midMagnitude)))
print("Bass bins " + str(len(bassMagnitude)))

# treble dominates at 327

# task 7
print("------------------")

pipeline.position = 3087000
inputarray = pipeline.signal[pipeline.position:pipeline.position + 1024] 
# librosa does hanning for me https://librosa.org/doc/dev/api/generated/librosa.feature.spectral_centroid.html

spectralcentroid = librosa.feature.spectral_centroid(y=inputarray, sr=pipeline.sample_rate, n_fft=1024, center=False)

print("Loud part spectralcentroid " + str(spectralcentroid))

# now the sparse section

pipeline.position = 20480
inputarray = pipeline.signal[pipeline.position:pipeline.position + 1024]

spectralcentroid = librosa.feature.spectral_centroid(y=inputarray, sr=pipeline.sample_rate, n_fft=1024, center=False)

print("Sparse part spectralcentroid " + str(spectralcentroid))

# the sparse part is higher than the loud part
# bass pulls the average down during the loud part