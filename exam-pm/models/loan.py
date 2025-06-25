# models/loan.py
from datetime import datetime, timedelta

class Loan:
    def __init__(self, book_id, reader_id, loan_date, return_date) -> None:
        self.id = None
        self.book_id = book_id
        self.reader_id = reader_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.is_returned = False

    def return_book(self) -> bool:
        if not self.is_returned:
            self.is_returned = True
            return True
        return False

    def is_overdue(self) -> bool:
        return datetime.now() > self.return_date and not self.is_returned

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "book_id": self.book_id,
            "reader_id": self.reader_id,
            "loan_date": self.loan_date.strftime("%Y-%m-%d %H:%M:%S"),
            "return_date": self.return_date.strftime("%Y-%m-%d %H:%M:%S"),
            "is_returned": self.is_returned,
            "is_overdue": self.is_overdue()
        }