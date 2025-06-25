from datetime import datetime

class Book:
    def __init__(self, title, author, isbn, year, quantity) -> None:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not author or not author.strip():
            raise ValueError("Author cannot be empty")
        if not isbn or not isbn.strip():
            raise ValueError("ISBN cannot be empty")
        if year < 0 or year > datetime.now().year:
            raise ValueError("Invalid year")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
            
        self.id = None
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.year = year
        self.quantity = quantity
        self.available = quantity

    def borrow_book(self) -> bool:
        if self.available > 0:
            self.available -= 1
            return True
        return False

    def return_book(self) -> bool:
        if self.available < self.quantity:
            self.available += 1
            return True
        return False

    def is_available(self) -> bool:
        return self.available > 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "quantity": self.quantity,
            "available": self.available
        }