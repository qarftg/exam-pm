import pytest
import sys
import os
from datetime import datetime, timedelta
import tempfile
from database.database_manager import DatabaseManager

# Добавляем путь к модулям проекта
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from controllers.book_controller import BookController
from controllers.reader_controller import ReaderController
from controllers.loan_controller import LoanController


class TestBookController:
    """Тесты для BookController"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.controller = BookController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()

    def test_add_book(self):
        """Тест добавления книги"""
        book_id = self.controller.add_book(
            "Война и мир", "Лев Толстой", "978-5-389-12345-6", 1869, 5
        )

        assert book_id is not None
        assert isinstance(book_id, int)

        # Проверяем, что книга действительно добавлена
        book = self.controller.get_book(book_id)
        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"

    def test_get_book(self):
        """Тест получения книги по ID"""
        book_id = self.controller.add_book(
            "Преступление и наказание",
            "Федор Достоевский",
            "978-5-389-12346-7",
            1866,
            3,
        )

        book = self.controller.get_book(book_id)
        assert book is not None
        assert book.title == "Преступление и наказание"

    def test_get_all_books(self):
        """Тест получения всех книг"""
        # Добавляем несколько книг
        self.controller.add_book("Книга 1", "Автор 1", "123-1", 2020, 1)
        self.controller.add_book("Книга 2", "Автор 2", "123-2", 2021, 2)

        books = self.controller.get_all_books()
        assert len(books) >= 2

        # Проверяем, что все книги имеют необходимые атрибуты
        for book in books:
            assert hasattr(book, "id")
            assert hasattr(book, "title")
            assert hasattr(book, "author")

    def test_update_book(self):
        """Тест обновления книги"""
        book_id = self.controller.add_book(
            "Старое название", "Старый автор", "123-456", 2020, 1
        )

        # Обновляем книгу
        self.controller.update_book(
            book_id, title="Новое название", author="Новый автор"
        )

        # Проверяем изменения
        book = self.controller.get_book(book_id)
        assert book.title == "Новое название"
        assert book.author == "Новый автор"

    def test_delete_book(self):
        """Тест удаления книги"""
        book_id = self.controller.add_book(
            "Книга для удаления", "Автор", "123-789", 2020, 1
        )

        # Удаляем книгу
        self.controller.delete_book(book_id)

        # Проверяем, что книга удалена
        book = self.controller.get_book(book_id)
        assert book is None

    def test_search_books(self):
        """Тест поиска книг"""
        self.controller.add_book("Война и мир", "Лев Толстой", "123-1", 1869, 1)
        self.controller.add_book("Мир и война", "Другой автор", "123-2", 2020, 1)

        # Поиск по названию
        results = self.controller.search_books("война")
        assert len(results) >= 1

        # Поиск по автору
        results = self.controller.search_books("Толстой")
        assert len(results) >= 1

    def test_borrow_book(self):
        """Тест выдачи книги"""
        book_id = self.controller.add_book("Книга", "Автор", "123-456", 2020, 3)

        # Выдаем книгу
        success = self.controller.borrow_book(book_id)
        assert success == True

        # Проверяем, что количество доступных уменьшилось
        book = self.controller.get_book(book_id)
        assert book.available == 2

    def test_return_book(self):
        """Тест возврата книги"""
        book_id = self.controller.add_book("Книга", "Автор", "123-456", 2020, 3)

        # Выдаем книгу
        self.controller.borrow_book(book_id)

        # Возвращаем книгу
        success = self.controller.return_book(book_id)
        assert success == True

        # Проверяем, что количество доступных увеличилось
        book = self.controller.get_book(book_id)
        assert book.available == 3


class TestReaderController:
    """Тесты для ReaderController"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.controller = ReaderController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()

    def test_add_reader(self):
        """Тест добавления читателя"""
        reader_id = self.controller.add_reader(
            "Иван Иванов", "ivan@example.com", "+7-999-123-45-67"
        )

        assert reader_id is not None
        assert isinstance(reader_id, int)

        # Проверяем, что читатель действительно добавлен
        reader = self.controller.get_reader(reader_id)
        assert reader.name == "Иван Иванов"
        assert reader.email == "ivan@example.com"

    def test_get_reader(self):
        """Тест получения читателя по ID"""
        reader_id = self.controller.add_reader(
            "Петр Петров", "petr@example.com", "+7-999-123-45-68"
        )

        reader = self.controller.get_reader(reader_id)
        assert reader is not None
        assert reader.name == "Петр Петров"

    def test_get_all_readers(self):
        """Тест получения всех читателей"""
        # Добавляем несколько читателей
        self.controller.add_reader(
            "Читатель 1", "reader1@example.com", "+7-999-111-11-11"
        )
        self.controller.add_reader(
            "Читатель 2", "reader2@example.com", "+7-999-222-22-22"
        )

        readers = self.controller.get_all_readers()
        assert len(readers) >= 2

        # Проверяем, что все читатели имеют необходимые атрибуты
        for reader in readers:
            assert hasattr(reader, "id")
            assert hasattr(reader, "name")
            assert hasattr(reader, "email")

    def test_update_reader(self):
        """Тест обновления читателя"""
        reader_id = self.controller.add_reader(
            "Старое имя", "old@example.com", "+7-999-123-45-67"
        )

        # Обновляем читателя
        self.controller.update_reader(
            reader_id, name="Новое имя", email="new@example.com"
        )

        # Проверяем изменения
        reader = self.controller.get_reader(reader_id)
        assert reader.name == "Новое имя"
        assert reader.email == "new@example.com"

    def test_delete_reader(self):
        """Тест удаления читателя"""
        reader_id = self.controller.add_reader(
            "Читатель для удаления", "delete@example.com", "+7-999-123-45-67"
        )

        # Удаляем читателя
        self.controller.delete_reader(reader_id)

        # Проверяем, что читатель удален
        reader = self.controller.get_reader(reader_id)
        assert reader is None

    def test_get_reader_loans(self):
        """Тест получения выдачи читателя"""
        reader_id = self.controller.add_reader(
            "Тестовый читатель", "test@example.com", "+7-999-123-45-67"
        )

        loans = self.controller.get_reader_loans(reader_id)
        assert isinstance(loans, list)


class TestLoanController:
    """Тесты для LoanController"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_manager = DatabaseManager(self.temp_db.name)
        self.book_controller = BookController(self.db_manager)
        self.reader_controller = ReaderController(self.db_manager)
        self.controller = LoanController(self.db_manager)

    def teardown_method(self):
        self.db_manager.close()

    def test_create_loan(self):
        """Тест создания выдачи"""
        # Создаем книгу и читателя
        book_id = self.book_controller.add_book("Книга", "Автор", "123-456", 2020, 1)
        reader_id = self.reader_controller.add_reader(
            "Читатель", "reader@example.com", "+7-999-123-45-67"
        )

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan_id = self.controller.create_loan(
            book_id, reader_id, loan_date, return_date
        )

        assert loan_id is not None
        assert isinstance(loan_id, int)

        # Проверяем, что выдача создана
        loan = self.controller.get_loan(loan_id)
        assert loan is not None
        assert loan.book_id == book_id
        assert loan.reader_id == reader_id

    def test_get_loan(self):
        """Тест получения выдачи по ID"""
        book_id = self.book_controller.add_book("Книга", "Автор", "123-456", 2020, 1)
        reader_id = self.reader_controller.add_reader(
            "Читатель", "reader@example.com", "+7-999-123-45-67"
        )

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan_id = self.controller.create_loan(
            book_id, reader_id, loan_date, return_date
        )

        loan = self.controller.get_loan(loan_id)
        assert loan is not None
        assert loan.book_id == book_id
        assert loan.reader_id == reader_id

    def test_get_all_loans(self):
        """Тест получения всех выдач"""
        # Создаем несколько выдач
        book_id = self.book_controller.add_book("Книга", "Автор", "123-456", 2020, 2)
        reader_id = self.reader_controller.add_reader(
            "Читатель", "reader@example.com", "+7-999-123-45-67"
        )

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        self.controller.create_loan(book_id, reader_id, loan_date, return_date)
        self.controller.create_loan(book_id, reader_id, loan_date, return_date)

        loans = self.controller.get_all_loans()
        assert len(loans) >= 2

        # Проверяем, что все выдачи имеют необходимые атрибуты
        for loan in loans:
            assert hasattr(loan, "id")
            assert hasattr(loan, "book_id")
            assert hasattr(loan, "reader_id")

    def test_return_book(self):
        """Тест возврата книги"""
        book_id = self.book_controller.add_book("Книга", "Автор", "123-456", 2020, 1)
        reader_id = self.reader_controller.add_reader(
            "Читатель", "reader@example.com", "+7-999-123-45-67"
        )

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        loan_id = self.controller.create_loan(
            book_id, reader_id, loan_date, return_date
        )

        # Возвращаем книгу
        success = self.controller.return_book(loan_id)
        assert success == True

        # Проверяем, что выдача отмечена как возвращенная
        loan = self.controller.get_loan(loan_id)
        assert loan.is_returned == True

    def test_get_overdue_loans(self):
        """Тест получения просроченных выдач"""
        book_id = self.book_controller.add_book("Книга", "Автор", "123-456", 2020, 1)
        reader_id = self.reader_controller.add_reader(
            "Читатель", "reader@example.com", "+7-999-123-45-67"
        )

        # Создаем просроченную выдачу
        loan_date = datetime.now() - timedelta(days=20)
        return_date = loan_date + timedelta(days=14)

        self.controller.create_loan(book_id, reader_id, loan_date, return_date)

        overdue_loans = self.controller.get_overdue_loans()
        assert len(overdue_loans) >= 1

        for loan in overdue_loans:
            assert loan.is_overdue() == True

    def test_get_reader_loans(self):
        """Тест получения выдачи конкретного читателя"""
        book_id = self.book_controller.add_book("Книга", "Автор", "123-456", 2020, 2)
        reader_id = self.reader_controller.add_reader(
            "Читатель", "reader@example.com", "+7-999-123-45-67"
        )

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=14)

        # Создаем выдачи для одного читателя
        self.controller.create_loan(book_id, reader_id, loan_date, return_date)
        self.controller.create_loan(book_id, reader_id, loan_date, return_date)

        reader_loans = self.controller.get_reader_loans(reader_id)
        assert len(reader_loans) >= 2

        for loan in reader_loans:
            assert loan.reader_id == reader_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
