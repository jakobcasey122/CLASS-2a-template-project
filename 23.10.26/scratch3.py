import numpy as np
import librosa

from audio.pipeline import AudioPipeline

pipeline = AudioPipeline(file_path="audio/track.wav")
pipeline.load()

totalwindows = len(pipeline.signal) // pipeline.window_size

amplitudes = []
bass = []
mid = []
treble = []
centroid = []

for i in range(totalwindows):
    features = pipeline.get_features()

    amplitudes.append(features["amplitude"])
    bass.append(features["bass"])
    mid.append(features["mid"])
    treble.append(features["treble"])
    centroid.append(features["centroid"])

print("minimum amplitude ", round(min(amplitudes)))
print("minimum bass ", round(min(bass)))
print("minimum mid ", round(min(mid)))
print("minimum treble ", round(min(treble)))
print("minimum centroid ", round(min(centroid)))

print("---------")

print("maximum amplitude ", round(max(amplitudes)))
print("maximum bass ", round(max(bass)))
print("maximum mid ", round(max(mid)))
print("maximum treble ", round(max(treble)))
print("maximum centroid ", round(max(centroid)))