"""
main.py
Command-line interface for the Library Management System.
Run this file to start the application.
"""

import database
import report


def print_books(books):
    if not books:
        print("No books found.\n")
        return
    print(f"\n{'ID':<5}{'Title':<30}{'Author':<20}{'Genre':<15}{'Total':<8}{'Available':<10}")
    print("-" * 88)
    for b in books:
        print(f"{b['book_id']:<5}{b['title']:<30}{b['author']:<20}{b['genre'] or '-':<15}"
              f"{b['total_copies']:<8}{b['available_copies']:<10}")
    print()


def print_members(members):
    if not members:
        print("No members found.\n")
        return
    print(f"\n{'ID':<5}{'Name':<25}{'Email':<30}{'Joined On':<12}")
    print("-" * 72)
    for m in members:
        print(f"{m['member_id']:<5}{m['name']:<25}{m['email']:<30}{m['joined_on']:<12}")
    print()


def menu():
    print("""
========== LIBRARY MANAGEMENT SYSTEM ==========
1. Add a new book
2. View all books
3. Search books
4. Register a new member
5. View all members
6. Issue a book
7. Return a book
8. View currently issued books
9. Generate HTML report
0. Exit
=================================================""")


def main():
    database.initialize_database()

    while True:
        menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Book title: ").strip()
            author = input("Author: ").strip()
            genre = input("Genre: ").strip()
            copies = int(input("Number of copies: ").strip())
            database.add_book(title, author, genre, copies)
            print("Book added successfully.\n")

        elif choice == "2":
            print_books(database.get_all_books())

        elif choice == "3":
            keyword = input("Search by title/author/genre: ").strip()
            print_books(database.search_books(keyword))

        elif choice == "4":
            name = input("Member name: ").strip()
            email = input("Member email: ").strip()
            try:
                database.add_member(name, email)
                print("Member registered successfully.\n")
            except Exception as e:
                print(f"Error: could not register member ({e})\n")

        elif choice == "5":
            print_members(database.get_all_members())

        elif choice == "6":
            book_id = int(input("Book ID to issue: ").strip())
            member_id = int(input("Member ID: ").strip())
            success, message = database.issue_book(book_id, member_id)
            print(message + "\n")

        elif choice == "7":
            issue_id = int(input("Issue ID to return: ").strip())
            success, message = database.return_book(issue_id)
            print(message + "\n")

        elif choice == "8":
            rows = database.get_currently_issued_books()
            if not rows:
                print("No books are currently issued.\n")
            else:
                print(f"\n{'Issue ID':<10}{'Title':<30}{'Member':<20}{'Issue Date':<12}")
                print("-" * 72)
                for r in rows:
                    print(f"{r['issue_id']:<10}{r['title']:<30}{r['member_name']:<20}{r['issue_date']:<12}")
                print()

        elif choice == "9":
            filename = report.generate_html_report()
            print(f"Report generated: {filename}\n")

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    main()
