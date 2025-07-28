import psycopg2
import os

def conectar_postgres():
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        port=int(os.getenv('POSTGRES_PORT', '5432')),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', '12345'),
        dbname=os.getenv('POSTGRES_DB', 'iot')
    )

def inserir_leitura(conn, leitura):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO leituras_iot (
                id_dispositivo, timestamp,
                temperatura, umidade, pressao, intensidade_luz
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            leitura["id_dispositivo"],
            leitura["timestamp"],
            leitura["temperatura"],
            leitura["umidade"],
            leitura["pressao"],
            leitura["intensidade_luz"]
        ))
    conn.commit()

def inserir_anomalia(conn, leitura, campo, descricao, valor):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO anomalias_iot (
                id_dispositivo, timestamp,
                campo, descricao, valor
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            leitura["id_dispositivo"],
            leitura["timestamp"],
            campo,
            descricao,
            valor
        ))
    conn.commit()

