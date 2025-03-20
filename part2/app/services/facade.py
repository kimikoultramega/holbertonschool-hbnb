#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Método placeholder para crear un usuario
    def create_user(self, user_data):
        """
        Crea un usuario a partir del diccionario user_data.
        Se espera que user_data tenga las claves 'first_name', 'last_name' y 'email'.
        """
        # Utilizamos el operador ** para desempaquetar el diccionario y pasar sus valores
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_user(self, user_id):
        """
        Recupera un usuario por su id.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Busca un usuario por su email.
        """
        return self.user_repo.get_by_attribute('email', email)
    
    
    # Método placeholder para obtener un lugar (Place) por su ID
    def get_place(self, place_id):
        # La lógica se implementará en tareas posteriores
        pass
