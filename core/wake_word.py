"""
Wake word detection for EDITH.
Uses openWakeWord. Place a trained 'hey_edith.onnx' in models/ for best results.
Falls back to a simple energy-based trigger if model not found.
"""

import numpy as np
import sounddevice as sd
from pathlib import Path

try:
    from openwakeword.model import Model
    OPENWAKEWORD_AVAILABLE = True
except ImportError:
    OPENWAKEWORD_AVAILABLE = False
    print("[WakeWord] openWakeWord not installed. Using fallback energy detector.")


class WakeWordDetector:
    def __init__(self, model_path: str = "models/hey_edith.onnx", threshold: float = 0.5):
        self.model_path = Path(model_path)
        self.threshold = threshold
        self.model = None
        self.sample_rate = 16000
        self.chunk_size = 1280

        if OPENWAKEWORD_AVAILABLE and self.model_path.exists():
            try:
                self.model = Model(wakeword_models=[str(self.model_path)])
                print(f"[WakeWord] Loaded custom model: {self.model_path}")
            except Exception as e:
                print(f"[WakeWord] Failed to load model: {e}")
                self.model = None
        else:
            print("[WakeWord] No custom model found. Using energy-based fallback.")
            print("          Train a real 'Hey Edith' model for best results.")

    def listen_once(self, timeout: float = 5.0) -> bool:
        if self.model is not None:
            return self._listen_openwakeword(timeout)
        else:
            return self._listen_energy(timeout)

    def _listen_openwakeword(self, timeout: float) -> bool:
        print("[WakeWord] Listening for 'Hey Edith'...")

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32") as stream:
            for _ in range(int(timeout * self.sample_rate / self.chunk_size)):
                audio, _ = stream.read(self.chunk_size)
                audio = audio.flatten()
                prediction = self.model.predict(audio)
                for score in prediction.values():
                    if score > self.threshold:
                        print("[WakeWord] 'Hey Edith' detected!")
                        return True
        return False

    def _listen_energy(self, timeout: float) -> bool:
        print("[WakeWord] Energy fallback active – speak loudly to trigger.")
        duration = 0.5
        threshold = 0.02

        with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype="float32") as stream:
            while True:
                audio, _ = stream.read(int(self.sample_rate * duration))
                energy = np.sqrt(np.mean(audio**2))
                if energy > threshold:
                    print("[WakeWord] Energy trigger activated!")
                    return True
                if timeout > 0:
                    timeout -= duration
                    if timeout <= 0:
                        return False
