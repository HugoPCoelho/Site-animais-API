# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect("sensor_data.db")
    conn.row_factory = sqlite3.Row  # Permite acessar colunas como dicionários
    return conn

# Rota para receber dados (POST)
@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        # Obtém os dados enviados no corpo da requisição
        data = request.get_json()

        # Verifica se os campos necessários estão presentes
        if 'temperature' not in data or 'heartbeat' not in data:
            return jsonify({"error": "Os campos 'temperature' e 'heartbeat' são obrigatórios."}), 400

        temperature = data['temperature']
        heartbeat = data['heartbeat']

        # Insere os dados no banco de dados
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO sensor_readings (temperature, heartbeat) VALUES (?, ?)',
            (temperature, heartbeat)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Dados armazenados com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao armazenar dados: {str(e)}"}), 500

# Rota para consultar dados (GET)
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Consulta os dados do banco
        conn = get_db_connection()
        rows = conn.execute(
            'SELECT id, temperature, heartbeat, timestamp FROM sensor_readings ORDER BY timestamp DESC'
        ).fetchall()
        conn.close()

        # Converte os dados para uma lista de dicionários
        result = [dict(row) for row in rows]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao consultar dados: {str(e)}"}), 500

# Rota para atualizar dados existentes (PUT)
@app.route('/api/data/<int:data_id>', methods=['PUT'])
def update_data(data_id):
    try:
        data = request.get_json()

        if 'temperature' not in data or 'heartbeat' not in data:
            return jsonify({"error": "Os campos 'temperature' e 'heartbeat' são obrigatórios."}), 400

        temperature = data['temperature']
        heartbeat = data['heartbeat']

        conn = get_db_connection()
        cursor = conn.execute(
            'UPDATE sensor_readings SET temperature = ?, heartbeat = ? WHERE id = ?',
            (temperature, heartbeat, data_id)
        )
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return jsonify({"error": "Registro não encontrado para atualizar."}), 404

        return jsonify({"message": "Dados atualizados com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar dados: {str(e)}"}), 500

# Rota para cadastrar novos dados manualmente (POST)
@app.route('/api/data/manual', methods=['POST'])
def add_data_manually():
    try:
        data = request.get_json()

        if 'temperature' not in data or 'heartbeat' not in data:
            return jsonify({"error": "Os campos 'temperature' e 'heartbeat' são obrigatórios."}), 400

        temperature = data['temperature']
        heartbeat = data['heartbeat']

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO sensor_readings (temperature, heartbeat) VALUES (?, ?)',
            (temperature, heartbeat)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Dados cadastrados manualmente com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": f"Erro ao cadastrar dados manualmente: {str(e)}"}), 500

# Inicializa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
