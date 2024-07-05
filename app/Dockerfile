# Используем официальный образ Python
FROM python:3.11.5

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы с зависимостями
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /app/

# Команда для запуска приложения
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

