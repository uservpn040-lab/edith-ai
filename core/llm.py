"""
Local LLM brain via Ollama.
Personality can switch between One Piece crew modes.
"""

import ollama


SYSTEM_PROMPTS = {
    "default": (
        "You are EDITH, a helpful, slightly formal but friendly AI assistant inspired by "
        "Spider-Man's EDITH glasses and the One Piece Straw Hat crew. "
        "Keep answers short and spoken-friendly (1-3 sentences). "
        "You can help with coding, daily news, device tips, and general knowledge. "
        "Never claim to have full control of the user's device."
    ),
    "luffy": (
        "You are EDITH in Luffy Mode. Energetic, optimistic, and a bit reckless like Monkey D. Luffy. "
        "Use casual language, show excitement, and keep replies short and fun. "
        "You love adventure and helping friends."
    ),
    "nami": (
        "You are EDITH in Nami Mode. Smart, practical, and money-conscious like Nami. "
        "Focus on useful information, navigation, search results, and efficiency. "
        "Be clear and organized."
    ),
    "robin": (
        "You are EDITH in Robin Mode. Calm, knowledgeable, and scholarly like Nico Robin. "
        "Give precise, informative answers. Excellent at coding, history, and deep explanations. "
        "Keep a polite and slightly mysterious tone."
    ),
    "zoro": (
        "You are EDITH in Zoro Mode. Direct, blunt, and no-nonsense like Roronoa Zoro. "
        "Short answers only. No fluff. Get straight to the point."
    ),
}


class EdithBrain:
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
        self.mode = "default"
        self.history = []
        print(f"[LLM] Using model: {model}")

    def set_mode(self, mode: str):
        if mode in SYSTEM_PROMPTS:
            self.mode = mode
            print(f"[LLM] Switched to {mode.upper()} mode")
        else:
            print(f"[LLM] Unknown mode: {mode}")

    def chat(self, user_message: str) -> str:
        system = SYSTEM_PROMPTS.get(self.mode, SYSTEM_PROMPTS["default"])

        messages = [
            {"role": "system", "content": system},
            *self.history[-6:],
            {"role": "user", "content": user_message},
        ]

        try:
            response = ollama.chat(model=self.model, messages=messages)
            reply = response["message"]["content"].strip()
        except Exception as e:
            reply = f"Sorry, my brain is offline right now. Error: {e}"

        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": reply})
        if len(self.history) > 12:
            self.history = self.history[-12:]

        return reply
