#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_amenity(self, amenity_data):
        """
        Crea una nueva amenidad a partir del diccionario amenity_data.
        Se espera que amenity_data contenga al menos la clave 'name'.
        """

        # Desempaquetamos el diccionario para pasar los valores al cosntructor de Amenity.
        amenity = Amenity(**amenity_data)

        # Agregamos la nueva amenity
        self.amenity_repo.add(amenity)

        # Retornamos la instancia para utilizar los datos
        return amenity
    
    def get_amenity(self, amenity_id):
        """
        Recupera una amenity por su ID
        """

        return self.amenity_repo.get(amenity_id)
    
    def get_all_amenities(self):
        """
        Recupera todas las amenidades almacenadas.
        """
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        """
        Actualiza una amenidad existente
        """

        # Primero buscamos la amenity por su ID
        amenity = self.amenity_repo.get(amenity_id)

        # Si no existe, retornamos None
        if not amenity:
            return None
        
        # Si existe, actualizamos los atributos
        amenity.update(amenity_data)

        return amenity

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
