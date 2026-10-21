import numpy as np
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline("audio/track.wav")
pipeline.load()



# i actually just printed it a bunch of times but
# it just returned the same number 
# i also tried putting amplitutde = pipeline.get_features() 
# outside the loop but that would be just doing the same as 
# printing it a bunch of times

for i in range(3):
    amplitutde = pipeline.get_features()
    print(i, amplitutde)

# i need to find the rms of one of the above windows
# found this part quite difficult but it makes sense now
# was originally trying to put it in the for loop but
# the values i need to rms already exist

rms = np.sqrt(np.mean(pipeline.signal[1024:2048]**2)) # everything between 1024 and 2048 samples
print("RMS:", rms) # taking rms of that
