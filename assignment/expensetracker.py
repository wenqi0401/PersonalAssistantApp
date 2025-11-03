from tkinter import *
from datetime import datetime
from zoneinfo import ZoneInfo
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import ttk  # Important for styling
from password import Password
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class ExpenseTracker:
    def __init__(self, parent_window=None):
        # If no parent window is provided, create a new Tk window
        if parent_window is None:
            self.parent_window = Tk()
        else:
            self.parent_window = parent_window
            
        # Ensure picture directory exists
        if not os.path.exists("picture"):
            os.makedirs("picture")
            
        # Store PhotoImage objects as instance variables
        self.images = {}
        
        # Initialize login window
        self.login()
    def show_main_expense_window(self):
        self.window = Toplevel(self.parent_window)
        self.window.title("Expense Tracker")
        
        self.front = Frame(self.window)
        self.front.pack()
        
        self.frame = Frame(self.window)
        self.frame.pack()
        
        # Use stored images
        self.logo_label = Label(self.front, image=self.images['expense'])
        self.logo_label.pack(side=LEFT)
        
        self.incomebt = Button(self.front, image=self.images['incomebt'], command=self.income)
        self.incomebt.pack(side=TOP)
        
        self.expensebt = Button(self.front, image=self.images['expensebt'], command=self.expense)
        self.expensebt.pack()
        
        self.viewbt = Button(self.front, image=self.images['recordbt'], command=self.choose)
        self.viewbt.pack()
        
        self.current()
        self.total = float(self.currentamount)
        self.setcolour()
        self.current = Label(self.front, text="Your current total is RM"+str("{:.2f}".format(self.total)), 
                           fg=self.color, font=("Arial", "30", "bold"))
        self.current.pack()
        
        self.incomeput = 0
        self.expenses = 0
        self.style = ttk.Style()
        self.style.configure("Income.TCombobox", foreground="#8F0F07", font=("Arial", 25, "bold"))
        self.style.configure("Expense.TCombobox", foreground="#8F0F07", font=("Arial", 25, "bold"))
        
        self.window.mainloop()

    def income(self):
        self.clear_frame()
        
        self.prompt = Label(self.frame, text="Enter your income(RM):",fg="#7C1B85",font=("Courier","30","bold"))
        self.prompt.grid(row=3, column=2) 
        self.incomeput = DoubleVar()
        self.entry = Entry(self.frame, textvariable=self.incomeput,fg="Green",font=("Arial","25","bold")).grid(row=3, column=3)
        self.catego = Label(self.frame, text="Choose a category:",fg="#7C1B85",font=("Courier","30","bold"))
        self.catego.grid(row=4, column=2) 
        
        self.categories=["Allowance","Award","Scholarships and Grants","Passive income","Investment","Lottery","Salary","Tips","Others"]
        self.combobox=Combobox(self.frame,value=self.categories,style="Income.TCombobox",font=("Arial", 25, "bold"))
        self.combobox.grid(row=4,column=3)
        self.combobox.set("None")
        
       
        self.description=Label(self.frame,text="Enter description:",foreground="#7C1B85",font=("Courier","30","bold")).grid(row=5,column=2)
        self.detail=StringVar()
        self.entrydecscrip=Entry(self.frame,textvariable=self.detail,fg="#00023D",font=("Arial","25","bold")).grid(row=5,column=3)
        
        self.confrimpic=PhotoImage(file="picture/confirmbt.png")
        self.confirmbt = Button(self.frame,image=self.confrimpic,command=self.confirmincome)
        self.confirmbt.grid(row=6,column=6)
        
    def expense(self):
        self.clear_frame()
        
        self.prompt2 = Label(self.frame, text="Enter your expense(RM):",fg="#7C1B85",font=("Courier","30","bold"))
        self.prompt2.grid(row=3, column=2)
        
        self.expenses = DoubleVar()
        self.entry = Entry(self.frame, textvariable=self.expenses,fg="Red",font=("Arial","25","bold"))
        self.entry.grid(row=3, column=3)
        
        self.catego2 = Label(self.frame,text="Choose a categories:",fg="#7C1B85",font=("Courier","30","bold"))
        self.catego2.grid(row=4,column=2)
        
        self.categories2 = ["Bills","Clothing","Education","Entertainment","Food","Gift","Health","Shopping","Transportation","Travel","Others"]
        self.combobox2 = Combobox(self.frame, values=self.categories2, style="Expense.TCombobox", font=("Arial", 25, "bold"))
        self.combobox2.grid(row=4,column=3)
        self.combobox2.set("None")
        
        self.details = StringVar()
        self.descriptions = Label(self.frame,text="Enter description:",fg="#7C1B85",font=("Courier","30","bold"))
        self.descriptions.grid(row=5,column=2)
        
        self.entrydescriptions = Entry(self.frame,textvariable=self.details,fg="#00023D",font=("Arial","25","bold"))
        self.entrydescriptions.grid(row=5,column=3)
        
        self.confrimpic=PhotoImage(file="picture/confirmbt.png")
        self.confirmbt = Button(self.frame,image=self.confrimpic,command=self.confirmexpense)  # This line remains the same
        self.confirmbt.grid(row=6,column=6)

    def confirmincome(self):
        try:            
            income = float(self.incomeput.get())  # Explicitly convert to float
            if not isinstance(income, (int, float)):
                messagebox.showerror("Invalid Input", "Please enter a valid number")
                return
                
            # Check for positive number
            if income <= 0:
                messagebox.showerror("Invalid Input", "Income must be a positive number")
                return
            
            self.amount = income
            self.choice = self.combobox.get()
            self.filename = "income.txt"
            self.desc = self.detail.get()
            
            messagebox.showinfo("Success","Income entered: RM {:.2f}".format(income))
            self.repeat()
            self.appendfile()
            
        except (TclError,ValueError) as e:
            messagebox.showerror("Error", "Invalid input! Please enter a numeric value.")
            return
    
    def confirmexpense(self):
        try:
            expense = float(self.expenses.get())  # Get the expense value from self.expenses
            if not isinstance(expense, (int, float)):
                messagebox.showerror("Invalid Input", "Please enter a valid number")
                return
                
            # Check for positive number
            if expense <= 0:
                messagebox.showerror("Invalid Input", "Expense must be a positive number")
                return
            
            if self.combobox2.get() == "None":
                messagebox.showerror("Invalid Input", "Please select a category")
                return
                
            self.amount = -expense  # Make expense negative for calculations
            self.choice = self.combobox2.get()
            self.filename = "expense.txt"
            self.desc = self.details.get()
            
            messagebox.showinfo("Success", f"Expense entered: RM {expense:.2f}")
            self.repeat()
            self.appendfile()
    
        except  (TclError,ValueError) as e:
            messagebox.showerror("Error", "Invalid input! Please enter a numeric value.")
            return

    def appendfile(self):
        try:
            self.f=open(self.filename,'a')
            self.f.write(str(self.amount)+'|')
            self.f.write(str(self.time.hour)+":"+str(self.time.minute)+":"+str(self.time.second)+'|')
            self.f.write(str(self.time.day)+'/'+str(self.time.month)+'/'+str(self.time.year)+'|')
            self.f.write(str(self.choice)+'|')
            self.f.write(str(self.desc+"\n"))
        
        finally:
            self.f.close()

    def viewincome(self):
        self.filename="income.txt"
        self.window2 = Toplevel(self.window)
        self.window2.title("Records of expenses and incomes")
        self.frame3 = Frame(self.window2)
        self.frame3.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)
    
        # Create Scrollbars FIRST
        self.scrollbar = Scrollbar(self.frame3)
        self.scrollbar.pack(side=RIGHT, fill=Y)
    
        # Create Text widgets
        self.records = Text(self.frame3, wrap=WORD, fg="#39107B", bg="#9798F0",font=("Arial", "20", "bold"), height=20, width=50,yscrollcommand=self.scrollbar.set, padx=0, pady=10)
        self.records.pack(side=LEFT, fill=Y, anchor='w')
        self.scrollbar.config(command=self.records.yview)
        self.recordname=self.records
        
        self.view()
        # Set records to read-only
        self.records.config(state=DISABLED)

        self.menu = Menu(self.window2, tearoff=0)
        self.menu.add_command(label="Delete lastest record for INCOME",command=self.deleteincome)
        self.window2.bind("<Button-3>", self.popup)
    def viewexpense(self):
        self.filename="expense.txt"
        self.window2 = Toplevel(self.window)
        self.window2.title("Records of expenses and incomes")
        self.frame4 = Frame(self.window2)
        self.frame4.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    
        # Create Scrollbars FIRST
        self.scrollbar2 = Scrollbar(self.frame4)
        self.scrollbar2.pack(side=RIGHT, fill=Y)
    
        # Create Text widgets
        self.records2 = Text(self.frame4, wrap=WORD, height=20, width=50,fg="#39107B", bg="#9798F0", font=("Arial", "20", "bold"),yscrollcommand=self.scrollbar2.set, padx=0, pady=10)
        self.records2.pack(side=LEFT, fill=Y, anchor='w')
        self.scrollbar2.config(command=self.records2.yview)
        self.recordname=self.records2
        
        self.view()
        # Set records to read-only
        self.records2.config(state=DISABLED)


        self.menu = Menu(self.window2, tearoff=0)
        self.menu.add_command(label="Delete lastest record for EXPENSE",command=self.deleteexpense)
        self.window2.bind("<Button-3>", self.popup)
        self.show_analysis()
    def savecurrent(self):
        try:
            with open("current.txt","a") as self.f:
                self.f.write(str(self.total)+"\n")
        except FileNotFoundError:
            self.fileerror=messagebox.showerror("File Not Found Error", "File opening error。")
              
            
    def current(self):
        try:
            with open("current.txt", "r") as self.f:
                # Read all lines and get the last (most recent) total
                self.currentamount = self.f.readlines()
                # If file is empty, start with 0
                if not self.currentamount:
                    with open("current.txt", "w") as f:
                        f.write("0\n")
                    self.currentamount = "0"
                else:
                    # Get the last line (most recent total)
                    self.currentamount = self.currentamount[-1].strip()
        except FileNotFoundError:
            # If file doesn't exist, create it with 0
            with open("current.txt", "w") as f:
                f.write("0\n")
            self.currentamount = "0"

    def popup(self,event):
        self.menu.post(event.x_root, event.y_root)
        
    def deleteexpense(self):
        self.filename="expense.txt"
        self.delete()
        
    def deleteincome(self):
        self.filename="income.txt"
        self.delete()
        
    def delete(self):
        try:
            # Read all lines from income/expense file
            with open(self.filename, "r") as f:
                lines = f.readlines()
            
            # Check if there are records to delete
            if len(lines) > 1:
                # Get amount from last line and split
                last_line = lines[-1].strip().split('|')
                amount = float(last_line[0])
                
                # Remove last line
                lines.pop()
                
                # Write remaining lines back
                with open(self.filename, "w") as f:
                    f.writelines(lines)
                
                # Update total
                self.total = self.total - amount
                
                # Update display
                for widget in self.front.winfo_children():
                    if isinstance(widget, Label) and ("total"in widget.cget("text").lower() or "current" in widget.cget("text").lower()):
                        widget.destroy()
                
                self.setcolour()
                self.result = Label(self.front, 
                                  text=f"Your total is RM:{self.total:.2f}", 
                                  fg=self.color, 
                                  font=("Arial", "30", "bold"))
                self.result.pack()
                
                # Update current.txt
                with open("current.txt", "a") as f:
                    f.write(f"{self.total}\n")
                    
            else:
                messagebox.showinfo("Info", "No records to delete")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        
        

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def setcolour(self):
        # Determine color based on total
            if self.total > 0:
                self.color = "green"
            elif self.total < 0:
                self.color = "red"
            else:
                self.color = "black"
    def repeat(self):
            self.clear_frame()
            self.total = self.total + self.amount
            self.savecurrent()
            self.current.destroy()
            self.setcolour()
            
            # Update total display
            try:
                self.result.destroy()
            except AttributeError:
                pass
            
            self.result = Label(self.front, text=f"Your total is RM: {self.total:.2f}", 
                                fg=self.color, font=("Arial", "40","bold"))
            self.result.pack()
            
            self.time = datetime.now(ZoneInfo('Asia/Kuala_Lumpur'))
    def choose(self):
        self.smallwindow=Toplevel(self.window)
        self.smallwindow.title("Expense OR Income")
        self.recordincomebt=PhotoImage(file="picture/recordincome.png")
        self.reocrdexpensebt=PhotoImage(file="picture/recordexpense.png")
        self.ana1=PhotoImage(file="picture/ana1.png")
        self.ana2=PhotoImage(file="picture/ana2.png")
        self.bt1=Button(self.smallwindow,image=self.recordincomebt,command=self.viewincome)
        self.bt1.pack(side=LEFT)
        self.bt2=Button(self.smallwindow,image=self.reocrdexpensebt,command=self.viewexpense)
        self.bt2.pack(side=LEFT)
        self.bt3=Button(self.smallwindow,image=self.ana1,command=self.show_income_analysis)
        self.bt3.pack(side=LEFT)
        
        self.bt4=Button(self.smallwindow,image=self.ana2,command=self.show_expense_analysis)
        self.bt4.pack(side=RIGHT)
        
    def view(self):
         # Handle expense records
        try:
            with open(self.filename,'r') as f:
                self.readed = f.readlines()
                if len(self.readed) > 1:
                    for line in self.readed[1:][::-1]:  # Skip header and reverse
                        try:
                            amount, time, date, category, description = line.strip().split('|')
                            record_text = (
                                f"-----------------------------\n"
                                f"Expense: RM {float(amount):.2f}\n"
                                f"Date: {date}\n"
                                f"Time: {time}\n"
                                f"Category: {category}\n"
                                f"Description: {description}\n"
                                f"---------------------------\n"
                            )
                            self.recordname.insert(END, record_text)
                        except ValueError:
                            self.recordname.insert(END, "Malformed record found.\n")
                else:
                    self.recordname.insert(END, "No expense records found.\n")
        except FileNotFoundError:
            self.recordname.insert(END, "Expense file not found.\n")
    
    def login(self):
        self.window1 = Toplevel(self.parent_window)
        self.window1.title("Expense Tracker Login")
        self.load_images()
        self.credentials_file = "credentials.txt"
        self.value=False
        # Load credentials if they exist
        self.stored_username = None
        self.stored_password = None
        self.load_credentials()

        # Create a grid layout
        self.loginframe = Frame(self.window1)
        self.loginframe.grid(row=0, column=0, padx=10, pady=10)

        self.loginframe2 = Frame(self.window1)
        self.loginframe2.grid(row=1, column=0, padx=10, pady=10)

# Use stored images for login screen
        self.username_label = Label(self.loginframe, text="Username:",font=("Arial",30,"bold"))
        self.username_label.grid(row=0, column=0, sticky=E, padx=5, pady=5)
        
        self.username_entry = Entry(self.loginframe, font=("Arial", 25, "bold"))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = Label(self.loginframe, text="Password:",font=("Arial",30,"bold"))
        self.password_label.grid(row=1, column=0, sticky=E, padx=5, pady=5)
        
        self.password_entry = Entry(self.loginframe, show="*", font=("Arial", 25, "bold"))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = Button(self.loginframe, image=self.images['login'], command=self.on_login_click)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.setbt = Button(self.loginframe, image=self.images['set'], command=self.set_credentials)
        self.setbt.grid(row=3, column=0, columnspan=2, pady=10)

        self.window1.mainloop()

    def load_credentials(self):
        """Load username and password from file if it exists and is not empty."""
        try:
            with open(self.credentials_file, "r") as file:
                lines = file.readlines()
                if len(lines) == 2:  # Ensure there are two lines (username and password)
                    self.stored_username = lines[0].strip()
                    self.stored_password = lines[1].strip()
                    print("Credentials loaded successfully.")
                    self.value=True
                else:
                    messagebox.showinfo("Info", "Credentials file is empty or invalid. Please set username and password.")
        except FileNotFoundError:
            print("Credentials file not found. Please set username and password.")

    def save_credentials(self, username, password):
        """Save username and password to a file."""
        with open(self.credentials_file, "w") as file:
            file.write(f"{username}\n{password}")
        print("Credentials saved successfully.")

    def on_login_click(self):
        username_input = self.username_entry.get()
        password_input = self.password_entry.get()

        # Validate login using the stored credentials
        if self.stored_username is None or self.stored_password is None:
            messagebox.showinfo("Login", "You must set both a username and a password first.")
        elif username_input == self.stored_username and password_input == self.stored_password:
            messagebox.showinfo("Login Success", "Welcome!")
            self.window1.destroy()
            self.show_main_expense_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def set_credentials(self):
        if self.value==True:
            messagebox.showinfo("Password and Username setted","You already have you password and username.")
            return
# Clear loginframe2 and create the credential-setting interface
        for widget in self.loginframe2.winfo_children():
            widget.destroy()

        self.lblusername = Label(self.loginframe2, text="Set new username:",font=("Arial", 25, "bold"))
        self.lblusername.grid(row=0, column=0, sticky=E, padx=5, pady=5)
        self.entryusername = Entry(self.loginframe2,font=("Arial", 25, "bold"))
        self.entryusername.grid(row=0, column=1, padx=5, pady=5)

        self.lblpassword = Label(self.loginframe2, text="Set new password:",font=("Arial", 25, "bold"))
        self.lblpassword.grid(row=1, column=0, sticky=E, padx=5, pady=5)
        self.entrypassword = Entry(self.loginframe2, show="*",font=("Arial", 25, "bold"))
        self.entrypassword.grid(row=1, column=1, padx=5, pady=5)

        self.confirmpass = Button(self.loginframe2, text="Confirm", command=self.check_credentials)
        self.confirmpass.grid(row=2, column=0, columnspan=2, pady=10)

    def check_credentials(self):
        new_username = self.entryusername.get()
        new_password = self.entrypassword.get()

        try:
            # Validate and set the username
            Password.check_username(new_username)
            Password.check_password(new_password)

            # Save the credentials
            self.save_credentials(new_username, new_password)

            messagebox.showinfo("Success", "Username and Password set successfully!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        messagebox.showinfo("Password and Username setted","You already set the password and username.")
    def load_images(self):
        """Load all required images and store them as instance variables"""
        image_files = {
            'expense': 'expense.png',
            'incomebt': 'incomebt.png',
            'expensebt': 'expensebt.png',
            'recordbt': 'recordbt.png',
            'confirmbt': 'confirmbt.png',
            'recordincome': 'recordincome.png',
            'recordexpense': 'recordexpense.png',
            'login': 'login.png',
            'set': 'set.png',
            'ana1': 'ana1.png',
            'ana2': 'ana2.png'
        }
        
        for key, filename in image_files.items():
            try:
                filepath = os.path.join("picture", filename)
                if os.path.exists(filepath):
                    self.images[key] = PhotoImage(file=filepath)
                else:
                    print(f"Warning: Image file {filepath} not found")
                    # Create a simple replacement image
                    self.images[key] = PhotoImage(width=100, height=30)
            except TclError as e:
                print(f"Error loading image {filename}: {e}")
                self.images[key] = PhotoImage(width=100, height=30)
    def show_expense_analysis(self):
        """Display spending analysis charts"""
        analysis_window = Toplevel(self.window)
        analysis_window.title("Expense Analysis")
        analysis_window.geometry("1200x800")
    
        # Create tabs for different charts
        tab_control = ttk.Notebook(analysis_window)
        
        # Tab 1: Category-wise Expenses
        tab1 = Frame(tab_control)
        tab_control.add(tab1, text='Category Analysis')
        
        # Tab 2: Monthly Comparison
        tab2 = Frame(tab_control)
        tab_control.add(tab2, text='Monthly Comparison')
        
        tab_control.pack(expand=1, fill='both')
    
        try:
            # Read expense data
            expenses_by_category = defaultdict(float)
            monthly_expenses = defaultdict(float)
            
            with open("expense.txt", 'r') as f:
                next(f)  # Skip header
                for line in f:
                    try:
                        amount, _, date, category, _ = line.strip().split('|')
                        amount = abs(float(amount))  # Convert to positive number
                        
                        # For category analysis
                        expenses_by_category[category] += amount
                        
                        # For monthly analysis
                        month = date.split('/')[1]  # Extract month from date
                        monthly_expenses[month] += amount
                    except:
                        continue
    
            # Create Figure 1: Pie Chart for Categories
            fig1 = Figure(figsize=(6, 5))
            ax1 = fig1.add_subplot(111)
            
            # Filter categories with non-zero values
            non_zero_categories = {k: v for k, v in expenses_by_category.items() if v > 0}
            
            if non_zero_categories:
                labels = list(non_zero_categories.keys())
                sizes = list(non_zero_categories.values())
                
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
                ax1.axis('equal')
                
                canvas1 = FigureCanvasTkAgg(fig1, tab1)
                canvas1.draw()
                canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    
            # Create Figure 2: Bar Chart for Monthly Expenses
            fig2 = Figure(figsize=(6, 5))
            ax2 = fig2.add_subplot(111)
            
            months = list(monthly_expenses.keys())
            values = list(monthly_expenses.values())
            
            ax2.bar(months, values)
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Total Expenses (RM)')
            ax2.set_title('Monthly Expenses')
            
            # Rotate x-axis labels for better readability
            ax2.tick_params(axis='x', rotation=45)
            
            canvas2 = FigureCanvasTkAgg(fig2, tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    
            # Add summary labels
            if expenses_by_category:
                total_expenses = sum(expenses_by_category.values())
                highest_category = max(expenses_by_category.items(), key=lambda x: x[1])
                
                summary_text = f"""
                Total Expenses: RM {total_expenses:.2f}
                Highest Spending Category: {highest_category[0]} (RM {highest_category[1]:.2f})
                """
                
                summary_label = Label(tab1, text=summary_text, font=("Arial", 12), justify=LEFT)
                summary_label.pack(pady=10)
    
        except FileNotFoundError:
            Label(analysis_window, text="No expense data found", font=("Arial", 14)).pack(pady=20)

    def show_income_analysis(self):
        """Display income analysis charts"""
        analysis_window = Toplevel(self.window)
        analysis_window.title("Income Analysis")
        analysis_window.geometry("1200x800")
    
        # Create tabs for different charts
        tab_control = ttk.Notebook(analysis_window)
        
        # Tab 1: Category-wise Income
        tab1 = Frame(tab_control)
        tab_control.add(tab1, text='Category Analysis')
        
        # Tab 2: Monthly Comparison
        tab2 = Frame(tab_control)
        tab_control.add(tab2, text='Monthly Income')
        
        tab_control.pack(expand=1, fill='both')
    
        try:
            # Read income data
            income_by_category = defaultdict(float)
            monthly_income = defaultdict(float)
            
            with open("income.txt", 'r') as f:
                next(f)  # Skip header
                for line in f:
                    try:
                        amount, _, date, category, _ = line.strip().split('|')
                        amount = float(amount)  # No need to abs() since income is positive
                        
                        # For category analysis
                        income_by_category[category] += amount
                        
                        # For monthly analysis
                        month = date.split('/')[1]  # Extract month from date
                        monthly_income[month] += amount
                    except:
                        continue
    
            # Create Figure 1: Pie Chart for Categories
            fig1 = Figure(figsize=(6, 5))
            ax1 = fig1.add_subplot(111)
            
            # Filter categories with non-zero values
            non_zero_categories = {k: v for k, v in income_by_category.items() if v > 0}
            
            if non_zero_categories:
                labels = list(non_zero_categories.keys())
                sizes = list(non_zero_categories.values())
                
                # Use a different color scheme for income
                colors = plt.cm.Greens(np.linspace(0.4, 0.8, len(sizes)))
                
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
                ax1.axis('equal')
                ax1.set_title('Income Sources Distribution')
                
                canvas1 = FigureCanvasTkAgg(fig1, tab1)
                canvas1.draw()
                canvas1.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    
            # Create Figure 2: Bar Chart for Monthly Income
            fig2 = Figure(figsize=(6, 5))
            ax2 = fig2.add_subplot(111)
            
            months = list(monthly_income.keys())
            values = list(monthly_income.values())
            
            # Use green color for income bars
            ax2.bar(months, values, color='#2E8B57')
            ax2.set_xlabel('Month')
            ax2.set_ylabel('Total Income (RM)')
            ax2.set_title('Monthly Income')
            
            # Rotate x-axis labels for better readability
            ax2.tick_params(axis='x', rotation=45)
            
            canvas2 = FigureCanvasTkAgg(fig2, tab2)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    
            # Add summary labels
            if income_by_category:
                total_income = sum(income_by_category.values())
                highest_category = max(income_by_category.items(), key=lambda x: x[1])
                
                summary_text = f"""
                Total Income: RM {total_income:.2f}
                Highest Income Source: {highest_category[0]} (RM {highest_category[1]:.2f})
                Average Monthly Income: RM {(total_income/len(monthly_income) if monthly_income else 0):.2f}
                """
                
                summary_label = Label(tab1, text=summary_text, font=("Arial", 12), justify=LEFT)
                summary_label.pack(pady=10)
    
        except FileNotFoundError:
            Label(analysis_window, text="No income data found", font=("Arial", 14)).pack(pady=20)

if __name__ == "__main__":
    ExpenseTracker()