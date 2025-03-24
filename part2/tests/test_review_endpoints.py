import uuid
import unittest
import json
from app import create_app

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        unique_email = f"owner.test+{uuid.uuid4()}@example.com"
        # Creamos un usuario para usar como owner
        user_payload = {
            "first_name": "Owner",
            "last_name": "Test",
            "email": unique_email
        }
        user_response = self.client.post('/api/v1/users/', 
                                         data=json.dumps(user_payload),
                                         content_type='application/json')
        self.assertEqual(user_response.status_code, 201)
        self.user_data = json.loads(user_response.data)
        
        # Crear un place para asociar con la review
        place_payload = {
            "title": "Test Place",
            "description": "For review testing",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_data['id'],
            "amenities": []
        }
        place_response = self.client.post('/api/v1/places/',
                                          data=json.dumps(place_payload),
                                          content_type='application/json')
        self.assertEqual(place_response.status_code, 201)
        self.place_data = json.loads(place_response.data)
    
    def test_create_review_success(self):
        review_payload = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_data['id'],
            "place_id": self.place_data['id']
        }
        response = self.client.post('/api/v1/reviews/',
                                    data=json.dumps(review_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], review_payload['text'])
    
    def test_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_update_review_success(self):
        # Crear una review
        review_payload = {
            "text": "Initial review",
            "rating": 4,
            "user_id": self.user_data['id'],
            "place_id": self.place_data['id']
        }
        post_response = self.client.post('/api/v1/reviews/',
                                         data=json.dumps(review_payload),
                                         content_type='application/json')
        self.assertEqual(post_response.status_code, 201)
        review_data = json.loads(post_response.data)
        
        # Actualizar la review
        update_payload = {
            "text": "Updated review",
            "rating": 3,
            "user_id": self.user_data['id'],
            "place_id": self.place_data['id']
        }
        put_response = self.client.put(f'/api/v1/reviews/{review_data["id"]}',
                                       data=json.dumps(update_payload),
                                       content_type='application/json')
        self.assertEqual(put_response.status_code, 200)
        updated_data = json.loads(put_response.data)
        self.assertEqual(updated_data['text'], update_payload['text'])
    
    def test_delete_review_success(self):
        # Crear una review para eliminarla
        review_payload = {
            "text": "Review to delete",
            "rating": 2,
            "user_id": self.user_data['id'],
            "place_id": self.place_data['id']
        }
        post_response = self.client.post('/api/v1/reviews/',
                                         data=json.dumps(review_payload),
                                         content_type='application/json')
        self.assertEqual(post_response.status_code, 201)
        review_data = json.loads(post_response.data)
        
        # Eliminar la review
        delete_response = self.client.delete(f'/api/v1/reviews/{review_data["id"]}')
        self.assertEqual(delete_response.status_code, 200)
        delete_data = json.loads(delete_response.data)
        self.assertEqual(delete_data['message'], "Review deleted successfully")
        
        # Verificar que ya no existe
        get_response = self.client.get(f'/api/v1/reviews/{review_data["id"]}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()