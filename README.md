**Учебная практика** <br/>
Для запуска проекта сделайте `git clone https://github.com/myDanik/ParserHH.git`, в корневой папке проекта создайте файл .env, где создадите следующие переменные и зададите им свои значения:
```.env
POSTGRES_USER=''
POSTGRES_PASSWORD=''
POSTGRES_DB=''
TOKEN = 'Ваш токен телеграмм бота'
URL = "postgresql://Имя_пользователя:Пароль@my_db:5432/База_данных"
```
Убедитесь что вы терминал открыт в корневой папке проекта
Далее введите в терминал: `docker-compose up --build` <br/>
Интерфейс бота должен быть понятен <br/>
При вводе количества значений вы можете вручную ввести 0, тогда спарсятся все доступные вакансии/резюме, но помните, что это может занять очень продолжительное время
**/resume**
1.Все параметры находятся в Enum, заведомо неправильно введенный параметр даст отрицательный ответ сервера
Введем во все возможные парметры "Пропустить", ожидаем увидеть json следующего вида:
``` python
{"status": "success",
"data": result_list,
"details": None}
```
![image](https://github.com/myDanik/ParserHH/assets/146641293/88abab51-4b41-4b02-8ca1-ded3dd99240f)
![image](https://github.com/myDanik/ParserHH/assets/146641293/543fc496-d30b-47a5-b8a4-b059d13c9872)
Его и получаем
2.Введем случайные парметры
![image](https://github.com/myDanik/ParserHH/assets/146641293/eeca27cc-6de6-48d8-b5db-19ba3ae2ab2c)
Получаем
![image](https://github.com/myDanik/ParserHH/assets/146641293/e32d587d-685c-4856-9ccc-e376410afa69)
3.Введем параметры, совокупность которых не даст подходящих резюме
![image](https://github.com/myDanik/ParserHH/assets/146641293/bd7cdd9a-4e13-4657-abbd-1e4256a99b01)
Ответ(парсинг по этой [ссылке](https://hh.ru/search/resume?isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&hhtmFrom=vacancy_search_list&hhtmFromLabel=resume_search_line&search_period=0&order_by=relevance&filter_exp_period=all_time&relocation=living_or_relocation&gender=female&area=113&job_search_status=active_search&job_search_status_changed_by_user=true&employment=volunteer&schedule=flyInFlyOut&experience=noExperience&education_level=doctor&text=повар)):
![image](https://github.com/myDanik/ParserHH/assets/146641293/cce1969a-029f-48e0-94e9-175219e6e779)


