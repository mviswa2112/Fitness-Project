import tkinter as tk
from tkinter import messagebox, PhotoImage
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Load the dataset
df = pd.read_csv("sample_bmi_diet_dataset.csv")

# Splitting the calories (25% breakfast, 30% lunch, 25% dinner, 20% snacks)
def calorie_split(total_calories):
    return {
        'breakfast': int(total_calories * 0.25),
        'lunch': int(total_calories * 0.30),
        'dinner': int(total_calories * 0.25),
        'snacks': int(total_calories * 0.20)
    }

# Train linear regression models
X = df[['Height', 'Current Weight', 'Age', 'Gender']]
y_weight = df['Optimal Weight']
y_days = df['Days to Target']
y_calories = df['Daily Caloric Intake']

model_weight = LinearRegression().fit(X, y_weight)
model_days = LinearRegression().fit(X, y_days)
model_calories = LinearRegression().fit(X, y_calories)

# Tkinter UI for user input
def calculate_bmi_and_predict():
    try:
        user_id = entry_user_id.get().strip()
        name = entry_name.get().strip()
        height = float(entry_height.get().strip())
        weight = float(entry_weight.get().strip())
        age = int(entry_age.get().strip())
        gender = 1 if gender_var.get() == 'Male' else 0

        # Check for valid input
        if not user_id or not name or height <= 0 or weight <= 0 or age <= 0:
            raise ValueError

        # BMI Calculation
        bmi = round(weight / (height / 100) ** 2, 2)

        # Predicting optimal weight, days, and caloric intake
        features = pd.DataFrame([[height, weight, age, gender]], columns=['Height', 'Current Weight', 'Age', 'Gender'])
        optimal_weight = round(model_weight.predict(features)[0], 2)
        days_to_target = max(0, int(model_days.predict(features)[0]))
        daily_calories = int(model_calories.predict(features)[0])

        # Calorie split
        calorie_distribution = calorie_split(daily_calories)

        # Display results
        result_bmi.config(text=f"BMI: {bmi}")
        result_weight.config(text=f"Optimal Weight: {optimal_weight} kg")
        result_days.config(text=f"Days to Reach: {days_to_target}")
        result_calories.config(text=f"Daily Calories: {daily_calories}")
        result_breakfast.config(text=f"Breakfast: {calorie_distribution['breakfast']} cal")
        result_lunch.config(text=f"Lunch: {calorie_distribution['lunch']} cal")
        result_dinner.config(text=f"Dinner: {calorie_distribution['dinner']} cal")
        result_snacks.config(text=f"Snacks: {calorie_distribution['snacks']} cal")

        # Save to CSV
        save_data(user_id, name, height, weight, age, gender, bmi, optimal_weight, days_to_target, daily_calories, calorie_distribution)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid inputs.")

# Save data to CSV
def save_data(user_id, name, height, weight, age, gender, bmi, optimal_weight, days, calories, cal_split):
    new_data = {
        'User ID': user_id,
        'Name': name,
        'Height': height,
        'Current Weight': weight,
        'Age': age,
        'Gender': 'Male' if gender == 1 else 'Female',
        'BMI': bmi,
        'Optimal Weight': optimal_weight,
        'Days to Target': days,
        'Daily Caloric Intake': calories,
        'Breakfast Calories': cal_split['breakfast'],
        'Lunch Calories': cal_split['lunch'],
        'Dinner Calories': cal_split['dinner'],
        'Snacks Calories': cal_split['snacks']
    }
    df_new = pd.DataFrame([new_data])
    df_new.to_csv('user_bmi_diet_data.csv', mode='a', index=False, header=False)

# Tkinter UI Setup
root = tk.Tk()
root.title("BMI & Diet Plan Predictor")
root.geometry("500x650")

# Set background color for labels and entries
label_bg = '#f2f2f2'

# Fonts and Colors
label_font = ('Arial', 12, 'bold')
entry_font = ('Arial', 12)
button_font = ('Arial', 12, 'bold')
button_bg = '#4CAF50'
button_fg = '#ffffff'

# Adding widgets
# Create and grid the labels and entries with centering

# User ID
tk.Label(root, text="User ID", font=label_font, bg=label_bg).grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_user_id = tk.Entry(root, font=entry_font)
entry_user_id.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

# Name
tk.Label(root, text="Name", font=label_font, bg=label_bg).grid(row=1, column=0, padx=10, pady=10, sticky='e')
entry_name = tk.Entry(root, font=entry_font)
entry_name.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

# Height
tk.Label(root, text="Height (cm)", font=label_font, bg=label_bg).grid(row=2, column=0, padx=10, pady=10, sticky='e')
entry_height = tk.Entry(root, font=entry_font)
entry_height.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

# Weight
tk.Label(root, text="Weight (kg)", font=label_font, bg=label_bg).grid(row=3, column=0, padx=10, pady=10, sticky='e')
entry_weight = tk.Entry(root, font=entry_font)
entry_weight.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

# Age
tk.Label(root, text="Age (years)", font=label_font, bg=label_bg).grid(row=4, column=0, padx=10, pady=10, sticky='e')
entry_age = tk.Entry(root, font=entry_font)
entry_age.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

# Gender
tk.Label(root, text="Gender", font=label_font, bg=label_bg).grid(row=5, column=0, padx=10, pady=10, sticky='e')
gender_var = tk.StringVar(value='Male')
tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", font=label_font, bg=label_bg).grid(row=5, column=1, padx=10, pady=10, sticky='w')
tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", font=label_font, bg=label_bg).grid(row=5, column=2, padx=10, pady=10, sticky='w')

# Calculate & Predict Button
tk.Button(root, text="Calculate & Predict", font=button_font, bg=button_bg, fg=button_fg, command=calculate_bmi_and_predict).grid(row=6, columnspan=3, padx=10, pady=20, sticky='ew')

# Configure column weights for proper resizing
root.grid_columnconfigure(1, weight=1)

# Result labels
result_bmi = tk.Label(root, text="", font=label_font, bg=label_bg)
result_bmi.grid(row=7, columnspan=3, padx=10, pady=5)

result_weight = tk.Label(root, text="", font=label_font, bg=label_bg)
result_weight.grid(row=8, columnspan=3, padx=10, pady=5)

result_days = tk.Label(root, text="", font=label_font, bg=label_bg)
result_days.grid(row=9, columnspan=3, padx=10, pady=5)

result_calories = tk.Label(root, text="", font=label_font, bg=label_bg)
result_calories.grid(row=10, columnspan=3, padx=10, pady=5)

result_breakfast = tk.Label(root, text="", font=label_font, bg=label_bg)
result_breakfast.grid(row=11, columnspan=3, padx=10, pady=5)

result_lunch = tk.Label(root, text="", font=label_font, bg=label_bg)
result_lunch.grid(row=12, columnspan=3, padx=10, pady=5)

result_dinner = tk.Label(root, text="", font=label_font, bg=label_bg)
result_dinner.grid(row=13, columnspan=3, padx=10, pady=5)

result_snacks = tk.Label(root, text="", font=label_font, bg=label_bg)
result_snacks.grid(row=14, columnspan=3, padx=10, pady=5)

root.mainloop()