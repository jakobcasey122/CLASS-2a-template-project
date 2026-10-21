import numpy as np
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline("audio/track.wav")
pipeline.load()

# list of amplitutes for 200 frames

pipeline.window_size = 256 # changes the window size so i dont forget to edit the main file later
amplitutdes = []

for i in range(200):
    amplitutde = pipeline.get_features() # we already have amplitutde values here
    amplitutdes.append(amplitutde)
    print(amplitutdes)
    # we have a list of amplitutdes but need the difference

difference = max(amplitutdes) - min(amplitutdes)

print("Jump ", difference)