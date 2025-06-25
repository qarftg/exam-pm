import pytest
import sys
import os
import tempfile
from datetime import datetime, timedelta

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from database.database_manager import DatabaseManager
from models.book import Book
from models.reader import Reader
from models.loan import Loan


class TestDatabaseManager:
    """Тесты для DatabaseManager"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        # Создаем временную базу данных для тестов
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.db_manager.create_tables()

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.db_manager.close()

    def test_create_tables(self):
        """Тест создания таблиц"""
        # Проверяем, что таблицы созданы
        cursor = self.db_manager.connection.cursor()

        # Проверяем таблицу книг
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='books'"
        )
        assert cursor.fetchone() is not None

        # Проверяем таблицу читателей
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='readers'"
        )
        assert cursor.fetchone() is not None

        # Проверяем таблицу выдач
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='loans'"
        )
        assert cursor.fetchone() is not None

    def test_add_book(self):
        """Тест добавления книги в базу данных"""
        book = Book("Война и мир", "Лев Толстой", "978-5-389-12345-6", 1869, 5)

        book_id = self.db_manager.add_book(book)
        assert book_id is not None
        assert isinstance(book_id, int)

        # Проверяем, что книга сохранена в базе
        saved_book = self.db_manager.get_book_by_id(book_id)
        assert saved_book is not None
        assert saved_book.title == "Война и мир"
        assert saved_book.author == "Лев Толстой"

    def test_get_book_by_id(self):
        """Тест получения книги по ID"""
        book = Book(
            "Преступление и наказание",
            "Федор Достоевский",
            "978-5-389-12346-7",
            1866,
            3,
        )
        book_id = self.db_manager.add_book(book)

        retrieved_book = self.db_manager.get_book_by_id(book_id)
        assert retrieved_book is not None
        assert retrieved_book.title == "Преступление и наказание"
        assert retrieved_book.author == "Федор Достоевский"
        assert retrieved_book.id == book_id

    def test_get_all_books(self):
        """Тест получения всех книг"""
        # Добавляем несколько книг
        book1 = Book("Книга 1", "Автор 1", "123-1", 2020, 1)
        book2 = Book("Книга 2", "Автор 2", "123-2", 2021, 2)

        self.db_manager.add_book(book1)
        self.db_manager.add_book(book2)

        books = self.db_manager.get_all_books()
        assert len(books) >= 2

        # Проверяем, что все книги имеют ID
        for book in books:
            assert book.id is not None

    def test_update_book(self):
        """Тест обновления книги"""
        book = Book("Старое название", "Старый автор", "123-456", 2020, 1)
        book_id = self.db_manager.add_book(book)

        # Обновляем книгу
        self.db_manager.update_book(
            book_id, title="Новое название", author="Новый автор"
        )

        # Проверяем изменения
        updated_book = self.db_manager.get_book_by_id(book_id)
        assert updated_book.title == "Новое название"
        assert updated_book.author == "Новый автор"

    def test_delete_book(self):
        """Тест удаления книги"""
        book = Book("Книга для удаления", "Автор", "123-789", 2020, 1)
        book_id = self.db_manager.add_book(book)

        # Удаляем книгу
        self.db_manager.delete_book(book_id)

        # Проверяем, что книга удалена
        deleted_book = self.db_manager.get_book_by_id(book_id)
        assert deleted_book is None

    def test_search_books(self):
        """Тест поиска книг"""
        book1 = Book("Война и мир", "Лев Толстой", "123-1", 1869, 1)
        book2 = Book("Мир и война", "Другой автор", "123-2", 2020, 1)

        self.db_manager.add_book(book1)
        self.db_manager.add_book(book2)

        # Поиск по названию
        results = self.db_manager.search_books("война")
        assert len(results) >= 1

        # Поиск по автору
        results = self.db_manager.search_books("Толстой")
        assert len(results) >= 1

    def test_add_reader(self):
        """Тест добавления читателя в базу данных"""
        reader = Reader("Иван Иванов", "ivan@example.com", "+7-999-123-45-67")

        reader_id = self.db_manager.add_reader(reader)
        assert reader_id is not None
        assert isinstance(reader_id, int)

        # Проверяем, что читатель сохранен в базе
        saved_reader = self.db_manager.get_reader_by_id(reader_id)
        assert saved_reader is not None
        assert saved_reader.name == "Иван Иванов"
        assert saved_reader.email == "ivan@example.com"

    def test_get_reader_by_id(self):
        """Тест получения читателя по ID"""
        reader = Reader("Петр Петров", "petr@example.com", "+7-999-123-45-68")
        reader_id = self.db_manager.add_reader(reader)

        retrieved_reader = self.db_manager.get_reader_by_id(reader_id)
        assert retrieved_reader is not None
        assert retrieved_reader.name == "Петр Петров"
        assert retrieved_reader.email == "petr@example.com"
        assert retrieved_reader.id == reader_id

    def test_get_all_readers(self):
        """Тест получения всех читателей"""
        # Добавляем несколько читателей
        reader1 = Reader("Читатель 1", "reader1@example.com", "+7-999-111-11-11")
        reader2 = Reader("Читатель 2", "reader2@example.com", "+7-999-222-22-22")

        self.db_manager.add_reader(reader1)
        self.db_manager.add_reader(reader2)

        readers = self.db_manager.get_all_readers()
        assert len(readers) >= 2

        # Проверяем, что все читатели имеют ID
        for reader in readers:
            assert reader.id is not None

    def test_update_reader(self):
        """Тест обновления читателя"""
        reader = Reader("Старое имя", "old@example.com", "+7-999-123-45-67")
        reader_id = self.db_manager.add_reader(reader)

        # Обновляем читателя
        self.db_manager.update_reader(
            reader_id, name="Новое имя", email="new@example.com"
        )

        # Проверяем изменения
        updated_reader = self.db_manager.get_reader_by_id(reader_id)
        assert updated_reader.name == "Новое имя"
        assert updated_reader.email == "new@example.com"

    def test_delete_reader(self):
        """Тест удаления читателя"""
        reader = Reader(
            "Читатель для удаления", "delete@example.com", "+7-999-123-45-67"
        )
        reader_id = self.db_manager.add_reader(reader)

        # Удаляем читателя
        self.db_manager.delete_reader(reader_id)

        # Проверяем, что читатель удален
        deleted_reader = self.db_manager.get_reader_by_id(reader_id)
        assert deleted_reader is None

    def test_add_loan(self):
        """Тест добавления выдачи в базу данных"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 1)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)
        loan = Loan(book_id, reader_id, loan_date, return_date)

        loan_id = self.db_manager.add_loan(loan)
        assert loan_id is not None
        assert isinstance(loan_id, int)

        # Проверяем, что выдача сохранена в базе
        saved_loan = self.db_manager.get_loan_by_id(loan_id)
        assert saved_loan is not None
        assert saved_loan.book_id == book_id
        assert saved_loan.reader_id == reader_id

    def test_get_loan_by_id(self):
        """Тест получения выдачи по ID"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 1)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)
        loan = Loan(book_id, reader_id, loan_date, return_date)

        loan_id = self.db_manager.add_loan(loan)

        retrieved_loan = self.db_manager.get_loan_by_id(loan_id)
        assert retrieved_loan is not None
        assert retrieved_loan.book_id == book_id
        assert retrieved_loan.reader_id == reader_id
        assert retrieved_loan.id == loan_id

    def test_get_all_loans(self):
        """Тест получения всех выдач"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 2)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        # Создаем несколько выдач
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan1 = Loan(book_id, reader_id, loan_date, return_date)
        loan2 = Loan(book_id, reader_id, loan_date, return_date)

        self.db_manager.add_loan(loan1)
        self.db_manager.add_loan(loan2)

        loans = self.db_manager.get_all_loans()
        assert len(loans) >= 2

        # Проверяем, что все выдачи имеют ID
        for loan in loans:
            assert loan.id is not None

    def test_update_loan(self):
        """Тест обновления выдачи"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 1)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)
        loan = Loan(book_id, reader_id, loan_date, return_date)

        loan_id = self.db_manager.add_loan(loan)

        # Обновляем выдачу
        self.db_manager.update_loan(loan_id, is_returned=True)

        # Проверяем изменения
        updated_loan = self.db_manager.get_loan_by_id(loan_id)
        assert updated_loan.is_returned == True

    def test_get_reader_loans(self):
        """Тест получения выдачи конкретного читателя"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 2)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        # Создаем выдачи для одного читателя
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan1 = Loan(book_id, reader_id, loan_date, return_date)
        loan2 = Loan(book_id, reader_id, loan_date, return_date)

        self.db_manager.add_loan(loan1)
        self.db_manager.add_loan(loan2)

        reader_loans = self.db_manager.get_reader_loans(reader_id)
        assert len(reader_loans) >= 2

        for loan in reader_loans:
            assert loan.reader_id == reader_id

    def test_get_overdue_loans(self):
        """Тест получения просроченных выдач"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 1)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        # Создаем просроченную выдачу
        loan_date = datetime.now() - timedelta(days=20)
        return_date = loan_date + timedelta(days=14)
        loan = Loan(book_id, reader_id, loan_date, return_date)

        self.db_manager.add_loan(loan)

        overdue_loans = self.db_manager.get_overdue_loans()
        assert len(overdue_loans) >= 1

        for loan in overdue_loans:
            assert loan.is_overdue() == True

    def test_data_integrity(self):
        """Тест целостности данных"""
        # Создаем книгу и читателя
        book = Book("Книга", "Автор", "123-456", 2020, 1)
        reader = Reader("Читатель", "reader@example.com", "+7-999-123-45-67")

        book_id = self.db_manager.add_book(book)
        reader_id = self.db_manager.add_reader(reader)

        # Создаем выдачу
        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)
        loan = Loan(book_id, reader_id, loan_date, return_date)

        loan_id = self.db_manager.add_loan(loan)

        # Проверяем связь между таблицами
        retrieved_loan = self.db_manager.get_loan_by_id(loan_id)
        retrieved_book = self.db_manager.get_book_by_id(retrieved_loan.book_id)
        retrieved_reader = self.db_manager.get_reader_by_id(retrieved_loan.reader_id)

        assert retrieved_book is not None
        assert retrieved_reader is not None
        assert retrieved_book.id == book_id
        assert retrieved_reader.id == reader_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
