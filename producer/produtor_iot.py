import faker
from confluent_kafka import Producer
import json
import datetime
import random
import time

def dados_iot(evento_de_parada):
    ids_dispositivos = [f"sensor_{i:03d}" for i in range(10)]
    try:
        print("Gerando dados...")
        produtor = Producer({'bootstrap.servers': 'localhost:9092'})
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

            if random.random() < 0.15:
                inserir_anomalia(leitura)


            leitura = json.dumps(leitura).encode('utf-8')

            produtor.produce('iot-dados', leitura, callback=verificar_erro)
            time.sleep(0.5)

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
