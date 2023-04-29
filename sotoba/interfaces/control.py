import copy
import threading
import time
import tkinter as tk

from sotoba.interfaces.graphics import Graphics
from sotoba.models import entities


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
        self.root.protocol("WM_DELETE_WINDOW", self.terminate)

        self.frame_rate = FRAME_RATE
        self.fr_counter = FrameRateCounter()
        self.debug_screen = DebugScreen(self.gfx)

        self.key_detector = KeyDetector(self.root)

        # [!] just for debugging
        self.player = entities.Playable(self.gfx, 1, 112)

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

        # Capture the current state of sets of detected keys
        detected_keys_locked = copy.deepcopy(self.key_detector.detected_keys)
        dtkl = detected_keys_locked

        # [!] just for debugging
        self.player.operate(dtkl)

        # Update the key detector
        self.debug_screen.change_info(pressed_keys=dtkl["pressed"],
                                      released_keys=dtkl["released"],
                                      remaining_keys=dtkl["remaining"])
        self.key_detector.update()

        # Update the window
        self.root.update_idletasks()

        self.task_state = "free"


class KeyDetector:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root

        self.detected_keys = {
            "pressed": set(), "released": set(), "remaining": set()
        }
        self.root.bind("<KeyPress>", self.press_key)
        self.root.bind("<KeyRelease>", self.release_key)

    def press_key(self, event: tk.Event) -> None:
        key_code = event.keycode
        # Prevent a key from being pressed serially
        if key_code not in self.detected_keys["remaining"]:
            self.detected_keys["pressed"].add(key_code)
        self.detected_keys["remaining"].add(key_code)

    def release_key(self, event: tk.Event) -> None:
        key_code = event.keycode
        self.detected_keys["released"].add(key_code)
        self.detected_keys["remaining"].remove(key_code)

    def update(self) -> None:
        self.detected_keys["pressed"].clear()
        self.detected_keys["released"].clear()


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

        self.info = {
            "frame_rate": None, "pressed_keys": None, "released_keys": None,
            "remaining_keys": None
        }
        self.text = self.gfx.add_text(0, 0, self.info_str)

    @property
    def info_str(self) -> str:
        frame_rate = self.info["frame_rate"]
        product = f"{frame_rate} FPS\n" if frame_rate != None else "-- FPS\n"

        key_tags = ["pressed_keys", "released_keys", "remaining_keys"]
        for kind_of_detected_keys in key_tags:
            detected_keys = self.info[kind_of_detected_keys]
            product += f"{kind_of_detected_keys[0:3]}: "
            if detected_keys == None:
                product += "--\n"
                continue
            if len(detected_keys) == 0:
                product += "--\n"
                continue
            product += f"{', '.join(map(str, detected_keys))}\n"

        return product

    def change_info(self, **kwargs) -> None:
        for key in kwargs:
            value = kwargs[key]
            self.info[key] = value
        self.gfx.configure(self.text, text=self.info_str)
