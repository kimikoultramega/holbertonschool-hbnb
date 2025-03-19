from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def test_review_creation():
    # Crear instancias de User y Place para relacionarlas con la reseña.
    owner = User(first_name="Bob", last_name="Brown", email="bob.brown@example.com")
    place = Place(title="Modern Loft", description="Spacious and modern", 
                  price=150.0, latitude=40.7128, longitude=-74.0060, owner=owner)
    
    # Crear una reseña con datos válidos.
    review = Review(text="Amazing experience!", rating=5, place=place, user=owner)
    
    # Verificar que la reseña tenga los datos correctos.
    assert review.text == "Amazing experience!", "El texto debería ser 'Amazing experience!'."
    assert review.rating == 5, "La calificación debería ser 5."
    assert review.place == place, "La reseña debe estar asociada al Place creado."
    assert review.user == owner, "La reseña debe estar asociada al User creado."
    
    print("Test de creación de Review: PASADO")

if __name__ == '__main__':
    test_review_creation()
