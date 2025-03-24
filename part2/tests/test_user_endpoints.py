import unittest
import json
from app import create_app

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_success(self):

        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }

        response = self.client.post('/api/v1/users/', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], payload['first_name'])
    
    def test_create_user_invalid(self):
        
        payload = {
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        }
        
        response = self.client.post('/api/v1/users/', 
                                    data=json.dumps(payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_user_not_found(self):
        
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()