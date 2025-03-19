from app.models.base_model import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        # Válidación de título y precio
        if len(title) > 100:
            raise ValueError("El título no puede tener más de 100 caracteres.")
        if price <= 0:
            raise ValueError("El precio debe de ser un valor positivo")
        # Validación de coordenadas
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitud debe de estar entre -90.0 y 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitud debe de estar entre -180.0 y 180.0")
        
        self.title = title 
        self.description = description 
        self.price = price
        self.latitude = latitude 
        self.longitude = longitude 
        self.owner = owner

        # Inicializamos relaciones: reseñas y amenidades
        self.reviews = []
        self.amenities = []
        
    def add_review(self, review):
        """Agrega una reseña a la lista de reseñas."""
        self.reviews.append(review)
    
    def add_amenity(self, amenity):
        """Agrega una amenidad a la lista de amenidades."""
        self.amenities.append(amenity)

    def __str__(self):
        return f"Place({self.title}, {self.price})"
