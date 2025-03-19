from app.models.amenity import Amenity

def test_amenity_creation():
    # Crear una instancia de Amenity.
    amenity = Amenity(name="Wi-Fi")
    
    # Verificar que el nombre se haya asignado correctamente.
    assert amenity.name == "Wi-Fi", "El nombre de la amenidad debería ser 'Wi-Fi'."
    
    print("Test de creación de Amenity: PASADO")

if __name__ == '__main__':
    test_amenity_creation()
