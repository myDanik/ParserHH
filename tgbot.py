import asyncio
import requests
from bs4 import BeautifulSoup
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import aiohttp
from Enums.vacancy_parms_validation import *
from Enums.resume_parms_validation import *
from url import TOKEN
bot = AsyncTeleBot(TOKEN)

user_states = {}
user_data = {}

class Count(Enum):
    COUNT_20 = '20'
    COUNT_40 = '40'
    COUNT_ALL = '0'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет, этот бот позволяет получить информацию о резюме и вакансиях с сайта hh.ru. Для получения информации по вакансиям отправьте команду /vacancy'
    await bot.reply_to(message, text)

@bot.message_handler(commands=['vacancy'])
async def start_vacancy_process(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    user_states[chat_id] = 'GET_TEXT'
    await bot.send_message(chat_id, "Введите текст для поиска:")

@bot.message_handler(func=lambda message: True)
async def handle_message(message):
    chat_id = message.chat.id

    if chat_id in user_states:
        state = user_states[chat_id]

        if state == 'GET_TEXT':

            user_data[chat_id]['text'] = message.text
            user_states[chat_id] = 'GET_EDUCATION'
            await bot.send_message(chat_id, "Выберите уровень образования:", reply_markup=create_enum_markup(Vacancy_Education))
        elif state == 'GET_EDUCATION':
            user_data[chat_id]['education'] = convert_to_enum_value(Vacancy_Education, message.text)
            user_states[chat_id] = 'GET_PART_TIME'
            await bot.send_message(chat_id, "Выберите тип занятости:", reply_markup=create_enum_markup(Vacancy_PartTime))
        elif state == 'GET_PART_TIME':
            user_data[chat_id]['part_time'] = convert_to_enum_value(Vacancy_PartTime, message.text)
            user_states[chat_id] = 'GET_EXPERIENCE'
            await bot.send_message(chat_id, "Выберите опыт работы:", reply_markup=create_enum_markup(Vacancy_Experience))
        elif state == 'GET_EXPERIENCE':
            user_data[chat_id]['experience'] = convert_to_enum_value(Vacancy_Experience, message.text)
            user_states[chat_id] = 'GET_SCHEDULE'
            await bot.send_message(chat_id, "Выберите график работы:", reply_markup=create_enum_markup(Vacancy_Schedule))
        elif state == 'GET_SCHEDULE':
            user_data[chat_id]['schedule'] = convert_to_enum_value(Vacancy_Schedule, message.text)
            user_states[chat_id] = 'GET_COUNT'
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('20'), types.KeyboardButton('40'))
            await bot.send_message(chat_id, "Выберите количество вакансий:", reply_markup=(markup))
        elif state == 'GET_COUNT':
            user_data[chat_id]['count'] = convert_to_enum_value(Count, message.text)
            await bot.send_message(chat_id, "Идет поиск вакансий, подождите...", reply_markup=types.ReplyKeyboardRemove())
            user_states.pop(chat_id)

            text = user_data[chat_id]['text']
            education = user_data[chat_id]['education']
            part_time = user_data[chat_id]['part_time']
            experience = user_data[chat_id]['experience']
            schedule = user_data[chat_id]['schedule']
            count = user_data[chat_id]['count']
            result = await fetch_vacancies(text, education, part_time, experience, schedule, count)
            for vacancy_dict in result:
                await bot.send_message(chat_id, format_vacancy_info(vacancy_dict))

def create_enum_markup(enum_cls):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in enum_cls:
        markup.add(item.value)
    return markup



def convert_to_enum_value(enum_cls, value):
    for item in enum_cls:
        if item.value == value:
            return item
    raise ValueError(f"Invalid value '{value}' for enum '{enum_cls}'")
def format_vacancy_info(vacancy_dict):
    print(vacancy_dict.get("url"))
    URL = ("https://" + str(vacancy_dict.get("url")).split(".", 1 )[1]).replace("vacancies", "vacancy")
    return f"""
    URL: {URL}
    Название: {vacancy_dict.get("name")}
    Город: {vacancy_dict.get("area")}
    Работодатель: {vacancy_dict.get("employer_name")}
    Описание: {vacancy_dict.get("description")}
    Зарплата: от {vacancy_dict['salary_from']} до {vacancy_dict['salary_to']}
    Опыт работы(мес.): {vacancy_dict.get("experience")}
    График: {vacancy_dict['schedule']}
    Занятость: {vacancy_dict.get("employment")}
    Навыки: {(vacancy_dict.get("key_skills"))}
    Водительское Удостоверение: {vacancy_dict.get("driver_licence")}
    Знание языков: {vacancy_dict.get("languages")}
    Контакты: {vacancy_dict.get("contacts")}
    """
async def fetch_vacancies(text, education, part_time, experience, schedule, count):
    url = f"http://127.0.0.1:8000/vacancy"
    cnt = int(count.value)//20
    params = {
        "text": text,
        "education": education.value,
        "part_time": part_time.value,
        "experience": experience.value,
        "schedule": schedule.value,
        "count": cnt
    }
    print("Fetch vacancies")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                print(data.get("data"))
                return data.get("data")
            else:
                return []

asyncio.run(bot.polling())