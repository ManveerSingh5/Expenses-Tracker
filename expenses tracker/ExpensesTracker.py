# -------------------------------
# EXPENSE TRACKER (Personal Budget Manager)
# Author : Manveer Singh
# Language : Python
# -------------------------------

import csv
from datetime import datetime

# -------------------------------
# FILE SETUP
# -------------------------------
FILENAME = "expenses.csv"

# Create file with headers if it doesn't exist
try:
    with open(FILENAME, 'x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Note"])
except FileExistsError:
    pass


# -------------------------------
# FUNCTION : Add a new expense
# -------------------------------
def add_expense():
    category = input("Enter category (Food/Travel/Shopping/Others): ").capitalize()
    try:
        amount = float(input("Enter amount: ₹"))
    except ValueError:
        print(" Invalid amount. Please enter a number.")
        return

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    note = input("Enter note/description: ")

    # Save to file
    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])

    print(f" Expense added successfully: ₹{amount} for {category}")


# -------------------------------
# FUNCTION : View all expenses
# -------------------------------
def view_expenses():
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
            if len(data) <= 1:
                print("No expenses recorded yet.")
                return

            print("\n----- All Expenses -----")
            print("{:<12} {:<15} {:<10} {}".format("Date", "Category", "Amount", "Note"))
            print("-" * 50)
            total = 0
            for row in data[1:]:
                print("{:<12} {:<15} ₹{:<9} {}".format(row[0], row[1], row[2], row[3]))
                total += float(row[2])
            print("-" * 50)
            print(f"Total Spent: ₹{total}")
    except FileNotFoundError:
        print("Error: Expense file not found.")


# -------------------------------
# FUNCTION : View summary (category-wise + balance)
# -------------------------------
def view_summary(salary):
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.DictReader(file)
            summary = {}
            total_spent = 0

            for row in reader:
                category = row["Category"]
                amount = float(row["Amount"])
                total_spent += amount
                summary[category] = summary.get(category, 0) + amount

            if total_spent == 0:
                print("No expenses to summarize.")
                return

            print("\n----- Expense Summary -----")
            for category, total in summary.items():
                print(f"{category:<15}: ₹{total}")
            print("----------------------------")
            print(f"Total Spent: ₹{total_spent}")
            print(f"Remaining Balance: ₹{salary - total_spent}")
    except FileNotFoundError:
        print("Error: Expense file not found.")


# -------------------------------
# FUNCTION : Delete an expense
# -------------------------------
def delete_expense():
    view_expenses()
    try:
        record_no = int(input("\nEnter the record number to delete (starting from 1): "))
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

        if record_no < 1 or record_no >= len(data):
            print(" Invalid record number.")
            return

        removed = data.pop(record_no)
        with open(FILENAME, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)

        print(f" Deleted record: {removed}")
    except Exception as e:
        print(f"Error deleting expense: {e}")


# -------------------------------
# MAIN PROGRAM
# -------------------------------
def main():
    print("=====================================")
    print("        EXPENSE TRACKER             ")
    print("=====================================")

    # Take monthly salary input
    while True:
        try:
            salary = float(input("Enter your monthly salary: ₹"))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Menu loop
    while True:
        print("\n====== MENU ======")
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. View Summary (Category-wise + Remaining Balance)")
        print("4. Delete an Expense")
        print("5. Exit")
        print("==================")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_summary(salary)
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            print("\nThank you for using Expense Tracker")
            print("Your data is safely saved in 'expenses.csv'")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


# -------------------------------
# PROGRAM ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    main()
