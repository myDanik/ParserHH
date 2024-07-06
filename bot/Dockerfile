
FROM python:3.11.5


WORKDIR /bot


COPY requirements.txt /bot/

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . /bot/

CMD ["python", "tgbot.py"]
