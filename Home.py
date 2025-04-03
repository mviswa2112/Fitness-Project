import tkinter as tk
from tkinter import font as tkFont
import os

# Function to create rounded corner button
def create_rounded_button(canvas, text, x, y, command=None):
    button_id = canvas.create_oval(x, y, x+180, y+60, fill="#80c1ff", outline="")
    text_id = canvas.create_text(x+90, y+30, text=text, font=button_font, fill="black")
    
    # Hover effect
    def on_enter(e):
        canvas.itemconfig(button_id, fill="#ffbf80")
        
    def on_leave(e):
        canvas.itemconfig(button_id, fill="#80c1ff")
        
    canvas.tag_bind(button_id, "<Enter>", on_enter)
    canvas.tag_bind(button_id, "<Leave>", on_leave)
    canvas.tag_bind(text_id, "<Enter>", on_enter)
    canvas.tag_bind(text_id, "<Leave>", on_leave)
    
    # Click event
    def on_click(e):
        if command:
            command()
    
    canvas.tag_bind(button_id, "<Button-1>", on_click)
    canvas.tag_bind(text_id, "<Button-1>", on_click)

# Button command functions to run separate files
def run_file1():
    os.system("python path/to/your_first_file.py")

def run_file2():
    os.system("python path/to/your_second_file.py")

def run_file3():
    os.system("python path/to/your_third_file.py")

# Initialize main window
root = tk.Tk()
root.title("FITBIT App")
root.geometry("800x600")
root.configure(bg="#f0f8ff")  # Set a light blue background color

# Set custom font
button_font = tkFont.Font(family="Helvetica", size=14)

# Create canvas for rounded buttons
canvas = tk.Canvas(root, bg="#f0f8ff", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Title label
title_font = tkFont.Font(family="Helvetica", size=24, weight="bold")
title_label = tk.Label(root, text="FITBIT App", font=title_font, bg="#f0f8ff", fg="#4CAF50")
title_label.pack(pady=20)

# Create buttons with hover effects and commands
create_rounded_button(canvas, "Button 1", 310, 200, command=run_file1)
create_rounded_button(canvas, "Button 2", 310, 300, command=run_file2)
create_rounded_button(canvas, "Button 3", 310, 400, command=run_file3)

# Run the application
root.mainloop()