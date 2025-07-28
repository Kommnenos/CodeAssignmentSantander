from confluent_kafka.admin import AdminClient
import time

def checar_topico_existe(topico: str, timeout_segundos: int = 30, intervalo: float = 1.0):
    admintoken = AdminClient({'bootstrap.servers': 'kafka:29092'})
    tempo_corrido = 0

    while tempo_corrido < timeout_segundos:
        metadata = admintoken.list_topics(timeout=2.0)
        if topico in metadata.topics and not metadata.topics[topico].error:
            print(f"O topico {topico} existe")
            return
        print(f"Aguardando {intervalo} segundos para checar se o topico {topico} existe")
        time.sleep(intervalo)
        tempo_corrido += intervalo

    raise TimeoutError(f"Topico '{topico}' não foi encontrado após {timeout_segundos} segundos.")

