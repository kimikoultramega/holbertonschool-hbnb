import uuid
import unittest
import json
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
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
        
        # print("Respuesta de creación de usuario:", user_response.data.decode())
        self.assertEqual(user_response.status_code, 201)
        self.owner_data = json.loads(user_response.data)
    
    def test_create_place_success(self):
        payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_data['id'],
            "amenities": []
        }
        response = self.client.post('/api/v1/places/', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], payload['title'])
    
    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
    
    def test_update_place_success(self):
        # Primero crear un place
        create_payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_data['id'],
            "amenities": []
        }
        create_response = self.client.post('/api/v1/places/', 
                                           data=json.dumps(create_payload),
                                           content_type='application/json')
        self.assertEqual(create_response.status_code, 201)
        place_data = json.loads(create_response.data)
        
        # Actualizar el place
        update_payload = {
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_data['id'],
            "amenities": []
        }
        update_response = self.client.put(f'/api/v1/places/{place_data["id"]}',
                                          data=json.dumps(update_payload),
                                          content_type='application/json')
        self.assertEqual(update_response.status_code, 200)
        updated_data = json.loads(update_response.data)
        self.assertEqual(updated_data['title'], update_payload['title'])

if __name__ == '__main__':
    unittest.main()