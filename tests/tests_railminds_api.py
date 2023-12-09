# tests/test_railminds_api.py

import unittest
from flask import Flask
from flask_restful import Api
from flask_testing import TestCase
from app.routes import TrainListResource, TrainSpeedResource, TrainDirectionResource, AccessoryListResource, AccessoryActivateResource, AccessoryDeactivateResource

class RailMindsAPITestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        api = Api(app)

        # Disable Flask error catching during tests
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

        # Add resources for testing
        api.add_resource(TrainListResource, '/trains')
        api.add_resource(TrainSpeedResource, '/trains/<int:train_id>/speed')
        api.add_resource(TrainDirectionResource, '/trains/<int:train_id>/direction')
        api.add_resource(AccessoryListResource, '/accessories')
        api.add_resource(AccessoryActivateResource, '/accessories/<int:accessory_id>/activate')
        api.add_resource(AccessoryDeactivateResource, '/accessories/<int:accessory_id>/deactivate')

        return app

    def test_get_trains(self):
        response = self.client.get('/trains')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('trains', data)

    def test_get_trains_empty_list(self):
        # Test when there are no trains
        app = self.create_app()
        app.config['trains'] = []  # Override sample data
        response = self.client.get('/trains')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('trains', data)
        self.assertEqual(data['trains'], [])

    def test_update_train_speed(self):
        response = self.client.put('/trains/1/speed', json={'speed': 50})
        self.assertEqual(response.status_code, 204)

    def test_update_train_speed_invalid_speed(self):
        # Test when updating train speed with an invalid value
        response = self.client.put('/trains/1/speed', json={'speed': 120})
        self.assertEqual(response.status_code, 400)

    def test_update_train_speed_negative_speed(self):
        # Test when updating train speed with a negative value
        response = self.client.put('/trains/1/speed', json={'speed': -50})
        self.assertEqual(response.status_code, 400)

    def test_update_train_direction(self):
        response = self.client.put('/trains/1/direction', json={'direction': 'reverse'})
        self.assertEqual(response.status_code, 204)

    def test_update_train_direction_invalid_direction(self):
        # Test when updating train direction with an invalid value
        response = self.client.put('/trains/1/direction', json={'direction': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_get_accessories(self):
        response = self.client.get('/accessories')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('accessories', data)

    def test_activate_accessory(self):
        response = self.client.put('/accessories/1/activate')
        self.assertEqual(response.status_code, 204)

    def test_activate_accessory_not_found(self):
        # Test when activating an accessory that doesn't exist
        response = self.client.put('/accessories/99/activate')
        self.assertEqual(response.status_code, 404)

    def test_deactivate_accessory(self):
        response = self.client.put('/accessories/1/deactivate')
        self.assertEqual(response.status_code, 204)

    def test_deactivate_accessory_not_found(self):
        # Test when deactivating an accessory that doesn't exist
        response = self.client.put('/accessories/99/deactivate')
        self.assertEqual(response.status_code, 404)

    def test_get_train_speed_after_update(self):
        # Test getting train speed after updating
        self.client.put('/trains/1/speed', json={'speed': 75})
        response = self.client.get('/trains/1/speed')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('speed', data)
        self.assertEqual(data['speed'], 75)

    def test_get_train_direction_after_update(self):
        # Test getting train direction after updating
        self.client.put('/trains/1/direction', json={'direction': 'reverse'})
        response = self.client.get('/trains/1/direction')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('direction', data)
        self.assertEqual(data['direction'], 'reverse')

if __name__ == '__main__':
    unittest.main()

