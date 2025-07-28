FROM python:3.13

LABEL authors="Pedro Lealdini"
WORKDIR /app

COPY shared ./shared
COPY producer/produtor_iot.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "produtor_iot.py"]
