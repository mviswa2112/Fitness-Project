import tkinter as tk
from tkinter import messagebox
import pandas as pd

# Load the dataset
df_user_data = pd.read_csv("user_bmi_diet_data.csv")

# Function to fetch user details based on User ID
def fetch_user_details():
    user_id = entry_user_id.get().strip()
    
    # Check if User ID exists in the dataset
    user_data = df_user_data[df_user_data['User ID'] == user_id]
    
    if not user_data.empty:
        # Extract user details
        height = user_data.iloc[0]['Height']
        name = user_data.iloc[0]['Name']
        weight = user_data.iloc[0]['Current Weight']
        age = user_data.iloc[0]['Age']
        gender = user_data.iloc[0]['Gender']
        bmi = user_data.iloc[0]['BMI']
        optimal_weight = user_data.iloc[0]['Optimal Weight']
        days_to_target = user_data.iloc[0]['Days to Target']
        daily_calories = user_data.iloc[0]['Daily Caloric Intake']
        breakfast_calories = user_data.iloc[0]['Breakfast Calories']
        lunch_calories = user_data.iloc[0]['Lunch Calories']
        dinner_calories = user_data.iloc[0]['Dinner Calories']
        snacks_calories = user_data.iloc[0]['Snacks Calories']
        
        # Display results in the UI
        result_name.config(text=f"Name: {name}")
        result_height.config(text=f"Height: {height} cm")
        result_weight.config(text=f"Weight: {weight} kg")
        result_age.config(text=f"Age: {age} years")
        result_gender.config(text=f"Gender: {gender}")
        result_bmi.config(text=f"BMI: {bmi:.2f}")
        result_optimal_weight.config(text=f"Optimal Weight: {optimal_weight:.2f} kg")
        result_days_to_target.config(text=f"Days to Target: {days_to_target}")
        result_daily_calories.config(text=f"Daily Calories: {daily_calories:.0f}")
        result_breakfast.config(text=f"Breakfast: {breakfast_calories:.0f} cal")
        result_lunch.config(text=f"Lunch: {lunch_calories:.0f} cal")
        result_dinner.config(text=f"Dinner: {dinner_calories:.0f} cal")
        result_snacks.config(text=f"Snacks: {snacks_calories:.0f} cal")
    else:
        messagebox.showerror("Error", "User ID not found")

# Tkinter UI Setup
root = tk.Tk()
root.title("User BMI & Diet Plan Details")
root.geometry("500x600")

# Fonts and Colors
label_font = ('Arial', 12, 'bold')
entry_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')
button_bg = '#4CAF50'
button_fg = '#ffffff'
label_bg = '#f2f2f2'

# Adding widgets
tk.Label(root, text="User ID", font=label_font, bg=label_bg).grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_user_id = tk.Entry(root, font=entry_font)
entry_user_id.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

tk.Button(root, text="Fetch Details", font=button_font, bg=button_bg, fg=button_fg, command=fetch_user_details).grid(row=1, columnspan=2, padx=10, pady=20, sticky='ew')

# Result labels for user details
result_name = tk.Label(root, text="", font=label_font, bg=label_bg)
result_name.grid(row=2, columnspan=2, padx=10, pady=5)

result_height = tk.Label(root, text="", font=label_font, bg=label_bg)
result_height.grid(row=3, columnspan=2, padx=10, pady=5)

result_weight = tk.Label(root, text="", font=label_font, bg=label_bg)
result_weight.grid(row=4, columnspan=2, padx=10, pady=5)

result_age = tk.Label(root, text="", font=label_font, bg=label_bg)
result_age.grid(row=5, columnspan=2, padx=10, pady=5)

result_gender = tk.Label(root, text="", font=label_font, bg=label_bg)
result_gender.grid(row=6, columnspan=2, padx=10, pady=5)

result_bmi = tk.Label(root, text="", font=label_font, bg=label_bg)
result_bmi.grid(row=7, columnspan=2, padx=10, pady=5)

result_optimal_weight = tk.Label(root, text="", font=label_font, bg=label_bg)
result_optimal_weight.grid(row=8, columnspan=2, padx=10, pady=5)

result_days_to_target = tk.Label(root, text="", font=label_font, bg=label_bg)
result_days_to_target.grid(row=9, columnspan=2, padx=10, pady=5)

result_daily_calories = tk.Label(root, text="", font=label_font, bg=label_bg)
result_daily_calories.grid(row=10, columnspan=2, padx=10, pady=5)

result_breakfast = tk.Label(root, text="", font=label_font, bg=label_bg)
result_breakfast.grid(row=11, columnspan=2, padx=10, pady=5)

result_lunch = tk.Label(root, text="", font=label_font, bg=label_bg)
result_lunch.grid(row=12, columnspan=2, padx=10, pady=5)

result_dinner = tk.Label(root, text="", font=label_font, bg=label_bg)
result_dinner.grid(row=13, columnspan=2, padx=10, pady=5)

result_snacks = tk.Label(root, text="", font=label_font, bg=label_bg)
result_snacks.grid(row=14, columnspan=2, padx=10, pady=5)

# Start the Tkinter loop
root.mainloop()