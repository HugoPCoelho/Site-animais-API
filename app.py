# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect("sensor_data.db")
    conn.row_factory = sqlite3.Row
    return conn

# Rota para cadastrar dados (POST)
@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        # Verifica e processa os dados recebidos
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado enviado!"}), 400

        temperature = data.get('temperature')
        heartbeat = data.get('heartbeat')
        animal_name = data.get('animal_name')
        breed = data.get('breed')

        if not all([temperature, heartbeat, animal_name, breed]):
            return jsonify({"error": "Todos os campos são obrigatórios: temperature, heartbeat, animal_name, breed"}), 400

        # Insere os dados no banco de dados
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO sensor_readings (temperature, heartbeat, animal_name, breed)
            VALUES (?, ?, ?, ?)
        ''', (temperature, heartbeat, animal_name, breed))
        conn.commit()
        conn.close()

        return jsonify({"message": "Dados armazenados com sucesso!"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Erro no banco de dados: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro desconhecido: {str(e)}"}), 500

# Rota para consultar todos os dados (GET)
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        conn = get_db_connection()
        rows = conn.execute('SELECT * FROM sensor_readings ORDER BY timestamp DESC').fetchall()
        conn.close()

        # Formata os dados para JSON
        return jsonify([dict(row) for row in rows]), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Erro no banco de dados: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro desconhecido: {str(e)}"}), 500

# Rota para atualizar dados por ID (PUT)
@app.route('/api/data/<int:id>', methods=['PUT'])
def update_data(id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Nenhum dado enviado!"}), 400

        temperature = data.get('temperature')
        heartbeat = data.get('heartbeat')
        animal_name = data.get('animal_name')
        breed = data.get('breed')

        if not all([temperature, heartbeat, animal_name, breed]):
            return jsonify({"error": "Todos os campos são obrigatórios: temperature, heartbeat, animal_name, breed"}), 400

        conn = get_db_connection()
        cursor = conn.execute('''
            UPDATE sensor_readings
            SET temperature = ?, heartbeat = ?, animal_name = ?, breed = ?
            WHERE id = ?
        ''', (temperature, heartbeat, animal_name, breed, id))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Nenhum dado encontrado para atualizar."}), 404

        return jsonify({"message": "Dados atualizados com sucesso!"}), 200
    except sqlite3.Error as e:
        return jsonify({"error": f"Erro no banco de dados: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro desconhecido: {str(e)}"}), 500

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
