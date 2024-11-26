# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect("DATABASE_URL")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

# Rota para cadastrar um funcionário
@app.route('/api/employees', methods=['POST'])
def add_employee():
    data = request.get_json()
    if not data or 'name' not in data or 'role' not in data or 'email' not in data:
        return jsonify({"error": "Dados incompletos para cadastrar o funcionário"}), 400

    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO employees (name, role, email)
                VALUES (?, ?, ?)
            ''', (data['name'], data['role'], data['email']))
            conn.commit()
        return jsonify({"message": "Funcionário cadastrado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email já cadastrado"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para cadastrar um animal
@app.route('/api/animals', methods=['POST'])
def add_animal():
    data = request.get_json()
    if not data or 'name' not in data or 'breed' not in data or 'sensor_id' not in data:
        return jsonify({"error": "Dados incompletos para cadastrar o animal"}), 400

    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO animals (name, breed, age, sensor_id)
                VALUES (?, ?, ?, ?)
            ''', (data['name'], data['breed'], data.get('age', None), data['sensor_id']))
            conn.commit()
        return jsonify({"message": "Animal cadastrado com sucesso!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Sensor ID não encontrado ou inválido"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para adicionar uma leitura do sensor
@app.route('/api/sensor_readings', methods=['POST'])
def add_sensor_reading():
    data = request.get_json()
    if not data or 'temperature' not in data or 'heartbeat' not in data:
        return jsonify({"error": "Dados incompletos para registrar leitura"}), 400

    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO sensor_readings (temperature, heartbeat)
                VALUES (?, ?)
            ''', (data['temperature'], data['heartbeat']))
            conn.commit()
        return jsonify({"message": "Leitura do sensor registrada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para consultar todos os animais e suas leituras de sensores
@app.route('/api/animals', methods=['GET'])
def get_animals():
    try:
        with get_db_connection() as conn:
            rows = conn.execute('''
                SELECT animals.id, animals.name, animals.breed, animals.age,
                       sensor_readings.temperature, sensor_readings.heartbeat, sensor_readings.timestamp
                FROM animals
                LEFT JOIN sensor_readings ON animals.sensor_id = sensor_readings.id
                ORDER BY animals.id
            ''').fetchall()
        return jsonify([dict(row) for row in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para consultar todas as leituras de sensores
@app.route('/api/sensor_readings', methods=['GET'])
def get_sensor_readings():
    try:
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM sensor_readings ORDER BY timestamp DESC').fetchall()
        return jsonify([dict(row) for row in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota para consultar todos os funcionários
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        with get_db_connection() as conn:
            rows = conn.execute('SELECT * FROM employees ORDER BY id').fetchall()
        return jsonify([dict(row) for row in rows]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar a API
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
