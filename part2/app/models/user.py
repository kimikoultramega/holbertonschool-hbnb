import re
from app.models.base_model import BaseModel
from app.extensions import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
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

        if password:
            self.hash_password(password)
        
        else:
            self.password = None
    
    def hash_password(self, password):
        """
        Hash la contraseña usando bcrypt y almacena el resultado en el atributo password.
        """
        # generate_password_hash() genera un hash a partir del password
        # .decode('utf-8') convierte el hash a una cadena

        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        """
        Verifica si el password proporcionado coincide con el hash almacenado.
        """
        return bcrypt.check_password_hash(self.password, password)
        

    def __str__(self):
        return f"User({self.first_name} {self.last_name}, {self.email})"