from producer.produtor_iot import dados_iot
from threading import Thread, Event
from consumer.consumidor_iot import consumir_dados
from shared.utils import checar_topico_existe

evento_de_parada = Event()

def main():
    thread_produtor = Thread(target=dados_iot, args=(evento_de_parada,))
    thread_produtor.start()

    try:
        checar_topico_existe('iot-dados', timeout_segundos=20)
    except TimeoutError as e:
        print(f"Erro: {e}")
        evento_de_parada.set()
        thread_produtor.join()
        return

    thread_consumidor = Thread(target=consumir_dados, args=(evento_de_parada,))
    thread_consumidor.start()


    try:
        thread_produtor.join()
        thread_consumidor.join()
    except KeyboardInterrupt:
        print("\nSaindo do programa...")
        evento_de_parada.set()
        thread_produtor.join()
        thread_consumidor.join()


if __name__ == '__main__':
    main()


