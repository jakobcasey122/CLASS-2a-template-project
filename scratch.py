import numpy as np  
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

pipeline.position = 3087000

inputarray = pipeline.signal[pipeline.position:pipeline.position + 1024] * np.hanning(1024)
# bfore i was just doing 3087000 x hanning 1024 but that doesn't make 
# any sense, so im using a window of 1024 starting at 3087000 from
# the signal.
magnitude = np.abs(np.fft.rfft(inputarray)) 
# abs makes negatives positives, fft is fourier transform
print(len(magnitude)) # number of bins
# frequency is f = bin position * sample rate / window size
print(1*22050/1024) # first bin
print(512*22050/1024) # last bin

# task 2

index = np.argmax(magnitude[1:]) + 1 # you add one to get the real
# number since we removed one (bin 0)
hz = index * 22050 / 1024
print("Peak magnitude in loud part " + str(magnitude[index])) # finding argmax of magnitude and printing it
print("Frequency of the strongest bin in loud part " + str(hz))
# 150.7 hz, very bassy point in the song

# task 3
# now need a quiet window
print("------------------")

pipeline.position = 20480 # doing the beginning because its quiet

quietinputarray = pipeline.signal[pipeline.position:pipeline.position + 1024] * np.hanning(1024)
quietmagnitude = np.abs(np.fft.rfft(quietinputarray))

quietindex = np.argmax(quietmagnitude[1:]) + 1
quiethz = quietindex * 22050 / 1024
print("Peak magnitude in quiet part " + str(quietmagnitude[quietindex]))
print("Frequency of the strongest bin in quiet part " + str(quiethz))

# Loud part has a much higher peak magntitude but lower frequency
# Quiet part has a higher frequency but much lower magntitude

# task 4
# removing the hanning window
print("------------------")

pipeline.position = 3087000

nohanninginputarray = pipeline.signal[pipeline.position:pipeline.position + 1024]
nohanningmaxmagnitude = np.abs(np.fft.rfft(nohanninginputarray))

nohanningindex = np.argmax(nohanningmaxmagnitude[1:]) + 1

print("Stongest bin no hanning " + str(nohanningindex))
print("Strongest bin with hanning " + str(index))

# STILL NEED TO DO PT 2 OF TASK 4
# feeling very confident with slicing now!

print("No hanning magnitudes " + str(nohanningmaxmagnitude[nohanningindex:nohanningindex + 10]))
print("With hanning magnitudes " + str(magnitude[index:index + 10]))

