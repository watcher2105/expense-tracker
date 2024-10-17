import json
from collections import defaultdict
from datetime import datetime, timedelta
import calendar
import matplotlib.pyplot as plt

# File where the expense data will be saved
DATA_FILE = "expenses.json"

# Load expense data from file
def load_expenses():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            # Check if data is in list format, else return empty list
            if isinstance(data, list):
                return data
            else:
                print("Error: Data file is not in the expected format.")
                return []
    except FileNotFoundError:
        print("No previous expense data found. Starting fresh.")
        return []
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return []

# Save expense data to file
def save_expenses(expenses):
    with open(DATA_FILE, 'w') as file:
        json.dump(expenses, file, indent=4)

# Add a new expense entry
def add_expense(expenses):
    amount = float(input("Enter the expense amount: "))
    category = input("Enter the category (e.g., Food, Transport, Entertainment): ").capitalize()
    date_input = input("Enter the date (YYYY-MM-DD) or leave blank for today: ")
    
    # If no date is provided, use today's date
    if not date_input:
        date_input = datetime.today().strftime('%Y-%m-%d')
    
    # Create expense dictionary and append to list
    expense = {
        "amount": amount,
        "category": category,
        "date": date_input
    }
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense added successfully!")

# Delete an existing expense
def delete_expense(expenses):
    view_expenses(expenses)
    try:
        index = int(input("Enter the index of the expense to delete: ")) - 1
        # Check if index is within the list range
        if 0 <= index < len(expenses):
            deleted = expenses.pop(index)
            save_expenses(expenses)
            print(f"Deleted expense: {deleted}")
        else:
            print("Invalid index. No expense deleted.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Edit an existing expense
def edit_expense(expenses):
    view_expenses(expenses)
    try:
        index = int(input("Enter the index of the expense to edit: ")) - 1
        # Validate index and allow updating fields
        if 0 <= index < len(expenses):
            expense = expenses[index]
            print(f"Editing expense: {expense}")
            amount = input(f"Enter new amount (current: {expense['amount']}): ")
            category = input(f"Enter new category (current: {expense['category']}): ")
            date = input(f"Enter new date (current: {expense['date']}): ")

            if amount:
                expense["amount"] = float(amount)
            if category:
                expense["category"] = category.capitalize()
            if date:
                expense["date"] = date

            save_expenses(expenses)
            print("Expense updated successfully!")
        else:
            print("Invalid index. No expense edited.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Filter expenses within a specific date range
def filter_expenses_by_date(expenses, start_date, end_date):
    return [expense for expense in expenses if start_date <= datetime.strptime(expense["date"], "%Y-%m-%d").date() <= end_date]

# View summary of expenses based on user selection
def view_summary(expenses):
    if not expenses:
        print("No expenses found.")
        return
    
    print("\n--- Expense Summary ---")
    print("1. Total spending for a specific category")
    print("2. Total overall spending")
    print("3. Spending over time (daily, weekly, or monthly)")
    print("4. View graphical summary")
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        # Show total spending by category
        category = input("Enter the category to view spending for: ").capitalize()
        category_total = sum(expense["amount"] for expense in expenses if expense["category"] == category)
        print(f"\nTotal spending for {category}: ${category_total:.2f}")
    
    elif choice == "2":
        # Calculate total overall spending
        overall_total = sum(expense["amount"] for expense in expenses)
        print(f"\nTotal overall spending: ${overall_total:.2f}")
    
    elif choice == "3":
        # Show spending over a selected time frame
        print("\n--- Spending Over Time ---")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        time_choice = input("Choose a time period (1-3): ")
        
        if time_choice == "1":
            # Daily spending
            date_total = defaultdict(float)
            for expense in expenses:
                date_total[expense["date"]] += expense["amount"]
            for date, total in sorted(date_total.items()):
                print(f"{date}: ${total:.2f}")
        
        elif time_choice == "2":
            # Weekly spending based on user-specified start date
            start_date = datetime.strptime(input("Enter start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
            end_date = start_date + timedelta(days=7)
            weekly_expenses = filter_expenses_by_date(expenses, start_date, end_date)
            total_weekly_spending = sum(expense["amount"] for expense in weekly_expenses)
            print(f"Spending for the week starting {start_date}: ${total_weekly_spending:.2f}")
        
        elif time_choice == "3":
            # Monthly spending based on selected month and year
            month = int(input("Enter the month (1-12): "))
            year = int(input("Enter the year (e.g., 2024): "))
            first_day = datetime(year, month, 1).date()
            last_day = datetime(year, month, calendar.monthrange(year, month)[1]).date()
            monthly_expenses = filter_expenses_by_date(expenses, first_day, last_day)
            total_monthly_spending = sum(expense["amount"] for expense in monthly_expenses)
            print(f"Spending for {calendar.month_name[month]} {year}: ${total_monthly_spending:.2f}")
    
    elif choice == "4":
        # Display graphical summary of expenses by category
        view_graphical_summary(expenses)
    
    else:
        print("Invalid choice. Please enter a number between 1 and 4.")

# Display graphical summary of expenses as a bar chart
def view_graphical_summary(expenses):
    if not expenses:
        print("No expenses found for graphical summary.")
        return

    # Calculate total spending by category
    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense['category']] += expense['amount']

    # Plot category spending as a bar chart
    categories = list(category_totals.keys())
    totals = list(category_totals.values())
    plt.figure(figsize=(8, 5))
    plt.bar(categories, totals, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Total Spending')
    plt.title('Total Spending by Category')
    plt.xticks(rotation=90)  # Rotate category names vertically to avoid overlap
    plt.tight_layout()
    plt.show()

# Display all expenses with index numbers
def view_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\n--- Expenses ---")
    # Enumerate and display expenses with index for easy reference
    for i, expense in enumerate(expenses, start=1):
        print(f"{i}. {expense['date']} - {expense['category']} - ${expense['amount']:.2f}")

# Main loop to interact with the expense tracker
expenses = load_expenses()
while True:
    print("\n--- Personal Expense Tracker ---")
    print("1. Add Expense")
    print("2. View Summary")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        add_expense(expenses)
    elif choice == "2":
        view_summary(expenses)
    elif choice == "3":
        edit_expense(expenses)
    elif choice == "4":
        delete_expense(expenses)
    elif choice == "5":
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
