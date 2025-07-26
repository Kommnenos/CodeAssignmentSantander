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
                print(f"Leitura: {leitura}")
            except json.JSONDecodeError:
                print("Mensagem recebida, porém: erro ao decodificar")

    except KeyboardInterrupt:
        print("\nSaindo do programa...")

    finally:
        consumer.close()

