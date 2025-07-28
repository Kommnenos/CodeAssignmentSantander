CREATE TABLE IF NOT EXISTS leituras_iot (
    id SERIAL PRIMARY KEY,
    id_dispositivo TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperatura REAL,
    umidade REAL,
    pressao REAL,
    intensidade_luz REAL
);

