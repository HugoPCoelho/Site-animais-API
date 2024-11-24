# -*- coding: utf-8 -*-
import sqlite3

# Função para criar o banco de dados e a tabela
def criar_banco():
    try:
        # Conexão com o banco de dados
        conn = sqlite3.connect("sensor_data.db")
        cursor = conn.cursor()

        # Criação da tabela com os campos adicionais
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                temperature REAL NOT NULL,
                heartbeat INTEGER NOT NULL,
                animal_name TEXT NOT NULL,
                breed TEXT NOT NULL
            )
        ''')
        print("Tabela 'sensor_readings' criada ou já existe.")

        conn.commit()
    except sqlite3.Error as e:
        print("Erro ao criar a tabela: {}".format(e))  # Corrigido aqui
    finally:
        conn.close()

# Verifica se o código está sendo executado como script principal
if __name__ == "__main__":
    criar_banco()
    print("Banco de dados configurado com sucesso!")

