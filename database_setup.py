# -*- coding: utf-8 -*-
import sqlite3

def criar_banco():
    conn = sqlite3.connect("sensor_data.db")
    cursor = conn.cursor()

    # Tabela de funcionários (sem relação com animais)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')

    # Tabela de animais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            breed TEXT NOT NULL,
            age INTEGER,
            sensor_id INTEGER NOT NULL,
            FOREIGN KEY (sensor_id) REFERENCES sensor_readings (id)
        )
    ''')

    # Tabela de leituras dos sensores com relação aos animais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL,
            heartbeat INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_banco()
    print("Banco de dados atualizado com sucesso!")
