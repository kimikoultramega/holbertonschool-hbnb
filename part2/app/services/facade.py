#!/usr/bin/python3

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_review(self, review_data):
        """
        Crea una nueva review a partir del diccionario review_data.
        """
        # Verificamos que el usuario exista:
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")
        
        # Verificamos que el place exista:
        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )

        # Se añade la review al repositorio:
        self.review_repo.add(review)

        place.add_review(review)
        return review
    
    def get_review(self, review_id):
        """Recupera una review por su ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Recupera todas las reviews almacenadas.
        """
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """
        Recupera todas las reviews asociadas a un place específico.
        Se filtran las reviews cuyo place.id coincida con place_id.
        """
        reviews = self.review_repo.get_all()
        filtered = [r for r in reviews if r.place.id == place_id]
        return filtered
    
    def update_review(self, review_id, review_data):
        """
        Actualiza una review existente usando los nuevos datos del diccionario review_data.
        Retorna la review actualizada o None si no se encuentra.
        """

        review = self.review_repo.get(review_id)

        if not review:
            return None
        review.update(review_data)
        return review
    
    def delete_review(self, review_id):
        """
        Elimina una review del repositorio.
        Retorna True si la eliminación es exitosa o None si no se encuentra la review.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return True

    def create_place(self, place_data):
        """
        Crea un nuevo Place a partir del diccionario place_data.
        Se espera que place_data incluya:
          - title, description, price, latitude, longitude, owner_id, amenities (lista de IDs).
        """

        owner = self.user_repo.get(place_data['owner_id'])

        if not owner:
            raise ValueError("Owner not found")
        
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        amenity_ids = place_data.get('amenities', [])
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)
        self.place_repo.add(place)
        return place
    
    def get_place(self, place_id):
        """
        Recupera un Place por su ID.
        """
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        """
        Recupera todos los places.
        """
        return self.place_repo.get_all()
    
    def update_place(self, place_id, place_data):
        """
        Actualiza un Place existente usando los nuevos datos proporcionados.
        Se pueden actualizar atributos como title, description, price, latitude, longitude.
        """
        place = self.place_repo.get(place_id)
        
        if not place:
            return None
        
        place.update(place_data)

        return place

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
