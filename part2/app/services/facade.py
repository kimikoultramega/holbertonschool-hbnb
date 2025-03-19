#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Método placeholder para crear un usuario
    def create_user(self, user_data):
        # La lógica se implementará en tareas posteriores
        pass

    # Método placeholder para obtener un lugar (Place) por su ID
    def get_place(self, place_id):
        # La lógica se implementará en tareas posteriores
        pass
