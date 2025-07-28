from confluent_kafka import Consumer
import json
from shared import db

def consumir_dados(evento_de_parada):
    conexao = db.conectar_postgres()
    consumer = Consumer({
        'bootstrap.servers': 'kafka:29092',
        'group.id': 'grupo-consumidor-iot',
        'auto.offset.reset': 'earliest',
    })
    consumer.subscribe(['iot-dados'])

    print("Aguardando mensagens...\n (Pressione CTRL+C para sair)\n")

    try:
        while not evento_de_parada.is_set():
            mensagem = consumer.poll(1.0)

            if mensagem is None:
                continue
            if mensagem.error():
                print(f"Erro na leitura da mensagem: {mensagem.error()}")
                continue

            try:
                leitura = json.loads(mensagem.value().decode('utf-8'))
                anomalias = verificar_anomalias(leitura)

                if not anomalias:
                    db.inserir_leitura(conexao, leitura)
                else:
                    for campo, descricao, valor in anomalias:
                        db.inserir_anomalia(conexao, leitura, campo, descricao, valor)
                    print(f"[🚨 Anomalia] {leitura['id_dispositivo']} - {anomalias}")

            except json.JSONDecodeError:
                print("Mensagem recebida, porém: erro ao decodificar")

    except KeyboardInterrupt:
        print("\nSaindo do programa...")

    finally:
        consumer.close()
        conexao.close()

def verificar_anomalias(leitura):
    anomalias = []

    if leitura["temperatura"] < -50 or leitura["temperatura"] > 60:
        anomalias.append(("temperatura", "fora do intervalo", leitura["temperatura"]))

    if leitura["umidade"] < 0 or leitura["umidade"] > 100:
        anomalias.append(("umidade", "fora do intervalo", leitura["umidade"]))

    if leitura["pressao"] < 800 or leitura["pressao"] > 1200:
        anomalias.append(("pressao", "fora do intervalo", leitura["pressao"]))

    if leitura["intensidade_luz"] < 0 or leitura["intensidade_luz"] > 150:
        anomalias.append(("intensidade_luz", "fora do intervalo", leitura["intensidade_luz"]))

    return anomalias



if __name__ == "__main__":
    from threading import Event
    import time

    stop_event = Event()
    try:
        consumir_dados(stop_event)
    except KeyboardInterrupt:
        print("[Consumer] Interrompido pelo usuário.")
        stop_event.set()
        time.sleep(1)
