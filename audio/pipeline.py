import librosa
import numpy as np

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
        # still a bit confused why i need to put these here and not in features
        self.window_size = 1024
        self.position = 0

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

        rms_value = np.sqrt(np.mean(window**2)) # root mean square
        self.position = self.position + self.window_size # move window to next position

        return{"amplitude": rms_value} # amplitutude

    