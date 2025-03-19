from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        # Validación: El nombre debe existir y no superar 50 caracteres.

        if not name:
            raise ValueError("El nombre de la amenidad es obligatiorio.")
        if len(name) > 50:
            raise ValueError("El nombre de la amenidad no puede tener más de 50 caracteres.")
        
        self.name = name
    
    def __str__(self):
        return f"Amenity({self.name})"
