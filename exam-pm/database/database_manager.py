import sqlite3
from datetime import datetime
from models.book import Book
from models.reader import Reader
from models.loan import Loan

class DatabaseManager:
    def __init__(self, db_path="library.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT NOT NULL UNIQUE,
                year INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                available INTEGER NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                registration_date TEXT NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                reader_id INTEGER NOT NULL,
                loan_date TEXT NOT NULL,
                return_date TEXT NOT NULL,
                is_returned INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (reader_id) REFERENCES readers(id)
            )
        """)
        self.conn.commit()

    def add_book(self, book: Book) -> int:
        self.cursor.execute("""
            INSERT INTO books (title, author, isbn, year, quantity, available)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (book.title, book.author, book.isbn, book.year, book.quantity, book.available))
        self.conn.commit()
        book.id = self.cursor.lastrowid
        return book.id

    def get_book_by_id(self, book_id) -> Book | None:
        self.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        row = self.cursor.fetchone()
        if row:
            book = Book(row[1], row[2], row[3], row[4], row[5])
            book.id = row[0]
            book.available = row[6]
            return book
        return None

    def get_all_books(self) -> list[Book]:
        self.cursor.execute("SELECT * FROM books")
        books = []
        for row in self.cursor.fetchall():
            book = Book(row[1], row[2], row[3], row[4], row[5])
            book.id = row[0]
            book.available = row[6]
            books.append(book)
        return books

    def update_book(self, book_id, **kwargs) -> bool:
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        values.append(book_id)
        self.cursor.execute(f"UPDATE books SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_book(self, book_id) -> bool:
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def search_books(self, query) -> list[Book]:
        query = f"%{query}%"
        self.cursor.execute("""
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        """, (query, query, query))
        books = []
        for row in self.cursor.fetchall():
            book = Book(row[1], row[2], row[3], row[4], row[5])
            book.id = row[0]
            book.available = row[6]
            books.append(book)
        return books

    def add_reader(self, reader: Reader) -> int:
        self.cursor.execute("""
            INSERT INTO readers (name, email, phone, registration_date)
            VALUES (?, ?, ?, ?)
        """, (reader.name, reader.email, reader.phone, reader.registration_date.strftime("%Y-%m-%d %H:%M:%S")))
        self.conn.commit()
        reader.id = self.cursor.lastrowid
        return reader.id

    def get_reader_by_id(self, reader_id) -> Reader | None:
        self.cursor.execute("SELECT * FROM readers WHERE id = ?", (reader_id,))
        row = self.cursor.fetchone()
        if row:
            reader = Reader(row[1], row[2], row[3])
            reader.id = row[0]
            reader.registration_date = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            return reader
        return None

    def get_all_readers(self) -> list[Reader]:
        self.cursor.execute("SELECT * FROM readers")
        readers = []
        for row in self.cursor.fetchall():
            reader = Reader(row[1], row[2], row[3])
            reader.id = row[0]
            reader.registration_date = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            readers.append(reader)
        return readers

    def update_reader(self, reader_id, **kwargs) -> bool:
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        values.append(reader_id)
        self.cursor.execute(f"UPDATE readers SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_reader(self, reader_id) -> bool:
        self.cursor.execute("DELETE FROM readers WHERE id = ?", (reader_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0


    def add_loan(self, loan: Loan) -> int:
        self.cursor.execute("""
            INSERT INTO loans (book_id, reader_id, loan_date, return_date, is_returned)
            VALUES (?, ?, ?, ?, ?)
        """, (
            loan.book_id, 
            loan.reader_id, 
            loan.loan_date.strftime("%Y-%m-%d %H:%M:%S"), 
            loan.return_date.strftime("%Y-%m-%d %H:%M:%S"),
            int(loan.is_returned)
        ))
        self.conn.commit()
        loan.id = self.cursor.lastrowid
        return loan.id

    def get_loan_by_id(self, loan_id) -> Loan | None:
        self.cursor.execute("SELECT * FROM loans WHERE id = ?", (loan_id,))
        row = self.cursor.fetchone()
        if row:
            loan = Loan(
                row[1], 
                row[2], 
                datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            )
            loan.id = row[0]
            loan.is_returned = bool(row[5])
            return loan
        return None

    def get_all_loans(self) -> list[Loan]:
        self.cursor.execute("SELECT * FROM loans")
        loans = []
        for row in self.cursor.fetchall():
            loan = Loan(
                row[1], 
                row[2], 
                datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            )
            loan.id = row[0]
            loan.is_returned = bool(row[5])
            loans.append(loan)
        return loans

    def update_loan(self, loan_id, **kwargs) -> bool:
        set_clause = ", ".join(f"{k} = ?" for k in kwargs)
        values = list(kwargs.values())
        values.append(loan_id)
        self.cursor.execute(f"UPDATE loans SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def get_reader_loans(self, reader_id) -> list[Loan]:
        self.cursor.execute("SELECT * FROM loans WHERE reader_id = ?", (reader_id,))
        loans = []
        for row in self.cursor.fetchall():
            loan = Loan(
                row[1], 
                row[2], 
                datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            )
            loan.id = row[0]
            loan.is_returned = bool(row[5])
            loans.append(loan)
        return loans

    def get_overdue_loans(self) -> list[Loan]:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            SELECT * FROM loans 
            WHERE return_date < ? AND is_returned = 0
        """, (now,))
        loans = []
        for row in self.cursor.fetchall():
            loan = Loan(
                row[1], 
                row[2], 
                datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S"),
                datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
            )
            loan.id = row[0]
            loan.is_returned = bool(row[5])
            loans.append(loan)
        return loans