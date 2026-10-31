"""
Cartoon One Piece themed main window for EDITH.
"""

import customtkinter as ctk
import threading
from core.wake_word import WakeWordDetector
from core.stt import SpeechToText
from core.llm import EdithBrain
from core.tts import TextToSpeech
from core.commands import CommandHandler


class EdithMainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EDITH  •  Straw Hat AI")
        self.geometry("520x720")
        self.minsize(420, 600)

        self.colors = {
            "bg": "#0f0f1a",
            "card": "#1a1a2e",
            "accent": "#e94560",
            "accent2": "#0f3460",
            "gold": "#f5a623",
            "text": "#eaeaea",
            "muted": "#a0a0b0",
        }

        self.configure(fg_color=self.colors["bg"])

        self.wake = WakeWordDetector()
        self.stt = SpeechToText(model_size="tiny")
        self.brain = EdithBrain(model="llama3.2:1b")
        self.tts = TextToSpeech(voice="en-US-AriaNeural")
        self.commands = CommandHandler(self.brain)

        self.is_listening = False
        self.current_mode = "default"

        self._build_ui()
        self._update_status("Ready. Say \"Hey Edith\" or press the button.")

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color=self.colors["card"], corner_radius=16)
        header.pack(fill="x", padx=16, pady=(16, 8))

        title = ctk.CTkLabel(
            header,
            text="EDITH",
            font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"),
            text_color=self.colors["gold"]
        )
        title.pack(pady=(12, 0))

        subtitle = ctk.CTkLabel(
            header,
            text="Even Dead, I'm The Hero  •  Straw Hat Edition",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"]
        )
        subtitle.pack(pady=(0, 12))

        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(mode_frame, text="Crew Mode:", text_color=self.colors["muted"]).pack(side="left")

        self.mode_var = ctk.StringVar(value="default")
        modes = [("Default", "default"), ("Luffy", "luffy"), ("Nami", "nami"), ("Robin", "robin"), ("Zoro", "zoro")]
        for label, value in modes:
            btn = ctk.CTkRadioButton(
                mode_frame,
                text=label,
                variable=self.mode_var,
                value=value,
                command=self._on_mode_change,
                fg_color=self.colors["accent"],
                hover_color=self.colors["gold"]
            )
            btn.pack(side="left", padx=6)

        self.chat_box = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(size=14),
            fg_color=self.colors["card"],
            text_color=self.colors["text"],
            corner_radius=16,
            wrap="word"
        )
        self.chat_box.pack(fill="both", expand=True, padx=16, pady=8)
        self.chat_box.insert("end", "🏴‍☠️ Welcome aboard!\n\nI'm EDITH. Say \"Hey Edith\" or press the mic button to talk.\n")
        self.chat_box.configure(state="disabled")

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["muted"]
        )
        self.status_label.pack(pady=(0, 4))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=16, pady=(4, 16))

        self.mic_btn = ctk.CTkButton(
            btn_frame,
            text="🎤  Talk to EDITH",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            fg_color=self.colors["accent"],
            hover_color="#c73e54",
            corner_radius=25,
            command=self._on_mic_press
        )
        self.mic_btn.pack(side="left", expand=True, fill="x", padx=(0, 8))

        self.wake_btn = ctk.CTkButton(
            btn_frame,
            text="👂 Listen for\nHey Edith",
            font=ctk.CTkFont(size=12),
            height=50,
            width=120,
            fg_color=self.colors["accent2"],
            hover_color="#1a4a7a",
            corner_radius=16,
            command=self._start_wake_listen
        )
        self.wake_btn.pack(side="right")
