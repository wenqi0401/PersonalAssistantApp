from tkinter import *
from datetime import datetime
from TimerBase import *
from tkinter import messagebox
import pygame
import os
import pytz

class PomodoroTimer(TimerBase):
    def __init__(self):
        # Call parent class's __init__ first
        super().__init__()
        
        # Default time
        self.work_time = 1500    # 25 minutes
        self.srest_time = 300    # 5 minutes
        self.lrest_time = 900    # 15 minutes

        
        self.srest = False
        self.lrest = False
        self.current_task = ""
        self.task_dict = {}
        
        # Initialize sound
        pygame.mixer.init()
        self.setup_sound()

        # Load task dictionary from file
        self.task_dict = self.load_task_dict()
        
        # Create Pomodoro-specific UI elements
        self.create_pomodoro_ui()
        
        self.window.mainloop()

    def create_pomodoro_ui(self):
        # Task entry section
        self.task_frame = Frame(self.main_frame, bg="#FEF8E3")
        self.task_frame.pack(fill=X, padx=20, pady=10)

        #Task
        Label(self.task_frame, text="Current Task:", font=("Arial", 12), bg="#FEF8E3").pack(side=LEFT)
        self.task_entry = Entry(self.task_frame, font=("Arial", 12), width=30)
        self.task_entry.pack(side=LEFT, padx=5)
        Button(self.task_frame, text="Set Task", command=self.set_task, font=("Arial", 11), bg="#FFE88C").pack(side=LEFT, padx=5)

        # Task display
        self.task_display = Label(self.main_frame, text="No task set", font=("Arial", 12), wraplength=300, bg="#FEF8E3")
        self.task_display.pack(pady=10)

        # Completed tasks list
        Label(self.main_frame, text="Completed Tasks:", font=("Arial", 12), bg="#FEF8E3").pack(pady=(10,0))
        self.completed_tasks = Listbox(self.main_frame, font=("Arial", 11), width=40, height=5)
        self.completed_tasks.pack(pady=10)

        # Timer display
        self.label = Label(self.main_frame, text="25:00", font=("Arial", 48), bg="#FEF8E3")
        self.label.pack(pady=20)

        # Control buttons frame
        self.control_frame = Frame(self.main_frame, bg="#FEF8E3")
        self.control_frame.pack(pady=10)

        # Control buttons
        self.start_button = Button(self.control_frame, text="Start", command=self.start_timer, font=("Arial", 12), bg="#FFE88C")
        self.start_button.pack(side=LEFT, padx=5, pady=10)

        self.shortrest_button = Button(self.control_frame, text="Short Rest", command=self.start_sresttimer, font=("Arial", 12), bg="#FFE88C")
        self.shortrest_button.pack(side=LEFT, padx=5, pady=10)

        self.longrest_button = Button(self.control_frame, text="Long Rest", command=self.start_lresttimer, font=("Arial", 12), bg="#FFE88C")
        self.longrest_button.pack(side=LEFT, padx=5, pady=10)

        self.stop_button = Button(self.control_frame, text="Stop", command=self.stop_timer, font=("Arial", 12), bg="#FFE88C")
        self.stop_button.pack(side=LEFT, padx=5, pady=10)

        self.reset_button = Button(self.control_frame, text="Reset", command=self.reset_timer, font=("Arial", 12), bg="#FFE88C")
        self.reset_button.pack(side=LEFT, padx=5, pady=10)

        #Setting Button
        self.settings_button = Button(self.main_frame, text="⚙ Settings", command=self.open_settings, font=("Arial", 12), bg="#FBDD61")
        self.settings_button.pack(pady=10)
        
        # History button
        self.history_button = Button(self.main_frame, text = "Completed Tasks History", command=self.open_history, font=("Arial", 12), bg="#FCD53A")
        self.history_button.pack(pady=10)

        # Settings buttons
        Button(self.settings_frame, text="Save", command=self.save_settings, font=("Arial", 11), bg="#65C624").grid(row=3, column=1, pady=10)
        Button(self.settings_frame, text="Cancel", command=self.hide_settings, font=("Arial", 11), bg="#EC4345").grid(row=3, column=0, pady=10)
        
        # Create history frame
        self.history_frame = Frame(self.window, bg="#C8FAB5")

      

    
    def set_task(self):
        '''  
        -----------------------------------------------------------------------------------------------------
                                                  Task
        -----------------------------------------------------------------------------------------------------
        To handle the user input of task
        '''
        task = self.task_entry.get().strip().upper()
        if task:
            self.current_task = task
            count = self.task_display.config(text=f'Current Task: {task}')
            self.task_entry.delete(0, END)
        else:
            self.task_display.config(text="No task set")
            self.current_task = ""
            
    def complete_task(self):
        if self.current_task:
            # Update dictionary count
            self.task_dict[self.current_task] = self.task_dict.get(self.current_task, 0) + 1
            
            timestamp = datetime.now().strftime("%H:%M")
            completed = self.current_task
            self.completed_tasks.insert(0, f"{timestamp} - {completed} (#{self.task_dict[completed]})")
            
            # Save to history with count
            current_time = datetime.now(pytz.timezone('Asia/Kuala_Lumpur'))
            try:
                with open("History.txt", 'a') as f:
                    f.write(f"{current_time.day}/{current_time.month}/{current_time.year}|")
                    f.write(f"{current_time.hour}:{current_time.minute}:{current_time.second}|")
                    f.write(f"{completed} (#{self.task_dict[completed]})\n")
            except Exception as e:
                print(f"Error saving to history: {e}")
            
            # Clear current task after saving
            self.current_task = ""
            self.task_display.config(text="No task set", bg="#FEF8E3")

    def open_history(self):
        self.main_frame.pack_forget()
        self.history_frame.pack(pady=20)
        
        # Clear existing widgets
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        # Create button frame for better organization
        button_frame = Frame(self.history_frame, bg="#C8FAB5")
        button_frame.pack(side=BOTTOM, fill=X, pady=10)
        
        # Create scrolled text area
        scrollbar = Scrollbar(self.history_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        records = Text(self.history_frame, bg="#C8FAB5", wrap=WORD, height=20, width=50, 
                      yscrollcommand=scrollbar.set, padx=10, pady=10)
        records.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar.config(command=records.yview)
        
        try:
            with open("History.txt", 'r') as f:
                self.history = f.readlines()
                
                if len(self.history) > 0:
                    for line in self.history:
                        try:
                            date, time, task = line.strip().split('|')
                            record_text = (
                                f"Date: {date}\n"
                                f"Time: {time}\n"
                                f"Task: {task}\n"
                                f"--------------------------------------------------\n"
                            )
                            records.insert(END, record_text)
                        except ValueError:
                            continue
                else:
                    records.insert(END, "No completed task records found.")
        
        except FileNotFoundError:
            records.insert(END, "History file not found.")
        except Exception as e:
            records.insert(END, f"An error occurred: {str(e)}")
            
        records.config(state=DISABLED)
        
        # Add Back and Clear History buttons to button frame
        Button(button_frame, text="Back", 
               command=self.hide_history, 
               font=("Arial", 11), bg="#65C624").pack(side=LEFT, padx=5)
        
        Button(button_frame, text="Clear History", 
               command=lambda: self.clear_history(records), 
               font=("Arial", 11), bg="#EC4345").pack(side=LEFT, padx=5)

    def clear_history(self, text_widget):
        """Clear the history file and update the display"""
        try:
            # Check if file exists and has content
            if not os.path.exists("History.txt") or os.path.getsize("History.txt") == 0:
                messagebox.showinfo("No Data", "There is no history data to delete.")
                return
                
            # If there is data, ask for confirmation
            result = messagebox.askyesno("Clear History", 
                                        "Are you sure you want to clear all history?\nThis action cannot be undone.")
            if result:
                try:
                    # Clear the file
                    with open("History.txt", 'w') as f:
                        f.write("")
                    
                    # Clear the text widget
                    text_widget.config(state=NORMAL)
                    text_widget.delete(1.0, END)
                    text_widget.insert(END, "History has been cleared.")
                    text_widget.config(state=DISABLED)
                    
                    # Reset task dictionary
                    self.task_dict = {}
                    
                    messagebox.showinfo("Success", "History has been cleared successfully!")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred while clearing history: {str(e)}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking history: {str(e)}")


    def hide_history(self):
        """Hide history frame and show main frame"""
        self.history_frame.pack_forget()
        self.main_frame.pack(pady=20)



    def open_settings(self):
        '''  
        -----------------------------------------------------------------------------------------------------
                                                  Setting
        -----------------------------------------------------------------------------------------------------
        Allowed user to modify the default setting of the work time, short rest time, and long rest time
        ''' 
        # Override parent's open_settings to add Pomodoro-specific settings
        super().open_settings()  # Call parent method first
        
        # Work time settings
        Label(self.settings_frame, text="Work Time (minutes):", font=("Arial", 12), bg="#C8FAB5").grid(row=0, column=0, padx=5, pady=5)
        self.work_entry = Entry(self.settings_frame, width=10, font=("Arial", 12))
        self.work_entry.grid(row=0, column=1, padx=5, pady=5)
        self.work_entry.insert(0, "25")

        # Short rest time settings
        Label(self.settings_frame, text="Short Rest Time (minutes):", font=("Arial", 12), bg="#C8FAB5").grid(row=1, column=0, padx=5, pady=5)
        self.srest_entry = Entry(self.settings_frame, width=10, font=("Arial", 12))
        self.srest_entry.grid(row=1, column=1, padx=5, pady=5)
        self.srest_entry.insert(0, "5")

        # Long rest time settings
        Label(self.settings_frame, text="Long Rest Time (minutes):", font=("Arial", 12), bg="#C8FAB5").grid(row=2, column=0, padx=5, pady=5)
        self.lrest_entry = Entry(self.settings_frame, width=10, font=("Arial", 12))
        self.lrest_entry.grid(row=2, column=1, padx=5, pady=5)
        self.lrest_entry.insert(0, "15")

    def update_display(self):
        # Ensure self.time is treated as seconds
        if isinstance(self.time, datetime):
            print("Error: self.time is a datetime object")
            self.time = self.work_time  # Reset to default
        
        minutes = self.time // 60
        seconds = self.time % 60
        self.label.config(text=f"{minutes:02d}:{seconds:02d}")


    def start_timer(self):
        '''  
        -----------------------------------------------------------------------------------------------------
                                                  Timer
        -----------------------------------------------------------------------------------------------------
        To allow user start and end the timer by themselves
        '''
    
        if not self.current_task and not self.srest and not self.lrest:
            warning = Label(self.main_frame, text="Please set a task first!", font=("Arial", 12), fg="red", bg="#FEF8E3")
            warning.pack(after=self.task_frame)
            self.window.after(2000, warning.destroy)
            return

        if not self.running:  # Only start if not already running
            self.running = True
            self.able_button()
            self.update_timer()

    def start_sresttimer(self):
        if self.running:  # Don't start rest if timer is running
            return
        self.srest = True
        self.lrest = False
        self.running = True
        self.able_button()
        self.time = self.srest_time
        self.update_display()
        self.update_timer()

    def start_lresttimer(self):
        if self.running:  # Don't start rest if timer is running
            return
        self.lrest = True
        self.srest = False
        self.running = True
        self.able_button()
        self.time = self.lrest_time
        self.update_display()
        self.update_timer()

    def stop_timer(self):
        self.running = False
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
        self.enable_buttons()

    def reset_timer(self):
        self.running = False
        if self.timer_id:
            self.window.after_cancel(self.timer_id)
        self.srest = False
        self.lrest = False
        self.time = self.work_time
        self.update_display()
        self.enable_buttons()

    def update_timer(self):
        if self.running and self.time > 0:  # Fixed syntax here
            self.time -= 1
            self.update_display()
    
            if self.time == 0:
                # Play sound if available
                if self.sound:
                    try:
                        self.sound.play()
                    except:
                        print("Warning: Could not play sound")
                
                # Complete task if work timer finishes
                if not self.srest and not self.lrest:
                    self.complete_task()
                    self.running = False  # Stop the timer
                    self.enable_buttons() # Re-enable the buttons
                # Handle rest periods
                elif self.srest:
                    self.srest = False
                    self.time = self.work_time
                    self.running = False
                    self.enable_buttons()
                elif self.lrest:
                    self.lrest = False
                    self.time = self.work_time
                    self.running = False
                    self.enable_buttons()
                
                self.update_display()

                resetwarning = Label(self.main_frame, text="Please press reset if you want to continue!!!", 
                                   font=("Arial", 11), fg="red", bg="#FEF8E3")
                resetwarning.pack(after=self.control_frame)
                self.window.after(10000, resetwarning.destroy)
            
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.enable_buttons()

    def load_task_dict(self):
        """Load task counts from history file"""
        task_dict = {}
        try:
            if os.path.exists("History.txt"):
                with open("History.txt", 'r') as f:
                    for line in f:
                        try:
                            # Split the line into its components
                            parts = line.strip().split('|')
                            if len(parts) >= 3:
                                task_info = parts[2]
                                # Extract task name and count from the format "Task Name (#X)"
                                if '(#' in task_info and ')' in task_info:
                                    task_name = task_info[:task_info.rindex('(#')].strip().upper()
                                    count_str = task_info[task_info.rindex('(#')+2:task_info.rindex(')')]
                                    try:
                                        count = int(count_str)
                                        # Update the dictionary with the highest count found
                                        if task_name in task_dict:
                                            task_dict[task_name] = max(task_dict[task_name], count)
                                        else:
                                            task_dict[task_name] = count
                                    except ValueError:
                                        continue
                        except Exception as e:
                            print(f"Error parsing line in history: {e}")
        except Exception as e:
            print(f"Error loading task dictionary: {e}")
        return task_dict
        
    def setup_sound(self):
        self.sound = None
        try:
            if os.path.exists("alarm.mp3"):
                self.sound = pygame.mixer.Sound("alarm.mp3")
            else:
                print("Warning: alarm.mp3 not found. Timer will run without sound.")
        except:
            print("Warning: Could not initialize sound. Timer will run without sound.")
    
    def enable_buttons(self):
        self.start_button.config(state='normal')
        self.shortrest_button.config(state='normal')
        self.longrest_button.config(state='normal')
        self.settings_button.config(state='normal')

    def able_button(self):
        self.shortrest_button.config(state='disabled')
        self.longrest_button.config(state='disabled')
        self.start_button.config(state='disabled')
        self.settings_button.config(state='disabled')

if __name__ == "__main__":
    app = PomodoroTimer()
        