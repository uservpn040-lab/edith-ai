#!/usr/bin/env python3
"""
EDITH – One Piece Themed Local AI Assistant
Desktop MVP v0.1
"""

import customtkinter as ctk
from ui.main_window import EdithMainWindow
import sys

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = EdithMainWindow()
    app.mainloop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEDITH shutting down... See you on the Grand Line!")
        sys.exit(0)
