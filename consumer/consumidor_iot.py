from confluent_kafka import Consumer
import json

def consumir_dados(evento_de_parada):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
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

                if anomalias:
                    print(f"[Anomalia] {leitura['id_dispositivo']} - {anomalias} - ")
                print(f"Leitura: {leitura}")

            except json.JSONDecodeError:
                print("Mensagem recebida, porém: erro ao decodificar")

    except KeyboardInterrupt:
        print("\nSaindo do programa...")

    finally:
        consumer.close()

def verificar_anomalias(leitura):
    anomalias = []

    if leitura["temperatura"] < -50 or leitura["temperatura"] > 60:
        anomalias.append("temperatura fora do intervalo")
    if leitura["umidade"] < 0 or leitura["umidade"] > 100:
        anomalias.append("umidade fora do intervalo")
    if leitura["pressao"] < 800 or leitura["pressao"] > 1200:
        anomalias.append("pressão fora do intervalo")
    if leitura["intensidade_luz"] < 0 or leitura["intensidade_luz"] > 150:
        anomalias.append("intensidade de luz fora do intervalo")

    return anomalias
