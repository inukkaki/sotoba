import threading
import time
import tkinter as tk

from sotoba.interfaces.graphics import Graphics


FRAME_RATE = 60

TIMER_FUNCTION = time.perf_counter
UNIT_TIME = 1
MIN_SLEEP_TIME = 0.002


class Controller:
    def __init__(self, root: tk.Tk, graphics: Graphics) -> None:
        self.root = root
        self.gfx = graphics

        self.is_alive = True
        self.task_state = "free"
        self.task_thread = threading.Thread(target=self.loop)

        self.frame_rate = FRAME_RATE
        self.fr_counter = FrameRateCounter()
        self.debug_screen = DebugScreen(self.gfx)

        self.root.protocol("WM_DELETE_WINDOW", self.terminate)

    def start(self) -> None:
        self.fr_counter.start()
        self.task_thread.start()

    def terminate(self) -> None:
        self.is_alive = False
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

            # Calculate the measured value of frame rate
            actual_frame_rate = self.fr_counter.calculate_frame_rate()
            if isinstance(actual_frame_rate, int):
                self.debug_screen.change_info(frame_rate=actual_frame_rate)

            # Call self.update (possibly with delay)
            self.root.after_idle(self.update)

            end_time = TIMER_FUNCTION()
            delta_time = end_time - start_time
            sleep_time = max(MIN_SLEEP_TIME, 1/self.frame_rate - delta_time)
            time.sleep(sleep_time)

    def update(self) -> None:
        self.task_state = "busy"

        # Update the window
        self.root.update_idletasks()

        self.task_state = "free"


class FrameRateCounter:
    def __init__(self) -> None:
        self.last_update_time = None
        self.passed_frames = None

    def start(self) -> None:
        self.last_update_time = TIMER_FUNCTION()
        self.passed_frames = 0

    def calculate_frame_rate(self) -> int | None:
        self.passed_frames += 1
        current_time = TIMER_FUNCTION()
        elapsed_time = current_time - self.last_update_time

        if elapsed_time < UNIT_TIME:
            return None
        actual_frame_rate = int(self.passed_frames/elapsed_time + 0.5)
        self.last_update_time = current_time
        self.passed_frames = 0
        return actual_frame_rate


class DebugScreen:
    def __init__(self, graphics: Graphics) -> None:
        self.gfx = graphics

        self.info = {"frame_rate": "--"}
        self.text = self.gfx.add_text(0, 0, self.info_str)

    @property
    def info_str(self) -> str:
        return f"{self.info['frame_rate']} FPS"

    def change_info(self, **kwargs) -> None:
        for key in kwargs:
            value = kwargs[key]
            self.info[key] = value
        self.gfx.configure(self.text, text=self.info_str)
