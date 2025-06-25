from datetime import datetime, timedelta
from models.loan import Loan

class LoanController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def create_loan(self, book_id, reader_id, loan_date=None, return_date=None) -> int:
        if loan_date is None:
            loan_date = datetime.now()
        if return_date is None:
            return_date = loan_date + timedelta(days=14)  # 2 weeks loan period
        loan = Loan(book_id, reader_id, loan_date, return_date)
        return self.db.add_loan(loan)

    def get_loan(self, loan_id) -> Loan | None:
        return self.db.get_loan_by_id(loan_id)

    def get_all_loans(self) -> list[Loan]:
        return self.db.get_all_loans()

    def return_book(self, loan_id) -> bool:
        loan = self.db.get_loan_by_id(loan_id)
        if loan and loan.return_book():
            return self.db.update_loan(loan_id, is_returned=1)
        return False

    def get_overdue_loans(self) -> list[Loan]:
        return self.db.get_overdue_loans()

    def get_reader_loans(self, reader_id) -> list[Loan]:
        return self.db.get_reader_loans(reader_id)