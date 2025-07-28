CREATE TABLE IF NOT EXISTS leituras_iot (
    id SERIAL PRIMARY KEY,
    id_dispositivo TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperatura REAL,
    umidade REAL,
    pressao REAL,
    intensidade_luz REAL
);

CREATE TABLE IF NOT EXISTS anomalias_iot (
    id SERIAL PRIMARY KEY,
    id_dispositivo TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    campo TEXT NOT NULL,
    descricao TEXT,
    valor REAL
);
