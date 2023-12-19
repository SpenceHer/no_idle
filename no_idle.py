import tkinter as tk
from tkinter import ttk
import platform
import ctypes
import threading
import subprocess
import time

class NoIdleClass:
    def __init__(self):
        def center_window(window, width, height):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()

            x = (screen_width - width) // 2
            y = (screen_height - height) // 2

            window.geometry(f"+{x}+{y}")

        # Create the main window
        self.main_window = tk.Tk()
        self.main_window.configure(background="#FF69B4")
        self.main_window.title("No Idle Switch")

        # Set the window's dimensions
        window_width = 400
        window_height = 200

        # Center the window
        center_window(self.main_window, window_width, window_height)
        
        button_frame = tk.Frame(self.main_window, bg='#FFB6C1')
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a variable to control the selection
        selected_option = tk.StringVar()

        # Create "On" button as a Radiobutton
        self.on_button = tk.Radiobutton(button_frame, text="On", variable=selected_option, value="On", command=self.prevent_sleep)
        self.on_button.configure(indicator=0,
                            font=("Arial", 48),
                            fg='#FF69B4',
                            bg="#FFDAB9",
                            selectcolor="#FFD700",
                            highlightcolor='blue',
                            highlightthickness=0,
                            border=100,
                            borderwidth=10,
                            width=7)
        self.on_button.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Create "Off" button as a Radiobutton
        self.off_button = tk.Radiobutton(button_frame, text="Off", variable=selected_option, value="Off", command=self.allow_sleep)
        self.off_button.configure(indicator=0,
                            font=("Arial", 48),
                            fg='#FF69B4',
                            bg="#FFDAB9",
                            selectcolor="#FFD700",
                            highlightcolor='blue',
                            highlightthickness=0,
                            border=100,
                            borderwidth=10,
                            width=7)
        self.off_button.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.allow_sleep_flag = threading.Event()
        self.allow_sleep_flag.set()  # Initially, sleep is allowed

        # Start a timer to periodically run the prevent_sleep function in a separate thread
        threading.Thread(target=self.repeat_prevent_sleep, args=(60,)).start()

        # Start the GUI event loop
        self.main_window.mainloop()

    # Function to prevent sleep based on the operating system
    def prevent_sleep(self):
        self.on_button.configure(
                        bg="#FF69B4",
                        fg="#FFFFFF"
        )
        self.off_button.configure(
                        bg="#FFDAB9",
                        fg="#FF69B4"
        )
        self.allow_sleep_flag.clear()  # Prevent sleep

        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)

        elif platform.system() == "Darwin":  # macOS
            subprocess_thread = threading.Thread(target=lambda: subprocess.run(["caffeinate", "-d"]))
            subprocess_thread.start()

        elif platform.system() == "Linux":
            subprocess_thread = threading.Thread(target=lambda: subprocess.run(["xdg-screensaver", "suspend"]))
            subprocess_thread.start()

        else:
            print("Unsupported operating system")

    # Function to allow sleep based on the operating system
    def allow_sleep(self):
        self.off_button.configure(
                        bg="#FF69B4",
                        fg="#FFFFFF"
        )
        self.on_button.configure(
                        bg="#FFDAB9",
                        fg="#FF69B4"
        )

        self.allow_sleep_flag.set()  # Allow sleep

        if platform.system() == "Windows":
            ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)

        elif platform.system() == "Darwin":  # macOS
            subprocess_thread = threading.Thread(target=lambda: subprocess.run(["killall", "caffeinate"]))
            subprocess_thread.start()

        elif platform.system() == "Linux":
            subprocess_thread = threading.Thread(target=lambda: subprocess.run(["xdg-screensaver", "resume"]))
            subprocess_thread.start()

        else:
            print("Unsupported operating system")

    # Function to repeat the prevent_sleep function every 'interval' seconds
    def repeat_prevent_sleep(self, interval):
        while True:
            if not self.allow_sleep_flag.is_set():
                self.prevent_sleep()
            time.sleep(interval)

NoIdleClass()
