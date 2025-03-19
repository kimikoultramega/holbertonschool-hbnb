# Importamos la clase User del módulo correspondiente.
from app.models.user import User

def test_user_creation():
    # Creamos una instancia de User con datos de ejemplo.
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    
    # Realizamos aserciones para verificar que la instancia se creó correctamente.
    assert user.first_name == "John", "El nombre debería ser 'John'."
    assert user.last_name == "Doe", "El apellido debería ser 'Doe'."
    assert user.email == "john.doe@example.com", "El email debería ser 'john.doe@example.com'."
    assert user.is_admin is False, "El valor por defecto de is_admin debe ser False."
    
    print("Test de creación de User: PASADO")

# Permite ejecutar el test directamente desde este archivo.
if __name__ == '__main__':
    test_user_creation()
