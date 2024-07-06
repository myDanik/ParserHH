FROM python:3.11.5

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

