# Monitoramento de Sensores IoT

Code Assignment - Pedro Lealdini

## Para Rodar:
```bash
git clone https://github.com/Kommnenos/Simulador-IoT.git
docker-compose up
```
- aguarde alguns minutos para que o sistema verifique que todos os serviços estão saudáveis
- ctrl+c para parar
## O Sistema:
- Irá armazenar as leituras de IoT em uma tabela
- Irá armazenar as anomalias em outra tabela
- Alertará nos logs quando ocorrerem anomalias

## Para a visualização dos resultados:

| Serviço    | Endereço                                      | Notas                              |
| ---------- | ---------------------------------------------- | ------------------------------------- |
| Adminer    | [http://localhost:8081](http://localhost:8081) | Serviço PostgreSQL, servidor: postgres login: postgres, senha: 12345, db: iot |
| Redpanda Console   | [http://localhost:8080](http://localhost:8080) | Visualização do Kafka        |

