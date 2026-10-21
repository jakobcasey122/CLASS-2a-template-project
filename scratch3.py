import numpy as np
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline("audio/track.wav")
pipeline.load()

window = 1024
totalwindows = len(pipeline.signal) // window # // means divide and round
print("Overall windows", totalwindows)

amplitutdes = [] 
# putting amplitutdes in a list the loop will add to it using append
# still think for loops are my weakest point, this took me a little to get
for i in range(totalwindows):
    amplitutde = pipeline.get_features()
    amplitutdes.append(amplitutde["amplitude"]) # append amplitude to the list

# then need to find smallest and largest

smallamp = min(amplitutdes)
largeamp = max(amplitutdes)

print("Smallest amplitude", smallamp)
print("Largest amplitude", largeamp)
