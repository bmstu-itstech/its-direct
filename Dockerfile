FROM python:3.10.15

WORKDIR /bot
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /bot/

CMD ["python", "main.py"]
