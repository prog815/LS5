FROM python:3.10

RUN mkdir -p /app
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3","app.py"]
