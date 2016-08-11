host = "127.0.0.1"
port = 5000

import os, sys
sys.path.append('../modules/')
import json

import pandas as pd
import numpy as np

import requests
from flask import Flask, url_for, render_template
from flask import request
from flask_socketio import SocketIO, send, emit
import generators

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_json_filenames():
    return filter(lambda file: file.endswith(".json"), os.listdir("resources"))

def get_csv_filenames():
    return filter(lambda file: file.endswith(".csv"), os.listdir("resources"))

def get_json(filename=None):
    with open("resources/"+filename) as json_file:
        return json.load(json_file)

def get_csv_resource(filename):
    return pd.read_csv(os.path.join(os.path.dirname(__file__), "resources/"+filename), sep = ',')

@socketio.on('csv/files')
def get_csv_files():
    emit('csv/files', get_csv_filenames())

@socketio.on('csv/data')
def get_csv_data(json):
    csv = get_csv_resource(json["filename"])
    emit('csv/data', {
        "columns": list(csv.columns.values),
        "data": csv.as_matrix().tolist()
    })

@socketio.on('csv/imitate')
def imitate(json):
    generator = generators.Imitator(json["filename"])
    samples = generator.simulate(100, json["columns"])
    generator.plot(samples[:, :2])
    emit('csv/imitate', samples.tolist())

@socketio.on('csv/imitate/normal')
def imitate_normal(json):
    generator = generators.Imitator(json["filename"])
    samples = generator.simulate_with_normal(100, json["columns"])
    emit('csv/imitate/normal', samples.tolist())

@socketio.on('csv/imitate/nonnormal')
def imitate_nonnormal(json):
    generator = generators.Imitator(json["filename"])
    samples = generator.simulate_with_nonnormal(100, json["columns"])
    emit('csv/imitate/nonnormal', samples.tolist())

if __name__ == '__main__':
    socketio.run(app, debug=True, port=port, host=host)
