from tkinter import *
from datetime import datetime
import pygame
import os
import pytz

class TimerBase:
    def __init__(self):
        self.window = Tk()
        self.window.title("Pomodoro Timer")
        
        # Common attributes for any timer
        self.running = False
        self.time = 1500
        self.timer_id = None
        
        # Create main UI frame
        self.main_frame = Frame(self.window, bg="#FEF8E3")
        self.main_frame.pack(pady=20)
        
        # Create basic settings
        self.create_settings()
        
    def create_settings(self):        
        self.settings_frame = Frame(self.window, bg="#C8FAB5")
        
    def open_settings(self):
        if self.running:
            return
        self.main_frame.pack_forget()
        self.settings_frame.pack(pady=20)
        
    def hide_settings(self):
        self.settings_frame.pack_forget()
        self.main_frame.pack(pady=20)

    def save_settings(self):
        try:
            work_minutes = float(self.work_entry.get())
            srest_minutes = float(self.srest_entry.get())
            lrest_minutes = float(self.lrest_entry.get())

            if work_minutes <= 0 or srest_minutes <= 0 or lrest_minutes <= 0:
                raise ValueError("Time must be positive")

            self.work_time = int(work_minutes * 60)
            self.srest_time = int(srest_minutes * 60)
            self.lrest_time = int(lrest_minutes * 60)
            self.reset_timer()
            self.hide_settings()

        except ValueError:
            error_label = Label(self.settings_frame, text="Please enter valid numbers!", fg="red", bg="#C8FAB5")
            error_label.grid(row=4, column=0, columnspan=2, pady=5)
            self.window.after(2000, error_label.destroy)

    def update_display(self):
        # Base method for updating display
        pass
        
    def start_timer(self):
        # Base method for starting timer
        pass