import pytest
import sys
import os
from datetime import datetime, timedelta

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models.book import Book
from models.reader import Reader
from models.loan import Loan


class TestBook:
    """Тесты для класса Book"""

    def test_book_creation(self):
        """Тест создания книги"""
        book = Book("Война и мир", "Лев Толстой", "978-5-389-12345-6", 1869, 5)

        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"
        assert book.isbn == "978-5-389-12345-6"
        assert book.year == 1869
        assert book.quantity == 5
        assert book.available == 5
        assert book.id is None  # ID будет установлен при сохранении в БД

    def test_book_borrow(self):
        """Тест выдачи книги"""
        book = Book(
            "Преступление и наказание",
            "Федор Достоевский",
            "978-5-389-12346-7",
            1866,
            3,
        )

        assert book.available == 3
        assert book.is_available() == True

        book.borrow_book()
        assert book.available == 2
        assert book.is_available() == True

        book.borrow_book()
        book.borrow_book()
        assert book.available == 0
        assert book.is_available() == False

    def test_book_return(self):
        """Тест возврата книги"""
        book = Book(
            "Мастер и Маргарита", "Михаил Булгаков", "978-5-389-12347-8", 1967, 2
        )

        book.borrow_book()
        assert book.available == 1

        book.return_book()
        assert book.available == 2
        assert book.is_available() == True

    def test_book_to_dict(self):
        """Тест преобразования книги в словарь"""
        book = Book("Идиот", "Федор Достоевский", "978-5-389-12348-9", 1869, 4)
        book.id = 1

        book_dict = book.to_dict()

        assert book_dict["id"] == 1
        assert book_dict["title"] == "Идиот"
        assert book_dict["author"] == "Федор Достоевский"
        assert book_dict["isbn"] == "978-5-389-12348-9"
        assert book_dict["year"] == 1869
        assert book_dict["quantity"] == 4
        assert book_dict["available"] == 4

    def test_book_validation(self):
        """Тест валидации данных книги"""
        # Тест с некорректным годом
        with pytest.raises(ValueError):
            Book("Книга", "Автор", "123-456", -100, 1)

        # Тест с некорректным количеством
        with pytest.raises(ValueError):
            Book("Книга", "Автор", "123-456", 2020, -1)

        # Тест с пустым названием
        with pytest.raises(ValueError):
            Book("", "Автор", "123-456", 2020, 1)


class TestReader:
    """Тесты для класса Reader"""

    def test_reader_creation(self):
        """Тест создания читателя"""
        reader = Reader("Иван Иванов", "ivan@example.com", "+7-999-123-45-67")

        assert reader.name == "Иван Иванов"
        assert reader.email == "ivan@example.com"
        assert reader.phone == "+7-999-123-45-67"
        assert reader.id is None
        assert isinstance(reader.registration_date, datetime)

    def test_reader_update_info(self):
        """Тест обновления информации о читателе"""
        reader = Reader("Петр Петров", "petr@example.com", "+7-999-123-45-68")

        reader.update_info(name="Петр Сидоров", email="petr.new@example.com")

        assert reader.name == "Петр Сидоров"
        assert reader.email == "petr.new@example.com"
        assert reader.phone == "+7-999-123-45-68"  # Не изменился

    def test_reader_to_dict(self):
        """Тест преобразования читателя в словарь"""
        reader = Reader("Анна Сидорова", "anna@example.com", "+7-999-123-45-69")
        reader.id = 1

        reader_dict = reader.to_dict()

        assert reader_dict["id"] == 1
        assert reader_dict["name"] == "Анна Сидорова"
        assert reader_dict["email"] == "anna@example.com"
        assert reader_dict["phone"] == "+7-999-123-45-69"
        assert "registration_date" in reader_dict

    def test_reader_validation(self):
        """Тест валидации данных читателя"""
        # Тест с некорректным email
        with pytest.raises(ValueError):
            Reader("Имя", "некорректный-email", "+7-999-123-45-67")

        # Тест с пустым именем
        with pytest.raises(ValueError):
            Reader("", "test@example.com", "+7-999-123-45-67")


class TestLoan:
    """Тесты для класса Loan"""

    def test_loan_creation(self):
        """Тест создания выдачи"""
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan = Loan(1, 1, loan_date, return_date)

        assert loan.book_id == 1
        assert loan.reader_id == 1
        assert loan.loan_date == loan_date
        assert loan.return_date == return_date
        assert loan.is_returned == False
        assert loan.id is None

    def test_loan_return_book(self):
        """Тест возврата книги"""
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan = Loan(1, 1, loan_date, return_date)
        assert loan.is_returned == False

        loan.return_book()
        assert loan.is_returned == True

    def test_loan_is_overdue(self):
        """Тест проверки просрочки"""
        loan_date = datetime.now() - timedelta(days=20)
        return_date = loan_date + timedelta(days=14)

        loan = Loan(1, 1, loan_date, return_date)
        assert loan.is_overdue() == True

        # Не просроченная книга
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)
        loan = Loan(1, 1, loan_date, return_date)
        assert loan.is_overdue() == False

    def test_loan_to_dict(self):
        """Тест преобразования выдачи в словарь"""
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan = Loan(1, 1, loan_date, return_date)
        loan.id = 1

        loan_dict = loan.to_dict()

        assert loan_dict["id"] == 1
        assert loan_dict["book_id"] == 1
        assert loan_dict["reader_id"] == 1
        assert loan_dict["loan_date"] == loan_date
        assert loan_dict["return_date"] == return_date
        assert loan_dict["is_returned"] == False

    def test_loan_validation(self):
        """Тест валидации данных выдачи"""
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        # Тест с некорректными ID
        with pytest.raises(ValueError):
            Loan(-1, 1, loan_date, return_date)

        with pytest.raises(ValueError):
            Loan(1, -1, loan_date, return_date)

        # Тест с некорректными датами
        with pytest.raises(ValueError):
            Loan(1, 1, return_date, loan_date)  # Дата возврата раньше даты выдачи


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
