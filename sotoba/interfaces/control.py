import threading
import time
import tkinter as tk


FRAME_RATE = 60

TIMER_FUNCTION = time.perf_counter
MIN_SLEEP_TIME = 0.002


class Controller:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self.is_alive = True
        self.task_state = "free"
        self.task_thread = threading.Thread(target=self.loop)

        self.frame_rate = FRAME_RATE

        self.root.protocol("WM_DELETE_WINDOW", self.terminate)

    def start(self) -> None:
        self.task_thread.start()

    def terminate(self) -> None:
        self.is_alive = False
        self.task_thread.join()
        self.root.after_idle(self.root.quit)

    def loop(self) -> None:
        while self.is_alive:
            start_time = TIMER_FUNCTION()

            # Wait if self.update is already running
            if self.task_state == "busy":
                while self.is_alive:
                    if self.task_state == "free":
                        break
                    time.sleep(MIN_SLEEP_TIME)

            end_time = TIMER_FUNCTION()
            delta_time = end_time - start_time
            sleep_time = max(MIN_SLEEP_TIME, 1/self.frame_rate - delta_time)
            time.sleep(sleep_time)

    def update(self) -> None:
        self.task_state = "busy"

        # Update the window
        self.root.update_idletasks()

        self.task_state = "free"
