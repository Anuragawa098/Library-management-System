"""
seed_sample_data.py
Populates the database with sample books, members, and issue records.
Run this once to quickly see the system in action / take screenshots for your GitHub README.
"""

import database

database.initialize_database()

# Sample books
database.add_book("The Pragmatic Programmer", "Andrew Hunt", "Technology", 3)
database.add_book("Clean Code", "Robert C. Martin", "Technology", 2)
database.add_book("Atomic Habits", "James Clear", "Self-Help", 4)
database.add_book("Introduction to Algorithms", "Thomas H. Cormen", "Computer Science", 2)
database.add_book("Wings of Fire", "A.P.J. Abdul Kalam", "Biography", 5)

# Sample members
database.add_member("Anurag Awasthi", "anurag935849@gmail.com")
database.add_member("Priya Sharma", "priya.sharma@example.com")
database.add_member("Rohit Verma", "rohit.verma@example.com")

# Issue a couple of books to demonstrate the workflow
success, msg = database.issue_book(1, 1)
print(msg)
success, msg = database.issue_book(3, 2)
print(msg)

print("\nSample data loaded successfully!")
print("Run 'python main.py' to explore the system, or check option 9 to generate an HTML report.")
