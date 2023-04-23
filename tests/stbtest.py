import os
import sys
import tkinter as tk

PROJECT_DIR = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(PROJECT_DIR)

from sotoba.interfaces.window import Window


def main() -> int:
    root = tk.Tk()
    window = Window(root)

    root.after(1000, window.controller.start)
    root.mainloop()

    if window.controller.task_thread.is_alive():
        print(window.controller.is_alive)
        window.controller.task_thread.join()
    print(window.controller.task_thread.is_alive())

    return 0


sys.exit(main())
