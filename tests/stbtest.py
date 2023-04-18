import os
import sys
import tkinter as tk

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(PROJECT_DIR)

from sotoba.interfaces.window import Window


def main() -> int:
    root = tk.Tk()
    window = Window(root)
    root.mainloop()
    return 0


sys.exit(main())
