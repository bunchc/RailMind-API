# routes.py

from flask import jsonify
from flask_restful import Resource, reqparse
from app import app, api

from RPiMotorLib import RPiMotorDC

# Sample data for trains and accessories
trains = [
    {'id': 1, 'name': 'Express Train', 'speed': 0, 'direction': 'forward'},
    {'id': 2, 'name': 'Freight Train', 'speed': 0, 'direction': 'forward'},
]

accessories = [
    {'id': 1, 'name': 'Signal Light', 'activated': False},
    {'id': 2, 'name': 'Crossing Gate', 'activated': False},
]

# Initialize the DC motors for each train
motor_channels = [f"MOTOR{i}" for i in range(1, len(trains) + 1)]
motors = {train['id']: RPiMotorDC(channel, 200) for train, channel in zip(trains, motor_channels)}

# Define parsers
speed_parser = reqparse.RequestParser()
speed_parser.add_argument('speed', type=int, help='Speed value (0-100)', required=True)

direction_parser = reqparse.RequestParser()
direction_parser.add_argument('direction', type=str, choices=('forward', 'reverse'), help='Direction (forward or reverse)', required=True)

class TrainListResource(Resource):
    def get(self):
        return jsonify({'trains': trains})

class TrainSpeedResource(Resource):
    def put(self, train_id):
        args = speed_parser.parse_args()
        speed = args['speed']
        for train in trains:
            if train['id'] == train_id:
                train['speed'] = speed

                # Control the DC motor based on the speed
                motor = motors[train_id]
                motor.setMotorSpeed(speed)
                motor.motorRun()

                return '', 204
        return jsonify({'error': 'Train not found'}), 404

class TrainDirectionResource(Resource):
    def put(self, train_id):
        args = direction_parser.parse_args()
        direction = args['direction']
        for train in trains:
            if train['id'] == train_id:
                train['direction'] = direction
                return '', 204
        return jsonify({'error': 'Train not found'}), 404

class AccessoryListResource(Resource):
    def get(self):
        return jsonify({'accessories': accessories})

class AccessoryActivateResource(Resource):
    def put(self, accessory_id):
        for accessory in accessories:
            if accessory['id'] == accessory_id:
                accessory['activated'] = True
                return '', 204
        return jsonify({'error': 'Accessory not found'}), 404

class AccessoryDeactivateResource(Resource):
    def put(self, accessory_id):
        for accessory in accessories:
            if accessory['id'] == accessory_id:
                accessory['activated'] = False
                return '', 204
        return jsonify({'error': 'Accessory not found'}), 404

# API routes
api.add_resource(TrainListResource, '/trains')
api.add_resource(TrainSpeedResource, '/trains/<int:train_id>/speed')
api.add_resource(TrainDirectionResource, '/trains/<int:train_id>/direction')
api.add_resource(AccessoryListResource, '/accessories')
api.add_resource(AccessoryActivateResource, '/accessories/<int:accessory_id>/activate')
api.add_resource(AccessoryDeactivateResource, '/accessories/<int:accessory_id>/deactivate')

if __name__ == '__main__':
    app.run(debug=True)
