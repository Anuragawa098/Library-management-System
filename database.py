"""
database.py
Handles all database operations for the Library Management System.
Uses SQLite so the project runs anywhere with zero setup.
"""

import sqlite3
from datetime import datetime

DB_NAME = "library.db"


def get_connection():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def initialize_database():
    """Create the required tables if they don't already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            total_copies INTEGER NOT NULL DEFAULT 1,
            available_copies INTEGER NOT NULL DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            joined_on TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issued_books (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (book_id),
            FOREIGN KEY (member_id) REFERENCES members (member_id)
        )
    """)

    conn.commit()
    conn.close()


# ---------- BOOK OPERATIONS ----------

def add_book(title, author, genre, copies):
    conn = get_connection()
    conn.execute(
        "INSERT INTO books (title, author, genre, total_copies, available_copies) "
        "VALUES (?, ?, ?, ?, ?)",
        (title, author, genre, copies, copies)
    )
    conn.commit()
    conn.close()


def get_all_books():
    conn = get_connection()
    books = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
    conn.close()
    return books


def search_books(keyword):
    conn = get_connection()
    query = "%" + keyword + "%"
    books = conn.execute(
        "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?",
        (query, query, query)
    ).fetchall()
    conn.close()
    return books


def update_available_copies(book_id, change):
    """change = -1 when issuing a book, +1 when returning one."""
    conn = get_connection()
    conn.execute(
        "UPDATE books SET available_copies = available_copies + ? WHERE book_id = ?",
        (change, book_id)
    )
    conn.commit()
    conn.close()


# ---------- MEMBER OPERATIONS ----------

def add_member(name, email):
    conn = get_connection()
    joined_on = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        "INSERT INTO members (name, email, joined_on) VALUES (?, ?, ?)",
        (name, email, joined_on)
    )
    conn.commit()
    conn.close()


def get_all_members():
    conn = get_connection()
    members = conn.execute("SELECT * FROM members ORDER BY name").fetchall()
    conn.close()
    return members


# ---------- ISSUE / RETURN OPERATIONS ----------

def issue_book(book_id, member_id):
    conn = get_connection()
    book = conn.execute("SELECT available_copies FROM books WHERE book_id = ?", (book_id,)).fetchone()

    if book is None:
        conn.close()
        return False, "Book not found."
    if book["available_copies"] <= 0:
        conn.close()
        return False, "No copies available right now."

    issue_date = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        "INSERT INTO issued_books (book_id, member_id, issue_date, return_date) "
        "VALUES (?, ?, ?, NULL)",
        (book_id, member_id, issue_date)
    )
    conn.commit()
    conn.close()
    update_available_copies(book_id, -1)
    return True, "Book issued successfully."


def return_book(issue_id):
    conn = get_connection()
    record = conn.execute("SELECT * FROM issued_books WHERE issue_id = ?", (issue_id,)).fetchone()

    if record is None:
        conn.close()
        return False, "Issue record not found."
    if record["return_date"] is not None:
        conn.close()
        return False, "This book was already returned."

    return_date = datetime.now().strftime("%Y-%m-%d")
    conn.execute(
        "UPDATE issued_books SET return_date = ? WHERE issue_id = ?",
        (return_date, issue_id)
    )
    conn.commit()
    conn.close()
    update_available_copies(record["book_id"], 1)
    return True, "Book returned successfully."


def get_currently_issued_books():
    """Books that are issued but not yet returned, with book and member details."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT issued_books.issue_id, books.title, members.name AS member_name,
               issued_books.issue_date
        FROM issued_books
        JOIN books ON books.book_id = issued_books.book_id
        JOIN members ON members.member_id = issued_books.member_id
        WHERE issued_books.return_date IS NULL
        ORDER BY issued_books.issue_date
    """).fetchall()
    conn.close()
    return rows
