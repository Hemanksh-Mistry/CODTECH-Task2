# Library Management System
# Develop a Python program to manage library resources such as books, magazines, and DVDs. The system should support functionalities like adding new items to the library, checking out and returning items, managing overdue fines, and searching for items by title, author, or category

# imporrtin the required libraries
import mysql.connector
from datetime import datetime, timedelta

# connecting to the database
def connect_db():
        return mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="LibraryDB"
        )

# Add a new item to the library
def add_item(title, author, category):
        db = connect_db()
        cursor = db.cursor()
        query = "INSERT INTO Items (title, author, category) VALUES (%s, %s, %s)"
        cursor.execute(query, (title, author, category))
        db.commit()
        cursor.close()
        db.close()

# Check out an item
def check_out_item(item_id, days=14):
        db = connect_db()
        cursor = db.cursor()
        due_date = datetime.now() + timedelta(days=days)
        query = "UPDATE Items SET available = FALSE, due_date = %s WHERE id = %s"
        cursor.execute(query, (due_date, item_id))
        db.commit()
        cursor.close()
        db.close()

# Return an item
def return_item(item_id):
        db = connect_db()
        cursor = db.cursor()
        query = "SELECT due_date FROM Items WHERE id = %s"
        cursor.execute(query, (item_id,))
        due_date = cursor.fetchone()[0]

        # Calculate overdue fine if applicable
        overdue_days = (datetime.now().date() - due_date).days
        overdue_fine = max(0, overdue_days * 1.00)  # Assume $1 fine per day

        query = "UPDATE Items SET available = TRUE, due_date = NULL, overdue_fine = %s WHERE id = %s"
        cursor.execute(query, (overdue_fine, item_id))
        db.commit()
        cursor.close()
        db.close()

# Search for items by title, author, or category
def search_items(search_term, search_type):
        db = connect_db()
        cursor = db.cursor()
        query = f"SELECT * FROM Items WHERE {search_type} LIKE %s"
        cursor.execute(query, ('%' + search_term + '%',))
        results = cursor.fetchall()
        cursor.close()
        db.close()
        return results

# Print available items in the library
def print_available_items():
        db = connect_db()
        cursor = db.cursor()
        query = "SELECT * FROM Items WHERE available = TRUE"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        print("Available Items:")
        print("ID | Title | Author | Category | Available | Due Date | Overdue Fine")
        for result in results:
                print(result)

# Print borrowed items in the library
def print_borrowed_items():
        db = connect_db()
        cursor = db.cursor()
        query = "SELECT * FROM Items WHERE available = FALSE"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        db.close()
        print("Borrowed Items:")
        print("ID | Title | Author | Category | Due Date")
        for result in results:
                print(result)

# Print menu for the library management system
def print_menu():
        print("Library Management System")
        print("1. Add Item")
        print("2. Check Out Item")
        print("3. Return Item")
        print("4. Search Items")
        print("5. Print Available Items")
        print("6. Print Borrowed Items")
        print("7. Exit")
        
        return (input("Enter your choice: "))

# Main function to test the library management system
def main():
        while True:
                
                choice = print_menu()
                
                if choice == '1':
                        title = input("Enter the title of the item: ")
                        author = input("Enter the author of the item: ")
                        category = input("Enter the category of the item (Book, Magazine, DVD): ")
                        add_item(title, author, category)
                        print("Item added successfully!")
                
                elif choice == '2':
                        item_id = input("Enter the ID of the item to check out: ")
                        check_out_item(item_id)
                        print("Item checked out successfully!")
                
                elif choice == '3':
                        item_id = input("Enter the ID of the item to return: ")
                        return_item(item_id)
                        print("Item returned successfully!")
                
                elif choice == '4':
                        search_term = input("Enter the search term: ")
                        search_type = input("Enter the search type (title, author, category): ")
                        results = search_items(search_term, search_type)
                        print("Search results:")
                        for result in results:
                                print(result)
                
                elif choice == '5':
                        print_available_items()
                
                elif choice == '6':
                        print_borrowed_items()

                elif choice == '7':
                        print("Exiting...")
                        break
                
                else:
                        print("Invalid choice. Please try again.")

if __name__ == "__main__":
        main()