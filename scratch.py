# scratch file for workshop

import librosa
import numpy as np

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

sampleamount = len(pipeline.signal)

print(pipeline.sample_rate)
print(sampleamount)
print(pipeline.signal.dtype)
print(sampleamount / pipeline.sample_rate)

# task 3:
t3samplewindow = 1024
t3start = len(pipeline.signal) // 2 # // means divide and round
t3window = pipeline.signal[t3start:t3start + t3samplewindow]

#peak and root mean square
t3peak = np.max(t3window)
#** = square other two self explanatory
t3rms = np.sqrt(np.mean(t3window**2))

print(t3peak, t3rms)

# peak is 0.0653737 rms is 0.028038038

# peak will always be bigger than rms because peak 
# was the highest number in the window meaning a 
# bunch of averaged numbers that are mostly 
# lower than it can never be higher

# task 4 quiet first

t4samplewindow = 1024
# should be the start of the signal
t4start = len(pipeline.signal) - len(pipeline.signal) + 1
t4window = pipeline.signal[t4start:t4start + t4samplewindow]

#peak and root mean square
t4peak = np.max(t4window)
t4rms = np.sqrt(np.mean(t4window**2))

print(t4peak, t4rms)

# peak is 0.00077466184 rms is 0.00022390219

# now the loud part i googled how to find a specific moment
# i want: seconds * 22050 = sample number

t4loudstart = 140 * 22050
t4loudwindow = pipeline.signal[t4loudstart:t4loudstart + t4samplewindow]

#peak and root mean square
t4loudpeak = np.max(t4loudwindow)
t4loudrms = np.sqrt(np.mean(t4loudwindow**2))

print(t4loudpeak, t4loudrms)

# peak is 0.7172493 rms is 0.026198218

# quieter window is larger, showing that the music is
# more dynamic which makes sense since the beginning
# of music usually builds up
