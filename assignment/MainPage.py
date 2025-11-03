from tkinter import *
from datetime import datetime
from TimerBase import *
from password import *
from PomodoroTimer import *
from MyNotes import MyNotes
from tkinter import messagebox, filedialog, colorchooser
import json
import pygame
import os
import pytz

# Import the class instead of using import *
from expensetracker import ExpenseTracker

class MainPage:
    def __init__(self):
        self.window = Tk()
        self.window.title("Main Page")
        
        self.main_frame = Frame(self.window)
        self.main_frame.pack(pady=20)
        self.expensebt=PhotoImage(file="mainpictures/mainexpense.png")
        self.pomodorobt=PhotoImage(file="mainpictures/mainpomodoro.png")
        self.notebt=PhotoImage(file="mainpictures/mainmynotes.png")
        Button(self.main_frame, image=self.expensebt, command=self.open_expenses).pack(side=LEFT)
        Button(self.main_frame, image=self.notebt, command=self.open_notes).pack(side=LEFT)
        Button(self.main_frame, image=self.pomodorobt, command=self.open_pomodoro).pack(side=LEFT)
        
        self.window.mainloop()
    
    def open_expenses(self):
        # Pass the main window as parent
        ExpenseTracker(self.window)

    def open_notes(self):
        notes_window = Toplevel(self.window)
        app = MyNotes(notes_window)
        
    def open_pomodoro(self): 
        app = PomodoroTimer()

if __name__ == "__main__":
    app = MainPage()