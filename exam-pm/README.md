# Задание для зачета по практике

## Описание проекта

Вам необходимо реализовать **Систему управления библиотекой** с использованием архитектуры MVC, SQL базы данных и автотестов.

## Технологии
- Python 3.8+
- SQLite (встроенная база данных)
- pytest (для автотестов)
- tkinter (для GUI)

## Структура проекта

```
library_system/
├── models/
│   ├── __init__.py
│   ├── book.py
│   ├── reader.py
│   └── loan.py
├── views/
│   ├── __init__.py
│   ├── main_window.py
│   ├── book_view.py
│   ├── reader_view.py
│   └── loan_view.py
├── controllers/
│   ├── __init__.py
│   ├── book_controller.py
│   ├── reader_controller.py
│   └── loan_controller.py
├── database/
│   ├── __init__.py
│   ├── database_manager.py
│   └── library.db
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_database.py
├── main.py
├── requirements.txt
└── README.md
```

## Задание 1: Модели (Models)

### 1.1 Класс Book (models/book.py)
Создайте класс `Book` со следующими атрибутами и методами:

**Атрибуты:**
- `id` (int) - уникальный идентификатор
- `title` (str) - название книги
- `author` (str) - автор
- `isbn` (str) - ISBN номер
- `year` (int) - год издания
- `quantity` (int) - количество экземпляров
- `available` (int) - количество доступных экземпляров

**Методы:**
- `__init__(self, title, author, isbn, year, quantity)`
- `borrow_book(self)` - выдать книгу (уменьшить available)
- `return_book(self)` - вернуть книгу (увеличить available)
- `is_available(self)` - проверить доступность
- `to_dict(self)` - вернуть словарь с данными книги

### 1.2 Класс Reader (models/reader.py)
Создайте класс `Reader` со следующими атрибутами и методами:

**Атрибуты:**
- `id` (int) - уникальный идентификатор
- `name` (str) - имя читателя
- `email` (str) - email
- `phone` (str) - телефон
- `registration_date` (datetime) - дата регистрации

**Методы:**
- `__init__(self, name, email, phone)`
- `update_info(self, name=None, email=None, phone=None)`
- `to_dict(self)` - вернуть словарь с данными читателя

### 1.3 Класс Loan (models/loan.py)
Создайте класс `Loan` со следующими атрибутами и методами:

**Атрибуты:**
- `id` (int) - уникальный идентификатор
- `book_id` (int) - ID книги
- `reader_id` (int) - ID читателя
- `loan_date` (datetime) - дата выдачи
- `return_date` (datetime) - дата возврата
- `is_returned` (bool) - возвращена ли книга

**Методы:**
- `__init__(self, book_id, reader_id, loan_date, return_date)`
- `return_book(self)` - отметить книгу как возвращенную
- `is_overdue(self)` - проверить просрочку
- `to_dict(self)` - вернуть словарь с данными выдачи

## Задание 2: База данных (SQL CRUD операции)

### 2.1 DatabaseManager (database/database_manager.py)
Создайте класс `DatabaseManager` для работы с SQLite базой данных:

**Методы для работы с книгами:**
- `create_book_table(self)` - создать таблицу книг
- `add_book(self, book)` - добавить книгу
- `get_book_by_id(self, book_id)` - получить книгу по ID
- `get_all_books(self)` - получить все книги
- `update_book(self, book_id, **kwargs)` - обновить книгу
- `delete_book(self, book_id)` - удалить книгу
- `search_books(self, query)` - поиск книг по названию/автору

**Методы для работы с читателями:**
- `create_reader_table(self)` - создать таблицу читателей
- `add_reader(self, reader)` - добавить читателя
- `get_reader_by_id(self, reader_id)` - получить читателя по ID
- `get_all_readers(self)` - получить всех читателей
- `update_reader(self, reader_id, **kwargs)` - обновить читателя
- `delete_reader(self, reader_id)` - удалить читателя

**Методы для работы с выдачами:**
- `create_loan_table(self)` - создать таблицу выдач
- `add_loan(self, loan)` - добавить выдачу
- `get_loan_by_id(self, loan_id)` - получить выдачу по ID
- `get_all_loans(self)` - получить все выдачи
- `update_loan(self, loan_id, **kwargs)` - обновить выдачу
- `get_reader_loans(self, reader_id)` - получить выдачи читателя
- `get_overdue_loans(self)` - получить просроченные выдачи

## Задание 3: Контроллеры (Controllers)

### 3.1 BookController (controllers/book_controller.py)
Создайте класс `BookController`:

**Методы:**
- `add_book(self, title, author, isbn, year, quantity)` - добавить книгу
- `get_book(self, book_id)` - получить книгу
- `get_all_books(self)` - получить все книги
- `update_book(self, book_id, **kwargs)` - обновить книгу
- `delete_book(self, book_id)` - удалить книгу
- `search_books(self, query)` - поиск книг
- `borrow_book(self, book_id)` - выдать книгу
- `return_book(self, book_id)` - вернуть книгу

### 3.2 ReaderController (controllers/reader_controller.py)
Создайте класс `ReaderController`:

**Методы:**
- `add_reader(self, name, email, phone)` - добавить читателя
- `get_reader(self, reader_id)` - получить читателя
- `get_all_readers(self)` - получить всех читателей
- `update_reader(self, reader_id, **kwargs)` - обновить читателя
- `delete_reader(self, reader_id)` - удалить читателя
- `get_reader_loans(self, reader_id)` - получить выдачи читателя

### 3.3 LoanController (controllers/loan_controller.py)
Создайте класс `LoanController`:

**Методы:**
- `create_loan(self, book_id, reader_id, loan_date, return_date)` - создать выдачу
- `get_loan(self, loan_id)` - получить выдачу
- `get_all_loans(self)` - получить все выдачи
- `return_book(self, loan_id)` - вернуть книгу
- `get_overdue_loans(self)` - получить просроченные выдачи
- `get_reader_loans(self, reader_id)` - получить выдачи читателя

## Задание 4: Представления (Views) - GUI

### 4.1 MainWindow (views/main_window.py)
Создайте главное окно приложения с меню и вкладками для:
- Управления книгами
- Управления читателями
- Управления выдачами

### 4.2 BookView (views/book_view.py)
Создайте интерфейс для управления книгами:
- Форма добавления/редактирования книги
- Таблица со списком книг
- Поиск по книгам
- Кнопки для выдачи/возврата

### 4.3 ReaderView (views/reader_view.py)
Создайте интерфейс для управления читателями:
- Форма добавления/редактирования читателя
- Таблица со списком читателей
- Просмотр выдачи читателя

### 4.4 LoanView (views/loan_view.py)
Создайте интерфейс для управления выдачами:
- Форма создания выдачи
- Таблица со списком выдач
- Фильтрация по статусу (активные/просроченные)

## Задание 5: Автотесты

### 5.1 Тесты моделей (tests/test_models.py)
Напишите тесты для всех классов моделей:
- Тестирование создания объектов
- Тестирование методов классов
- Тестирование валидации данных
- Тестирование граничных случаев

### 5.2 Тесты контроллеров (tests/test_controllers.py)
Напишите тесты для всех контроллеров:
- Тестирование CRUD операций
- Тестирование бизнес-логики
- Тестирование обработки ошибок

### 5.3 Тесты базы данных (tests/test_database.py)
Напишите тесты для работы с базой данных:
- Тестирование создания таблиц
- Тестирование SQL операций
- Тестирование целостности данных

## Важно для тестирования и архитектуры

- Все контроллеры (`BookController`, `ReaderController`, `LoanController`) должны принимать объект `DatabaseManager` в качестве обязательного аргумента конструктора.
- Для тестирования используйте временную базу данных (например, через `tempfile.NamedTemporaryFile` или SQLite `:memory:`).
- После каждого теста обязательно закрывайте соединение с базой (`db_manager.close()`) и удаляйте временный файл (если не `:memory:`).
- Пример инициализации для теста:
    ```python
    import tempfile
    import os
    from database.database_manager import DatabaseManager
    from controllers.book_controller import BookController

    class TestBookController:
        def setup_method(self):
            self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            self.db_manager = DatabaseManager(self.temp_db.name)
            self.controller = BookController(self.db_manager)

        def teardown_method(self):
            self.db_manager.close()
            os.unlink(self.temp_db.name)
    ```
- Для ускорения тестов можно использовать `DatabaseManager(':memory:')`, но тогда данные не сохраняются между тестами.

## Требования к реализации

1. **Архитектура MVC**: Строгое разделение на Model, View, Controller
2. **SQL операции**: Использование SQLite с правильными SQL запросами
3. **Обработка ошибок**: Корректная обработка исключений
4. **Валидация данных**: Проверка входных данных
5. **Документация**: Комментарии к коду и docstrings
6. **Автотесты**: Покрытие тестами не менее 80% кода

## Запуск проекта

1. Установите зависимости:

Если через pip: 

```bash
pip install -r requirements.txt
```
Если через poetry
```bash
pip install poetry # если не установлен
poetry install --no-root
```

2. Запустите приложение:
```bash
python main.py
```

или

```bash
poetry run python main.py
```

## Шаги для запуска и тестирования проекта

### 1 шаг: Тестирование моделей

Запустите тесты для моделей (Book, Reader, Loan):

```bash
poetry run pytest -v tests/test_models.py
```

### 2 шаг: Тестирование базы данных

Запустите тесты для работы с базой данных (DatabaseManager):

```bash
poetry run pytest -v tests/test_database.py
```

### 3 шаг: Тестирование контроллеров

Запустите тесты для контроллеров (BookController, ReaderController, LoanController):

```bash
poetry run pytest -v tests/test_controllers.py
```

---

## Критерии оценки

- **MVC архитектура** (30%): Правильное разделение ответственности
- **SQL операции** (30%): Корректная работа с базой данных
- **Работа с ORM** (30%): Функциональный и удобный интерфейс
- **Код** (10%): Чистота кода


ВАЖНО: УКАЗАННАЯ НАЧАЛЬНАЯ СТРУКТУРА (КЛАССЫ, ФУНКЦИИ, ИХ МЕТОДЫ И АРГУМЕНТЫ) ДОЛЖНЫ БЫТЬ НЕИЗМЕННЫ, ВЫ ДОПИСЫВАЕТЕ ТОЛЬКО ТЕЛО МЕТОДОВ И КЛАССОВ 