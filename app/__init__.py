# app/__init__.py

from flask import Flask
from flask_restful import Api
from RPiMotorLib import RPiMotorDC

app = Flask(__name__)
api = Api(app)

# Initialize the DC motors for each train
trains = [
    {'id': 1, 'name': 'Express Train', 'speed': 0, 'direction': 'forward'},
    {'id': 2, 'name': 'Freight Train', 'speed': 0, 'direction': 'forward'},
]

motor_channels = [f"MOTOR{i}" for i in range(1, len(trains) + 1)]
motors = {train['id']: RPiMotorDC(channel, 200) for train, channel in zip(trains, motor_channels)}

from app import routes  # noqa
