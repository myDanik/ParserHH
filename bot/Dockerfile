# Используем официальный образ Python
FROM python:3.11.5

# Устанавливаем рабочую директорию в контейнере
WORKDIR /bot

# Копируем файлы с зависимостями
COPY requirements.txt /bot/



# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /bot/

# Команда для запуска бота
CMD ["python", "tgbot.py"]
