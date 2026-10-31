# 🏴‍☠️ EDITH – One Piece Themed Local AI Assistant

**Even Dead, I'm The Hero** — Your personal voice AI with a cartoon One Piece crew vibe.

Wake word: **"Hey Edith"**  
Female voice · Local-first · Cartoon UI · Works on low-end PCs

---

## Current Status (v0.1 Desktop MVP)

| Feature                      | Status          | Notes |
|-----------------------------|-----------------|-------|
| Wake word "Hey Edith"       | Ready           | Uses openWakeWord (train custom model) |
| Speech-to-Text              | Working         | faster-whisper (tiny/base) |
| Local LLM brain             | Working         | Ollama (llama3.2:1b / 3b recommended) |
| Female neural TTS           | Working         | edge-tts |
| Cartoon One Piece UI        | Working         | CustomTkinter – straw hat theme |
| Basic commands              | Working         | Search, open apps, system info, news |
| Screen vision               | Not yet         | Planned |
| Full device control         | Limited         | Basic only |
| Mobile (Android/iOS)        | Skeleton only   | See `mobile/` folder |

---

## Quick Start (Desktop)

### 1. Requirements
- Python 3.10 – 3.12
- 4 GB+ RAM recommended (2 GB possible with tiny models)
- Microphone + speakers
- Ollama → https://ollama.com

### 2. Install
```bash
cd edith-ai
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
