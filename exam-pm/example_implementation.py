#!/usr/bin/env python3
"""
Пример реализации для демонстрации структуры проекта
Этот файл показывает, как должны быть реализованы классы согласно заданию
"""


class Book:
    """Модель книги - пример реализации"""

    def __init__(self, title, author, isbn, year, quantity):
        """
        Инициализация книги

        Args:
            title (str): Название книги
            author (str): Автор книги
            isbn (str): ISBN номер
            year (int): Год издания
            quantity (int): Количество экземпляров
        """
        # Валидация данных
        if not title or not title.strip():
            raise ValueError("Название книги не может быть пустым")
        # тут должны быть ещё валидации как минимум 3 шт

        self.id = None  # Будет установлен при сохранении в БД
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()
        self.year = year
        self.quantity = quantity
        self.available = quantity  # Изначально все экземпляры доступны

    def borrow_book(self):
        """Выдать книгу"""
        if self.available > 0:
            self.available -= 1
            return True
        return False

    def return_book(self):
        """Вернуть книгу"""
        if self.available < self.quantity:
            self.available += 1
            return True
        return False

    def is_available(self):
        """Проверить доступность книги"""
        return self.available > 0

    def to_dict(self):
        """Преобразовать в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "quantity": self.quantity,
            "available": self.available,
        }


# Пример использования
if __name__ == "__main__":
    print("Пример использования моделей:")

    # Создание книги
    try:
        book = Book("Война и мир", "Лев Толстой", "978-5-389-12345-6", 1869, 5)
        print(f"Создана книга: {book.title} - {book.author}")
        print(f"Доступно экземпляров: {book.available}")

        # Выдача книги
        if book.borrow_book():
            print(f"Книга выдана. Осталось: {book.available}")

        # Возврат книги
        if book.return_book():
            print(f"Книга возвращена. Доступно: {book.available}")

    except ValueError as e:
        print(f"Ошибка валидации: {e}")
