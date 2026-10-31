"""
Speech-to-Text using faster-whisper (CPU friendly).
"""

from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import tempfile
import soundfile as sf
from pathlib import Path


class SpeechToText:
    def __init__(self, model_size: str = "tiny", device: str = "cpu", compute_type: str = "int8"):
        print(f"[STT] Loading Whisper model '{model_size}' on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        self.sample_rate = 16000
        print("[STT] Ready.")

    def record(self, duration: float = 6.0) -> np.ndarray:
        print(f"[STT] Recording for {duration}s... Speak now.")
        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="float32"
        )
        sd.wait()
        return audio.flatten()

    def transcribe(self, audio: np.ndarray) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            sf.write(f.name, audio, self.sample_rate)
            segments, info = self.model.transcribe(f.name, beam_size=1, language="en")
            text = " ".join([seg.text for seg in segments]).strip()
        Path(f.name).unlink(missing_ok=True)
        return text

    def listen_and_transcribe(self, duration: float = 6.0) -> str:
        audio = self.record(duration)
        text = self.transcribe(audio)
        print(f"[STT] Heard: {text}")
        return text
