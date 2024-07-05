import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import aiohttp
from Enums.vacancy_parms_validation import *
from Enums.resume_parms_validation import *
from Enums.translate_dict import *
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

    text = 'Привет, этот бот позволяет получить информацию о резюме и вакансиях с сайта hh.ru.\nДля получения информации по вакансиям отправьте команду /vacancy.\nДля получения информации по резюме отправьте команду /resume'
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('/vacancy'), types.KeyboardButton('/resume'))
    await bot.reply_to(message, text, reply_markup=markup)

@bot.message_handler(commands=['vacancy'])
async def start_vacancy_process(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    user_states[chat_id] = 'GET_TEXT'
    await bot.send_message(chat_id, "Введите текст для поиска:", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) in ['GET_TEXT', 'GET_EDUCATION', 'GET_PART_TIME', 'GET_EXPERIENCE', 'GET_SCHEDULE', 'GET_COUNT'])
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
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('/vacancy'), types.KeyboardButton('/resume'))
            for vacancy_dict in result:
                await bot.send_message(chat_id, format_vacancy_info(vacancy_dict), reply_markup=markup)

def create_enum_markup(enum_cls):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for item in enum_cls:
        markup.add(translate_parms.get(str(item.value)))
    return markup



def convert_to_enum_value(enum_cls, value):
    for item in enum_cls:
        if item.value == reverse_translate_parms.get(value):
            return item
    raise ValueError(f"Invalid value '{value}' for enum '{enum_cls}'")
def format_vacancy_info(vacancy_dict):
    print(vacancy_dict.get("url"))
    URL = ("https://" + str(vacancy_dict.get("url")).split(".", 1 )[1]).replace("vacancies", "vacancy")
    message = f"""
    URL: {URL}
    Название: {vacancy_dict.get("name")}
    Город: {vacancy_dict.get("area")}
    Работодатель: {vacancy_dict.get("employer_name")}
    Описание: {vacancy_dict.get("description")}
    Зарплата: от {vacancy_dict['salary_from']} до {vacancy_dict['salary_to']}
    Опыт работы: {vacancy_dict.get("experience")}
    График: {vacancy_dict['schedule']}
    Занятость: {vacancy_dict.get("employment")}
    Навыки: {(vacancy_dict.get("key_skills"))}
    Водительское Удостоверение: {vacancy_dict.get("driver_licence")}
    Знание языков: {vacancy_dict.get("languages")}
    Контакты: {vacancy_dict.get("contacts")}
    """
    print(len(message))
    if len(message)>4095:
        return f"Текст вакансии превышает возможную длину сообщения Telegram, вакансия доступна по ссылке {URL}"
    else:
        return message

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

                return data.get("data")
            else:
                return []



@bot.message_handler(commands=['resume'])
async def start_resume_process(message):
    chat_id = message.chat.id
    user_data[chat_id] = {}
    user_states[chat_id] = 'GET_TEXT_RESUME'
    await bot.send_message(chat_id, "Введите текст для поиска резюме:", reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) in ['GET_TEXT_RESUME', 'GET_RELOCATION','GET_SEX', 'GET_JOBSEARCHSTATUS', 'GET_EDUCATION_RESUME', 'GET_EMPLOYMET', 'GET_EXPERIENCE_RESUME', 'GET_SCHEDULE_RESUME', 'GET_COUNT_RESUME'])
async def handle_message_resume(message):
    chat_id = message.chat.id
    print("chat")
    if chat_id in user_states:
        state = user_states[chat_id]

        if state == 'GET_TEXT_RESUME':
            user_data[chat_id]['text_resume'] = message.text
            user_states[chat_id] = 'GET_RELOCATION'
            await bot.send_message(chat_id, "Выберите возможность переезда:", reply_markup=create_enum_markup(Resume_Relocation))
        elif state == 'GET_RELOCATION':
            user_data[chat_id]['relocation'] = convert_to_enum_value(Resume_Relocation, message.text)
            user_states[chat_id] = 'GET_SEX'
            await bot.send_message(chat_id, "Выберите пол:", reply_markup=create_enum_markup(Resume_Sex))
        elif state == 'GET_SEX':
            user_data[chat_id]['sex'] = convert_to_enum_value(Resume_Sex, message.text)
            user_states[chat_id] = 'GET_JOBSEARCHSTATUS'
            await bot.send_message(chat_id, "Выберите статус поиска работы:", reply_markup=create_enum_markup(Resume_JobSearchStatus))
        elif state == 'GET_JOBSEARCHSTATUS':
            user_data[chat_id]['jobsearchstatus'] = convert_to_enum_value(Resume_JobSearchStatus, message.text)
            user_states[chat_id] = 'GET_EDUCATION_RESUME'
            await bot.send_message(chat_id, "Выберите Уровень образования:", reply_markup=create_enum_markup(Resume_Education))
        elif state == 'GET_EDUCATION_RESUME':
            user_data[chat_id]['education_resume'] = convert_to_enum_value(Resume_Education, message.text)
            user_states[chat_id] = 'GET_EMPLOYMET'
            await bot.send_message(chat_id, "Выберите статуз занятости:", reply_markup=create_enum_markup(Resume_Employment))
        elif state == 'GET_EMPLOYMET':
            user_data[chat_id]['employment'] = convert_to_enum_value(Resume_Employment, message.text)
            user_states[chat_id] = 'GET_EXPERIENCE_RESUME'
            await bot.send_message(chat_id, "Выберите опыт работы:", reply_markup=create_enum_markup(Resume_Experience))
        elif state == 'GET_EXPERIENCE_RESUME':
            user_data[chat_id]['experience_resume'] = convert_to_enum_value(Resume_Experience, message.text)
            user_states[chat_id] = 'GET_SCHEDULE_RESUME'
            await bot.send_message(chat_id, "Выберите График работы:", reply_markup=create_enum_markup(Resume_Schedule))
        elif state == 'GET_SCHEDULE_RESUME':
            user_data[chat_id]['schedule_resume'] = convert_to_enum_value(Resume_Schedule, message.text)
            user_states[chat_id] = 'GET_COUNT_RESUME'
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('20'), types.KeyboardButton('40'))
            await bot.send_message(chat_id, "Выберите количество резюме:", reply_markup=(markup))
        elif state == 'GET_COUNT_RESUME':
            user_data[chat_id]['count_resume'] = convert_to_enum_value(Count, message.text)
            await bot.send_message(chat_id, "Идет поиск резюме, подождите...", reply_markup=types.ReplyKeyboardRemove())
            user_states.pop(chat_id)

            text = user_data[chat_id]['text_resume']
            relocation = user_data[chat_id]['relocation']
            sex = user_data[chat_id]['sex']
            job_search_status = user_data[chat_id]['jobsearchstatus']
            education = user_data[chat_id]['education_resume']
            employment = user_data[chat_id]['employment']
            experience = user_data[chat_id]['experience_resume']
            schedule = user_data[chat_id]['schedule_resume']
            count = user_data[chat_id]['count_resume']
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('/vacancy'), types.KeyboardButton('/resume'))
            result = await fetch_resumes(text, relocation, sex, job_search_status, education, employment, experience, schedule, count)
            for resume_dict in result:
                await bot.send_message(chat_id, format_resume_info(resume_dict),reply_markup=markup)
async def fetch_resumes(text, relocation, sex, job_search_status, education, employment, experience, schedule, count):
    url = f"http://127.0.0.1:8000/resume"
    cnt = int(count.value)//20
    params = {
        "text": text,
        "relocation": relocation.value,
        "sex": sex.value,
        "job_search_status": job_search_status.value,
        "education": education.value,
        "employment": employment.value,
        "experience": experience.value,
        "schedule": schedule.value,
        "count": cnt
    }
    print("Fetch vacancies")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()

                return data.get("data")
            else:
                return []
def format_resume_info(resume_dict):
    print(resume_dict.get("url"))
    URL = resume_dict.get("url")
    message = f"""
        URL: {URL}
        Пол: {resume_dict.get("sex")} {resume_dict.get("age") if resume_dict.get("age") != 0 else "???"} г.
        {resume_dict.get("job_search_status")}
        Город: {resume_dict.get("personal_address")}
        Позиция: {resume_dict.get("specialization")}
        {resume_dict.get("work_schedule")}
        ```Описание: {resume_dict.get("about_me")}
        Опыт работы: {resume_dict.get("experience")//12} г. {resume_dict.get("experience") - (resume_dict.get("experience")//12)*12} мес.
        Навыки: {(resume_dict.get("skills"))}
        {resume_dict.get("education")}
        Знание языков: {resume_dict.get("language")}
        """
    print(len(message))
    if len(message) > 4095:
        return f"Текст резюме превышает возможную длину сообщения Telegram, резюме доступно по ссылке {URL}"
    else:
        return message
asyncio.run(bot.polling())