# EDITH Mobile (Flutter)

This is the planned mobile version.

## Recommended Approach (2026)

- **Flutter** for UI + cross-platform
- **Sherpa-ONNX** or openWakeWord for wake word on device
- **whisper.cpp** via FFI for STT
- Small local model (Gemma 2B / Llama 3.2 1B quantized)
- Or hybrid: local wake word + cloud LLM when online

## Existing inspiration

Look at the open-source project **Lilly** (Flutter + on-device Gemma + Sherpa ONNX) for a working example of a local voice assistant on Android.

## Next steps

1. `flutter create edith_mobile`
2. Add microphone + TTS plugins
3. Integrate a small ONNX wake-word model
4. Decide local vs hybrid brain

A full production mobile app requires significant native work. Start with the Desktop version first.
