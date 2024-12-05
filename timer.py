import time
import random
import os
import platform
import sys
import tkinter as tk
from tkinter import ttk
import winsound


def beep(volume=100):
    if platform.system() == "Windows":
        winsound.PlaySound(r'\notification.wav', winsound.SND_FILENAME)
    elif platform.system() == "Darwin":
        os.system('say "Time is up"')
    else:
        sys.stdout.write('\a')
        sys.stdout.flush()


def parse_time_input(time_input):
    if ":" in time_input:
        mins, secs = map(int, time_input.split(":"))
    else:
        mins, secs = int(time_input), 0
    return mins * 60 + secs


def update_timer_display(label, countdown_time):
    mins, secs = divmod(countdown_time, 60)
    timer_display = f'{mins:02d}:{secs:02d}'
    label.config(text=timer_display)


def continuous_timer(min_seconds, max_seconds):
    root = tk.Tk()
    root.title("Countdown Timer")
    label = tk.Label(root, font=("Helvetica", 48))
    label.pack(pady=20)

    is_running = [False]
    countdown_time = [0]
    timer_thread = [None]
    volume = [100]

    def start_countdown():
        countdown_time[0] = random.randint(min_seconds, max_seconds)
        is_running[0] = True
        run_countdown()

    def run_countdown():
        if is_running[0] and countdown_time[0] >= 0:
            update_timer_display(label, countdown_time[0])
            countdown_time[0] -= 1
            timer_thread[0] = root.after(1000, run_countdown)
        elif countdown_time[0] < 0:
            print("Time's up!")
            beep(volume[0])
            time.sleep(1)
            start_countdown()

    def pause_countdown():
        is_running[0] = False
        if timer_thread[0] is not None:
            root.after_cancel(timer_thread[0])

    def resume_countdown():
        if not is_running[0]:
            is_running[0] = True
            run_countdown()

    def stop_countdown():
        is_running[0] = False
        if timer_thread[0] is not None:
            root.after_cancel(timer_thread[0])
        update_timer_display(label, 0)

    def set_volume(value):
        volume[0] = int(float(value))
        print(f"Volume set to {volume[0]}%")

    # Control buttons
    control_frame = tk.Frame(root)
    control_frame.pack(pady=10)

    start_button = tk.Button(control_frame, text="Start", command=start_countdown)
    start_button.grid(row=0, column=0, padx=5)

    pause_button = tk.Button(control_frame, text="Pause", command=pause_countdown)
    pause_button.grid(row=0, column=1, padx=5)

    resume_button = tk.Button(control_frame, text="Resume", command=resume_countdown)
    resume_button.grid(row=0, column=2, padx=5)

    stop_button = tk.Button(control_frame, text="Stop", command=stop_countdown)
    stop_button.grid(row=0, column=3, padx=5)

    # Volume slider
    volume_slider = ttk.Scale(root, from_=0, to=100, orient='horizontal', command=set_volume)
    volume_slider.set(100)  # Default volume at 100%
    volume_slider.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    min_interval_input = input("Enter the minimum interval (minutes or minutes:seconds): ")
    max_interval_input = input("Enter the maximum interval (minutes or minutes:seconds): ")

    min_interval = parse_time_input(min_interval_input)
    max_interval = parse_time_input(max_interval_input)

    if min_interval > max_interval:
        print("Minimum interval should be less than or equal to the maximum interval.")
    else:
        continuous_timer(min_interval, max_interval)