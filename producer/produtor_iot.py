import faker
from confluent_kafka import Producer
import json
import datetime
import random
import os

NUMERO_DISPOSITIVOS = int(os.getenv("NUMERO_DISPOSITIVOS", 100))
INTERVALO_MSG_SEGUNDOS = float(os.getenv("INTERVALO_MSG_SEGUNDOS", 0.5))
NOME_TOPICO_PRINCIPAL = os.getenv("NOME_TOPICO_PRINCIPAL", "iot-dados")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")
PROBABILIDADE_ANOMALIA = float(os.getenv("PROBABILIDADE_ANOMALIA", 0.15))

def dados_iot(evento_de_parada):
    ids_dispositivos = [f"sensor_{i:03d}" for i in range(NUMERO_DISPOSITIVOS)]
    try:
        print("Gerando dados...")
        produtor = Producer({'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS})
        fake = faker.Faker('pt_BR')

        while not evento_de_parada.is_set():
            leitura = {
                "id_dispositivo": random.choice(ids_dispositivos),
                "timestamp": datetime.datetime.now().isoformat(),
                "temperatura": fake.pyfloat(min_value=-10, max_value=40, right_digits=2),
                "umidade": fake.pyfloat(min_value=20, max_value=80, right_digits=1),
                "pressao": fake.pyfloat(min_value=900, max_value=1100, right_digits=1),
                "intensidade_luz": fake.pyfloat(min_value=0, max_value=100, right_digits=1),
            }

            if random.random() < PROBABILIDADE_ANOMALIA:
                inserir_anomalia(leitura)


            leitura = json.dumps(leitura).encode('utf-8')

            produtor.produce(NOME_TOPICO_PRINCIPAL, leitura, callback=verificar_erro)
            time.sleep(INTERVALO_MSG_SEGUNDOS)

        produtor.flush()
        print(f"Dados enviados com sucesso!")

    except Exception as e:
        print(f"Erro ao gerar dados: {e}")

def inserir_anomalia(leitura):
    aux = random.randint(0, 100)
    if aux < 20:
        leitura["temperatura"] = -1000
    elif aux < 40:
        leitura["umidade"] = 200
    elif aux < 60:
        leitura["pressao"] = 5000
    elif aux < 80:
        leitura["intensidade_luz"] = 200

def verificar_erro(err, msg):
    if err:
        print(f"[Kafka Error] {err}")


if __name__ == "__main__":
    from threading import Event
    import time

    stop_event = Event()
    try:
        dados_iot(stop_event)
    except KeyboardInterrupt:
        print("[Producer] Interrompido pelo usuário.")
        stop_event.set()
        time.sleep(1)
