import pandas as  pd
import os
from datetime import datetime, timedelta

# for manually adding the expenses in an empty list and storing the values in list
# A list to store expenses
'''expenses = []'''
#Function to add an Expenses
'''def add_expense(date, category, amount):
    expense = {
        'date': date,
        'category': category,
        'amount': amount
    }
    expenses.append(expense)'''
# Example usage of manually adding expenses
'''add_expense('2024-10-13', 'Groceries', 50.75)
add_expense('2024-10-14', 'Utilities', 120.00)
add_expense('2024-10-15', 'Entertainment', 40.50)'''



# Load expenses from a CSV file
def load_expenses_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, parse_dates=['Date'], index_col=None)
    else:
        print(f"{file_path} not found. Starting with an empty expense list.")
        return pd.DataFrame(columns=['Category', 'Amount', 'Date'])

# Save expenses to a CSV file
def save_expenses_csv(expenses, file_path):
    expenses.to_csv(file_path, index=False)
    print(f"Expenses saved to {file_path}")

# Path to the CSV file
file_path = "expenses.csv"
expenses = load_expenses_csv(file_path)



# Function to add an expense with a date to the CSV file
def add_expense_csv(expenses, category, amount, date):
    new_expense = pd.DataFrame([[category, amount, date]], columns=['Category', 'Amount', 'Date'])
    expenses = pd.concat([expenses, new_expense], ignore_index=True)
    return expenses

# Example: Add a new expense
categories = ["Food", "Transport", "Entertainment", "Rent", "Trips", "Clothes"]
print("Available categories: ", ", ".join(categories))

category = input("Enter the category of the expense: ")
if category in categories:
    try:
        amount = float(input("Enter the amount: "))
        date = input("Enter the date (YYYY-MM-DD) of the expense: ")
        date = pd.to_datetime(date)
        expenses = add_expense_csv(expenses, category, amount, date)
        save_expenses_csv(expenses, file_path)
    except ValueError:
        print("Invalid input. Please enter valid data.")
else:
    print(f"Category '{category}' is not recognized.")


# Function to display the current summary of expenses
def show_summary_csv(expenses):
    if expenses.empty:
        print("\nNo expenses recorded yet.\n")
        return
    
    total_spent = expenses['Amount'].sum()
    print("\nExpense Summary:")
    print(expenses)
    print(f"\nTotal Spent: ${total_spent:.2f}\n")

# Show current expenses
show_summary_csv(expenses)

# Function to calculate spending over different time periods
def calculate_spending(expenses, period='daily'):
    today = datetime.today()

    if period == 'daily':
        filtered_expenses = expenses[expenses['Date'] == today]
    elif period == 'weekly':
        week_ago = today - timedelta(days=7)
        filtered_expenses = expenses[(expenses['Date'] >= week_ago) & (expenses['Date'] <= today)]
    elif period == 'monthly':
        filtered_expenses = expenses[expenses['Date'].dt.month == today.month]
    else:
        print("Invalid period. Choose 'daily', 'weekly', or 'monthly'.")
        return
    
    total_spent = filtered_expenses['Amount'].sum()
    print(f"\n{period.capitalize()} Expense Summary:")
    print(filtered_expenses)
    print(f"\nTotal Spent {period.capitalize()}: ${total_spent:.2f}\n")

# Example: Calculate daily, weekly, and monthly spending
print("Calculating daily spending:")
calculate_spending(expenses, 'daily')

print("Calculating weekly spending:")
calculate_spending(expenses, 'weekly')

print("Calculating monthly spending:")
calculate_spending(expenses, 'monthly')

# Function to delete an expense based on category and date
def delete_expense_csv(expenses, category, date):
    date = pd.to_datetime(date)
    expenses = expenses[~((expenses['Category'] == category) & (expenses['Date'] == date))]
    print(f"Deleted expense '{category}' on {date.date()}.")
    return expenses

# Example: Delete an expense
category = input("Enter the category to delete: ")
date = input("Enter the date (YYYY-MM-DD) of the expense to delete: ")
expenses = delete_expense_csv(expenses, category, date)
save_expenses_csv(expenses, file_path)
show_summary_csv(expenses)
