from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def test_place_creation_and_relationship():
    # Crear un usuario que será el propietario del Place.
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com")
    
    # Crear una instancia de Place con datos válidos.
    place = Place(title="Cozy Apartment", description="A nice place to stay", 
                  price=100.0, latitude=37.7749, longitude=-122.4194, owner=owner)
    
    # Verificar que el Place se creó con el título y precio correctos.
    assert place.title == "Cozy Apartment", "El título debería ser 'Cozy Apartment'."
    assert place.price == 100.0, "El precio debería ser 100.0."
    
    # Crear una reseña para el Place y agregarla.
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)
    
    # Verificar que la reseña se agregó correctamente.
    assert len(place.reviews) == 1, "Debería haber 1 reseña."
    assert place.reviews[0].text == "Great stay!", "El texto de la reseña debería ser 'Great stay!'."
    
    print("Test de creación de Place y relaciones: PASADO")

if __name__ == '__main__':
    test_place_creation_and_relationship()
