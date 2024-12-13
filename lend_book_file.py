import json
from datetime import datetime, timedelta

BOOKS_FILE = "all_books.json"
LEND_FILE = "lend_info.json"

def load_books():
    try:
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: Could not load books file. Starting with an empty library.")
        return []

def save_books(all_books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(all_books, file, indent=4)

def load_lend_info():
    try:
        with open(LEND_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_lend_info(lend_info):
    with open(LEND_FILE, "w") as file:
        json.dump(lend_info, file, indent=4)

def lend_book():
    all_books = load_books()
    lend_info = load_lend_info()

    print("\nAvailable Books:")
    for book in all_books:
        print(f"Title: {book['title']} (Quantity: {book['quantity']})")

    book_title = input("\nEnter the title of the book to lend: ").strip()
    book = next((b for b in all_books if b["title"].lower() == book_title.lower()), None)

    if not book:
        print("Error: Book not found in the library.")
        return

    if book["quantity"] <= 0:
        print("Error: No copies available for lending.")
        return

    borrower_name = input("Enter the borrower's name: ").strip()
    phone_number = input("Enter the borrower's phone number: ").strip()
    due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")

    # Add to lend info
    lend_info[borrower_name] = {
        "phone_number": phone_number,
        "book_title": book_title,
        "due_date": due_date
    }

    # Update book quantity
    book["quantity"] -= 1
    save_books(all_books)
    save_lend_info(lend_info)

    print(f"Success: Book '{book_title}' lent to {borrower_name}. Due date: {due_date}")

def return_book():
    all_books = load_books()
    lend_info = load_lend_info()

    borrower_name = input("\nEnter the borrower's name to return a book: ").strip()

    if borrower_name not in lend_info:
        print("Error: Borrower not found.")
        return

    book_title = lend_info[borrower_name]["book_title"]
    book = next((b for b in all_books if b["title"].lower() == book_title.lower()), None)

    if not book:
        print("Error: Book record not found.")
        return

    # Remove from lend info
    del lend_info[borrower_name]

    # Update book quantity
    book["quantity"] += 1
    save_books(all_books)
    save_lend_info(lend_info)

    print(f"Success: Book '{book_title}' returned by {borrower_name}.")

def lend_menu():
    while True:
        print("\nLend Book Menu:")
        print("1. Lend a Book")
        print("2. Return a Book")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            lend_book()
        elif choice == "2":
            return_book()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")
