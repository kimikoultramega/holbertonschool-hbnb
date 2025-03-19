import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):

        # Genera un identificador único (UUID) y lo convierte a cadena.
        # Esto garantiza que cada instancia tenga un id único, incluso en sistemas distribuidos.
        self.id = str(uuid.uuid4())

        # Registra el momento en que se crea el objeto.
        self.created_at = datetime.now()
        # Inicializa el atributo updated_at, que se actualizará cada vez que modifiquemos el objeto.
        self.updated_at = datetime.now()

    def save(self):
        """Actualiza el timestamp de modificación, reflejando que el objeto se ha modificado."""

        self.updated_at = datetime.now()

    def update(self, data):
        """
        Recibe un diccionario 'data' con nuevos valores para actualizar atributos.
        Solo se actualizan los atributos que ya existen en el objeto.
        Luego se llama a save() para actualizar el timestamp.
        """
        for key, value in data.items():
            # Comprueba si el objeto tiene un atributo con el nombre 'key'
            if hasattr(self, key):
                # Actualiza el valor del atributo
                setattr(self, key, value)
                # Actualiza la fecha de modificación
        self.save()
