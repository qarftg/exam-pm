from models.reader import Reader

class ReaderController:
    def __init__(self, db_manager) -> None:
        self.db = db_manager

    def add_reader(self, name, email, phone) -> int:
        reader = Reader(name, email, phone)
        return self.db.add_reader(reader)

    def get_reader(self, reader_id) -> Reader | None:
        return self.db.get_reader_by_id(reader_id)

    def get_all_readers(self) -> list[Reader]:
        return self.db.get_all_readers()

    def update_reader(self, reader_id, **kwargs) -> bool:
        return self.db.update_reader(reader_id, **kwargs)

    def delete_reader(self, reader_id) -> bool:
        return self.db.delete_reader(reader_id)

    def get_reader_loans(self, reader_id) -> list:
        return self.db.get_reader_loans(reader_id)

