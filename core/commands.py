"""
Simple command handler for EDITH.
Keeps device access limited and safe.
"""

import subprocess
import platform
import psutil
import webbrowser
from datetime import datetime


class CommandHandler:
    def __init__(self, brain):
        self.brain = brain
        self.system = platform.system()

    def handle(self, text: str) -> str | None:
        lower = text.lower().strip()

        if lower.startswith("open "):
            app = lower.replace("open ", "").strip()
            return self._open_app(app)

        if any(k in lower for k in ["cpu", "memory", "ram", "system info", "how is my computer"]):
            return self._system_info()

        if "what time" in lower or "current time" in lower:
            return f"The current time is {datetime.now().strftime('%I:%M %p')}."

        if "what day" in lower or "what date" in lower:
            return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

        if lower.startswith("search ") or lower.startswith("google ") or "search the web for" in lower:
            query = lower.replace("search ", "").replace("google ", "").replace("search the web for ", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"Searching the web for {query}."

        if "news" in lower or "headlines" in lower:
            return self._get_simple_news()

        for mode in ["luffy", "nami", "robin", "zoro", "default"]:
            if f"switch to {mode}" in lower or f"{mode} mode" in lower:
                self.brain.set_mode(mode)
                return f"Switched to {mode.capitalize()} mode. Ready when you are."

        return None

    def _open_app(self, app: str) -> str:
        try:
            if self.system == "Windows":
                subprocess.Popen(["start", app], shell=True)
            elif self.system == "Darwin":
                subprocess.Popen(["open", "-a", app])
            else:
                subprocess.Popen([app])
            return f"Opening {app}."
        except Exception as e:
            return f"Could not open {app}. Error: {e}"

    def _system_info(self) -> str:
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        return (
            f"CPU usage is {cpu}%. "
            f"Memory is {mem.percent}% used "
            f"({round(mem.used/1024**3, 1)} GB of {round(mem.total/1024**3, 1)} GB)."
        )

    def _get_simple_news(self) -> str:
        return (
            "I can fetch headlines when online. "
            "For now, try asking me about a specific topic or say 'search news about ...' "
            "so I can open a search for you."
        )
