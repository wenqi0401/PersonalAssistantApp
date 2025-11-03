import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import json
import os

class MyNotes:
    def __init__(self, root):
        self.root = root
        self.root.title("My Notes")
        self.root.geometry("800x600")
        
        # Set peach color as background color for main window
        lighter_peach = "#FFE4C4"  # Peach color in hex
        self.root.configure(bg = lighter_peach)
        
        self.notes = {}
        self.note_widgets = {}
        
        self.create_notebook_frame()
        
        # Load existing notes
        try:
            if os.path.exists("notes.json"):
                with open("notes.json", "r") as f:
                    self.notes = json.load(f)
                    for title, note_data in self.notes.items():
                        self.create_note_widget(title, note_data)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load notes: {e}")
        
    def create_notebook_frame(self):
        # Main notebook frame setup with peach background
        lighter_peach = "#FFE4C4"
        
        self.notebook_frame = tk.Frame(self.root, bg = lighter_peach)
        self.notebook_frame.pack(padx = 20, pady = 20, fill = tk.BOTH, expand = True)
        
        # Canvas and scrollbar setup
        self.canvas = tk.Canvas(self.notebook_frame, bg = lighter_peach)
        self.scrollbar = tk.Scrollbar(self.notebook_frame, orient = "vertical", command = self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg = lighter_peach)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((10, 10), window = self.scrollable_frame, anchor = "n")
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        
        self.canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)  # Fixed the space issue here
        
        # Create control buttons frame with peach background
        button_frame = tk.Frame(self.root, bg = lighter_peach)
        button_frame.pack(pady = 10)
        
        # Style buttons
        button_style = {'font': ('Arial', 10, 'bold'), 'relief': 'raised', 'padx': 15, 'pady': 5}
        
        tk.Button(button_frame, text = "New Note", bg = "#4CAF50", fg = "white", **button_style, command = self.add_note).pack(side = tk.LEFT, padx = 5)
        tk.Button(button_frame, text = "View Note", bg = "#2196F3", fg = "white", **button_style, command = self.view_note).pack(side = tk.LEFT, padx = 15)
        tk.Button(button_frame, text = "Delete Note", bg = "#f44336", fg = "white", **button_style, command = self.delete_note).pack(side = tk.LEFT, padx = 25)
    
        # Save Notes Button
        tk.Button(button_frame, text="Save Notes", bg="#FF9800", fg="white", **button_style, command=self.save_notes_button).pack(side=tk.LEFT, padx=25)

    def save_notes(self):
        try:
            with open("notes.json", "w") as f:
                json.dump(self.notes, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save notes: {e}")
    
    # Save note to the text file
    def save_notes_button(self):
        try:
            # First check if there are any notes to save
            if not self.notes:
                messagebox.showinfo("Info", "No notes to save!")
                return
            with open("notes.txt", "w", encoding="utf-8") as f:
                for title, note_data in self.notes.items():
                    f.write(f"Title: {title}\n")
                    f.write(f"Content:\n{note_data.get('content', '')}\n")
                    f.write(f"Colour: {note_data.get('colour', 'default')}\n")
                    
                    if note_data.get('image'):
                        f.write(f"Image Path: {note_data['image']}\n")
                    
                    f.write("-" * 40 + "\n")  # Separator between notes
            
            messagebox.showinfo("Success", "Notes have been saved to 'notes.txt'!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save notes: {e}")

    def create_note_widget(self, title, note_data):
        note_frame = tk.Frame(self.scrollable_frame, bg = "silver", relief = tk.RIDGE)
        note_frame.pack(padx = 50, pady = 10, fill = tk.X, anchor = "center")
        
        # Title
        tk.Label(note_frame, text = f"Title: {title}", anchor = "n", font = ('Arial', 18, 'bold')).pack(fill = tk.X, padx = 20, pady = (10,0))
        
        # Content
        content_display = tk.Text(note_frame, width = 40, height = 8, font = ('Times New Roman', 18))
        content_display.insert(tk.END, note_data.get('content', ''))
        content_display.configure(fg = note_data.get('colour', 'black'))
        content_display.config(state = tk.DISABLED)
        content_display.pack(padx = 10, pady = 10, fill = tk.X)
        
        # Image
        if note_data.get('image'):
            try:
                photo = tk.PhotoImage(file = note_data['image'])
                photo = photo.subsample(2, 2)  # image size
                image_label = tk.Label(note_frame, image = photo)
                image_label.image = photo
                image_label.pack(padx = 10, pady = 10)
            except Exception as e:
                print(f"Could not load image: {e}")
        
        self.note_widgets[title] = note_frame

    def add_note(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Note")
        dialog.geometry("600x600")
        dialog.resizable(True, True)
        dialog.minsize(500, 600)
        dialog.grab_set()
        
        # Title
        title_frame = tk.Frame(dialog)
        title_frame.pack(fill = tk.X, padx = 10, pady = 5)
        
        tk.Label(title_frame, text="Title:").pack(side = tk.LEFT)
        title_entry = tk.Entry(title_frame)
        title_entry.pack(side=tk.LEFT, fill = tk.X, expand = True, padx = 5)
        
        # Content
        content_frame = tk.Frame(dialog)
        content_frame.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 5)
        
        tk.Label(content_frame, text = "Content:").pack(anchor = "w")
        content_text = tk.Text(content_frame, height = 5)
        content_text.pack(fill = tk.BOTH, expand = True)
        
        # Image preview
        image_var = tk.StringVar()
        image_label = tk.Label(dialog)
        image_label.pack(pady = 5)
        
        def attach_file():
            dialog.grab_release()
            filename = filedialog.askopenfilename(
                parent = dialog,
                title = "Select a file",
                filetypes = [("All files", "*.*")]
            )
            dialog.grab_set()
            
            if filename:
                # Insert file reference directly into content
                content_text.insert(tk.END, f"\n[Attached File: {os.path.basename(filename)}]\n")
                content_text.insert(tk.END, f"Path: {filename}\n")
        
        def choose_image():
            dialog.grab_release()
            file_path = filedialog.askopenfilename(
                parent = dialog,
                filetypes = [
                    ("Image files", "*.gif *.ppm *.pgm *.pdm *.png"),
                    ("All files", "*.*")
                ]
            )
            dialog.grab_set()
            
            if file_path:
                try:
                    photo = tk.PhotoImage(file = file_path)
                    photo = photo.subsample(2, 2)
                    image_label.config(image = photo)
                    image_label.image = photo
                    image_var.set(file_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Could not load image: {e}")
        
        def choose_color():
            dialog.grab_release()
            colour = colorchooser.askcolor(parent = dialog, title = "Choose Text Colour")
            if colour[1]:
                content_text.configure(fg = colour[1])
            dialog.grab_set()
        
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill = tk.X, padx = 10, pady = 5)
        
        tk.Button(button_frame, text = "Attach File", command = attach_file).pack(side = tk.LEFT, padx = 5)
        tk.Button(button_frame, text = "Add Image", command = choose_image).pack(side = tk.LEFT, padx = 5)
        tk.Button(button_frame, text = "Choose Color", command = choose_color).pack(side = tk.LEFT, padx = 5)
        
        def save():
            title = title_entry.get().strip()
            content = content_text.get("1.0", tk.END).strip()
            
            if not title or not content:
                messagebox.showwarning("Warning", "Title and content are required!")
                return
            
            if title in self.notes:
                if not messagebox.askyesno("Warning", "Note already exists. Overwrite?"):
                    return
            
            self.notes[title] = {
                'content': content,
                'colour': content_text.cget('fg'),
                'image': image_var.get()
            }
            
            self.save_notes()
            
            if title in self.note_widgets:
                self.note_widgets[title].destroy()
            self.create_note_widget(title, self.notes[title])
            
            dialog.destroy()
        
        tk.Button(button_frame, text="Save", command=save).pack(side=tk.RIGHT, padx=5)
        
        def on_closing():
            dialog.grab_release()
            dialog.destroy()
            
        dialog.protocol("WM_DELETE_WINDOW", on_closing)

    def view_note(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("View Note")
        dialog.geometry("500x600")
        dialog.resizable(True, True)
        dialog.minsize(500, 600)
        dialog.grab_set()
        
        notes_list = tk.Listbox(dialog, width = 50)
        notes_list.pack(padx = 10, pady = 5, fill = tk.X)
        
        for title in self.notes:
            notes_list.insert(tk.END, title)
        
        content_text = tk.Text(dialog, height = 15, wrap = tk.WORD)
        content_text.pack(padx = 10, pady = 5, fill = tk.BOTH, expand = True)
        
        image_label = tk.Label(dialog)
        image_label.pack(pady = 5)
        
        if not self.notes:
            messagebox.showinfo("Info", "No notes to view!")
            return
        
        def show_note(event = None):
            selection = notes_list.curselection()
            if not selection:
                return
                
            title = notes_list.get(selection[0])
            note = self.notes[title]
            
            content_text.config(state = tk.NORMAL)
            content_text.delete(1.0, tk.END)
            content_text.insert(tk.END, note['content'])
            content_text.config(fg = note['colour'], state = tk.DISABLED)
            
            if note.get('image'):
                try:
                    photo = tk.PhotoImage(file = note['image'])
                    photo = photo.subsample(2, 2)
                    image_label.config(image = photo)
                    image_label.image = photo
                except Exception as e:
                    print(f"Could not load image: {e}")
            else:
                image_label.config(image ='')
        
        notes_list.bind('<<ListboxSelect>>', show_note)
        
        def close():
            dialog.grab_release()
            dialog.destroy()
            
        tk.Button(dialog, text="Close", command=close).pack(pady=5)
        dialog.protocol("WM_DELETE_WINDOW", close)

    def delete_note(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Note")
        dialog.geometry("300x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        notes_list = tk.Listbox(dialog, width = 40)
        notes_list.pack(padx = 10, pady = 5, fill = tk.BOTH, expand = True)
        
        for title in self.notes:
            notes_list.insert(tk.END, title)
        
        if not self.notes:
            messagebox.showinfo("Info", "No notes to delete!")
            return
        
        def delete():
            selection = notes_list.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a note to delete!")
                return
                
            title = notes_list.get(selection[0])
            if messagebox.askyesno("Confirm", f"Delete note '{title}'?"):
                del self.notes[title]
                self.save_notes()
                if title in self.note_widgets:
                    self.note_widgets[title].destroy()
                    del self.note_widgets[title]
                dialog.destroy()
        
        def close():
            dialog.grab_release()
            dialog.destroy()
            
        tk.Button(dialog, text = "Delete", command = delete).pack(pady = 5)
        tk.Button(dialog, text = "Cancel", command = close).pack(pady = 5)
        dialog.protocol("WM_DELETE_WINDOW", close)

if __name__ == "__main__":
    root = tk.Tk()
    app = MyNotes(root)
    root.mainloop()