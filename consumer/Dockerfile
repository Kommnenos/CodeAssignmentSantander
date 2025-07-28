FROM python:3.13

LABEL authors="Pedro Lealdini"

WORKDIR /app

COPY shared ./shared
COPY consumer/consumidor_iot.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "consumidor_iot.py"]
