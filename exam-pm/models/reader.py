from datetime import datetime
import re

class Reader:
    def __init__(self, name, email, phone) -> None:
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")
        if not phone or not phone.strip():
            raise ValueError("Phone cannot be empty")
            
        self.id = None
        self.name = name.strip()
        self.email = email.strip()
        self.phone = phone.strip()
        self.registration_date = datetime.now()

    def _is_valid_email(self, email) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def update_info(self, name=None, email=None, phone=None) -> None:
        if name is not None:
            if not name.strip():
                raise ValueError("Name cannot be empty")
            self.name = name.strip()
        if email is not None:
            if not self._is_valid_email(email):
                raise ValueError("Invalid email format")
            self.email = email.strip()
        if phone is not None:
            if not phone.strip():
                raise ValueError("Phone cannot be empty")
            self.phone = phone.strip()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "registration_date": self.registration_date.strftime("%Y-%m-%d %H:%M:%S")
        }