# 📚 Library Management System

A command-line Library Management System built with **Python** and **SQLite**, with an auto-generated **HTML** status report. Built as a portfolio project to demonstrate database design, CRUD operations, and clean Python code structure.

## Features

- Add, view, and search books by title/author/genre
- Register library members
- Issue books to members and track due copies
- Return books and automatically update stock
- View all currently issued books
- Generate a styled HTML report of the library's status (stock levels + active issues)

## Tech Stack

- **Python 3** – core application logic
- **SQLite** – relational database (no separate DB server needed)
- **HTML/CSS** – auto-generated report

## Project Structure

```
library-management-system/
│
├── main.py              # CLI entry point — run this to start the app
├── database.py           # All SQL queries and database logic
├── report.py              # Generates the HTML status report
├── seed_sample_data.py    # Optional: loads sample data to try the app quickly
├── requirements.txt        # (No external dependencies — uses Python's built-in sqlite3)
└── README.md
```

## How to Run

1. Clone this repository
   ```bash
   git clone https://github.com/<your-username>/library-management-system.git
   cd library-management-system
   ```

2. (Optional) Load sample data to explore the system immediately
   ```bash
   python seed_sample_data.py
   ```

3. Run the application
   ```bash
   python main.py
   ```

4. Follow the on-screen menu to add books, register members, issue/return books, or generate a report (option 9 creates `library_report.html`).

## Database Schema

**books** — `book_id, title, author, genre, total_copies, available_copies`

**members** — `member_id, name, email, joined_on`

**issued_books** — `issue_id, book_id, member_id, issue_date, return_date`

The `issued_books` table links `books` and `members` with foreign keys, and `return_date` is `NULL` while a book is still checked out — a simple example of relational design.

## What I Learned

- Designing a normalized relational schema with foreign key relationships
- Writing parameterized SQL queries to prevent SQL injection
- Structuring a Python project into logical modules (database layer, UI layer, report layer)
- Generating dynamic HTML from Python data

## Possible Future Improvements

- Add a Flask web interface instead of CLI
- Add due dates and late-return fines
- Add user authentication for librarian vs. member roles

---
*Built by Anurag Awasthi — B.Tech CSE Student*
