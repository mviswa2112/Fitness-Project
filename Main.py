import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Paths for the datasets
food_data_path = "indian_food.csv"
consumption_data_path = "daily_consumption.csv"

# Load the food dataset
food_df = pd.read_csv(food_data_path)

# Function to get caloric data from the dataset
def get_calories(food_item):
    food_data = food_df[food_df['name'].str.lower() == food_item.lower()]
    if not food_data.empty:
        return (
            food_data['calories'].fillna(0).values[0],
            food_data['carbs'].fillna(0).values[0],
            food_data['fats'].fillna(0).values[0],
            food_data['proteins'].fillna(0).values[0]
        )
    else:
        return 0, 0, 0, 0

# Function to update dataset with new food data
def update_food_dataset(food_item, calories, carbs, fats, proteins):
    global food_df
    new_data = pd.DataFrame({
        'name': [food_item],
        'calories': [calories],
        'carbs': [carbs],
        'fats': [fats],
        'proteins': [proteins]
    })
    food_df = pd.concat([food_df, new_data], ignore_index=True)
    food_df.to_csv(food_data_path, index=False)  # Save the updated dataset

# Function to log daily consumption along with User ID
def log_consumption(date, user_id, food_item, quantity, category, calories):
    try:
        consumption_df = pd.read_csv(consumption_data_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        # Create a new DataFrame with headers if the file does not exist or is empty
        consumption_df = pd.DataFrame(columns=['date', 'user_id', 'food_item', 'quantity', 'category', 'calories'])

    new_data = pd.DataFrame({
        'date': [date],
        'user_id': [user_id],
        'food_item': [food_item],
        'quantity': [quantity],
        'category': [category],
        'calories': [calories]
    })
    consumption_df = pd.concat([consumption_df, new_data], ignore_index=True)
    consumption_df.to_csv(consumption_data_path, index=False)  # Save the updated dataset

# Function to display the charts side by side filtered by User ID
def display_charts(date, user_id_entry):
    try:
        consumption_df = pd.read_csv(consumption_data_path)
        if consumption_df.empty:
            tk.messagebox.showinfo("Info", "No data available to display.")
            return
    except (FileNotFoundError, pd.errors.EmptyDataError):
        tk.messagebox.showinfo("Info", "No data available to display.")
        return

    # Filter data for the selected date and user ID
    daily_data = consumption_df[(consumption_df['date'] == date) & (consumption_df['user_id'] == user_id_entry)]

    if daily_data.empty:
        tk.messagebox.showinfo("Info", f"No data available for User ID {user_id_entry} on {date}.")
        return

    # Aggregate data for plotting
    daily_totals = daily_data.groupby('category').agg({'calories': 'sum'}).reset_index()

    goaldf = pd.read_csv('user_bmi_diet_data.csv')
    
    # Filter the DataFrame to find the row with the matching user_id
    user_data = goaldf[goaldf['User ID'] == user_id_entry]
    
    # Check if the user_id exists
    if not user_data.empty:
        name = user_data['Name'].values[0]
        breakfast = user_data['Breakfast Calories'].values[0]
        lunch = user_data['Lunch Calories'].values[0]
        dinner = user_data['Dinner Calories'].values[0]
        snacks = user_data['Snacks Calories'].values[0]
        
    else:
        tk.messagebox.showerror("Error", "User ID not found.")
        return

    # Goals for the day
    goals = {
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'snacks': snacks
    }

    categories = list(goals.keys())
    goal_values = list(goals.values())
    consumed_values = [daily_totals[daily_totals['category'] == category]['calories'].sum() for category in categories]

    # Handle missing categories (where no food was consumed in a category)
    consumed_values = [val if val > 0 else 0 for val in consumed_values]

    # Create positions for the bars on the x-axis
    x = range(len(categories))

    # Bar width
    bar_width = 0.35

    # Create a figure for the bar chart
    fig_bar, ax_bar = plt.subplots(figsize=(8, 6))

    # Plot the goal and consumed bars side by side
    ax_bar.bar([i - bar_width/2 for i in x], goal_values, width=bar_width, color='green', alpha=0.6, label='Goal')
    ax_bar.bar([i + bar_width/2 for i in x], consumed_values, width=bar_width, color='blue', alpha=0.6, label='Consumed')

    ax_bar.set_ylabel('Calories')
    ax_bar.set_title(f"Daily Caloric Intake vs Goal for {name}")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(categories)
    ax_bar.legend()

    # Embed bar chart in Tkinter window
    canvas_bar = FigureCanvasTkAgg(fig_bar, master=root)
    canvas_bar.draw()
    canvas_bar.get_tk_widget().grid(row=11, column=0, padx=10, pady=10, columnspan=2)

# Function to log food consumption
def log_food():
    food = food_entry.get().strip()
    quantity = float(quantity_entry.get().strip())
    category = category_entry.get().strip().lower()
    user_id = user_id_entry.get().strip()

    if category not in ['breakfast', 'lunch', 'dinner', 'snacks']:
        tk.messagebox.showerror("Error", "Invalid category. Please choose from breakfast, lunch, dinner, snacks.")
        return

    # Get calories for the food item
    calories_per_unit, _, _, _ = get_calories(food)

    if calories_per_unit == 0:
        calories_per_unit = float(calories_entry.get().strip())
        carbs = float(carbs_entry.get().strip())
        fats = float(fats_entry.get().strip())
        proteins = float(proteins_entry.get().strip())
        update_food_dataset(food, calories_per_unit, carbs, fats, proteins)

    # Log the consumption
    log_consumption(datetime.now().strftime("%Y-%m-%d"), user_id, food, quantity, category, calories_per_unit * quantity)
    tk.messagebox.showinfo("Info", f"{food} logged successfully for User ID {user_id}!")

# Main Tkinter window setup
root = tk.Tk()
root.title("Daily Nutrition Tracker")

# User_ID entry
tk.Label(root, text="User ID:").grid(row=0, column=0)
user_id_entry = tk.Entry(root)
user_id_entry.grid(row=0, column=1)

# Food Entry
tk.Label(root, text="Food Item:").grid(row=1, column=0)
food_entry = tk.Entry(root)
food_entry.grid(row=1, column=1)

# Quantity Entry
tk.Label(root, text="Quantity:").grid(row=2, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=2, column=1)

# Category Entry
tk.Label(root, text="Category (breakfast, lunch, dinner, snacks):").grid(row=3, column=0)
category_entry = tk.Entry(root)
category_entry.grid(row=3, column=1)

# Calories Entry
tk.Label(root, text="Calories (if unknown, enter 0):").grid(row=4, column=0)
calories_entry = tk.Entry(root)
calories_entry.grid(row=4, column=1)

# Carbs Entry
tk.Label(root, text="Carbs (if unknown, enter 0):").grid(row=5, column=0)
carbs_entry = tk.Entry(root)
carbs_entry.grid(row=5, column=1)

# Fats Entry
tk.Label(root, text="Fats (if unknown, enter 0):").grid(row=6, column=0)
fats_entry = tk.Entry(root)
fats_entry.grid(row=6, column=1)

# Proteins Entry
tk.Label(root, text="Proteins (if unknown, enter 0):").grid(row=7, column=0)
proteins_entry = tk.Entry(root)
proteins_entry.grid(row=7, column=1)

# Log Food Button
log_button = ttk.Button(root, text="Log Food", command=log_food)
log_button.grid(row=8, column=0, columnspan=2)

# Date Entry for Chart Display
tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=9, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=9, column=1)

# Display Chart Button
chart_button = ttk.Button(root, text="Display Chart", command=lambda: display_charts(date_entry.get().strip(), user_id_entry.get().strip()))
chart_button.grid(row=10, column=0, columnspan=2)

root.mainloop()