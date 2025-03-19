import re
from app.models.base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        # Validación básica de longitud
        if len(first_name) > 50:
            raise ValueError("El nombre no puede tener más de 50 caracteres")
        if len(last_name) > 50:
            raise ValueError("El apellido no puede tener más de 50 caracteres")
        # Validación simple de email utilizando re
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("El email no tiene un formato válido")
        
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
    def __str__(self):
        return f"User({self.first_name} {self.last_name}, {self.email})"