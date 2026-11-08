import librosa
import numpy as np

# frequency is f = bin position * sample rate / window size
# bin position = f * window size / sample rate

class AudioPipeline:
    """Loads an audio file and extracts features from it, frame by frame.

    Both load() and get_features() are stubs you must implement yourself —
    that's intentional, not an oversight. This unit is about the whole
    pipeline (data source -> feature extraction -> real-time rendering), not
    just feature extraction handed to you pre-solved.
    """

    def __init__(self, file_path: str, sample_rate: int = 22050) -> None:
        self.file_path = file_path
        self.sample_rate = sample_rate
        self.window_size = 1024
        self.position = 0
        self.bass_edge = round(250 * self.window_size / self.sample_rate) # setting edges and rounding for whole number
        self.treble_edge = round(4000 * self.window_size / self.sample_rate)
        self.previous_magnitude = np.zeros(self.window_size // 2 + 1) # a list of 513 zeros to store the previous magnitude

    def load(self) -> np.ndarray:
        self.signal, _ = librosa.load(self.file_path, sr=self.sample_rate)
        return self.signal
        """Load the audio file at self.file_path via librosa, at
        self.sample_rate, and store the resulting signal on the instance.
        """

    def get_features(self) -> dict:
        """Extract numerical features (amplitude at minimum) from the current
        window of the loaded signal, advance the pipeline's internal read
        position accordingly, and return them as a dict[str, float].

        This return value is passed directly into engine.update().
        """
        # making an if statement so if posiiton exceeds signal length it resets 
        # (it basicly loops when the song ends)
        if self.position + self.window_size > len(self.signal):
            self.position = 0

        # setting up the moving window, start is 0
        windowstart = self.position
        window = self.signal[windowstart:windowstart + self.window_size]
        rms_value = np.sqrt(np.mean(window**2)) * 500 # amplitude from raw audio before split
        self.position = self.position + self.window_size # move window to next position

        # hann and fft the window, lines 30-31 scratch2 23.10.26
        hann_window = window * np.hanning(self.window_size)
        magnitude = np.abs(np.fft.rfft(hann_window))

        # seperate the bass, mid, and treble values from above
        bass_magnitude = magnitude[1:self.bass_edge]
        mid_magnitude = magnitude[self.bass_edge:self.treble_edge]
        treble_magnitude = magnitude[self.treble_edge:]

        # get a single number from these lists to give the engine
        bass = np.average(bass_magnitude)
        mid = np.average(mid_magnitude)
        treble = np.average(treble_magnitude)

        # centroid, lines 46 onwards scratch2 23.10.26 .item() gives a usable number
        centroid = librosa.feature.spectral_centroid(y=window, sr=self.sample_rate, n_fft=self.window_size, center=False).item()

        # onset / spectral flux
        spectral_flux = np.maximum(magnitude - self.previous_magnitude, 0) # changes negatives to 0, to ignore fading sound
        self.previous_magnitude = magnitude # update magnitude 
        onset = np.sum(spectral_flux) # add up spectral flux to get onset

        
        

        return{
            "amplitude": rms_value, 
            "bass": bass, 
            "mid": mid, 
            "treble": treble, 
            "centroid": centroid, 
            "onset": onset
        }

    