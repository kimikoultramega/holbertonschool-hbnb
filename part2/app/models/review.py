from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        
        # Validación: el texto debe de estar si o si.

        if not text:
            raise ValueError("El texto de la reseña es obligatiorio.")
        
        # Validación: la calificación entre 1 y 5.
        
        if not (1 <= rating <= 5):
            raise ValueError("La calificación debe de estar entre 1 y 5.")
        
        self.text = text
        self.rating = rating
        self.place = place # Se espera que sea una instancia de Place.
        self.user = user # Se espera que sea una instancia de User.

    def __str__(self):
        # Muestra una vista resumida de la reseña para facilitar la depuración.
        return f"Review({self.rating} - {self.text[:20]}...)"
    