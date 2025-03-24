import unittest
import json
from app import create_app

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_create_amenity_success(self):
        payload = {"name": "Wi-Fi"}
        response = self.client.post('/api/v1/amenities/', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], payload['name'])
    
    def test_create_amenity_invalid(self):
        # Prueba con un nombre vacío.
        payload = {"name": ""}
        response = self.client.post('/api/v1/amenities/',
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
