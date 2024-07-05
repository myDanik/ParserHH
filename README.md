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
**/resume**<br/>
1.Параметры находятся в Enum, заведомо неправильно введенный параметр даст отрицательный ответ сервера<br/>
Введем во все возможные парметры "Пропустить", ожидаем увидеть json следующего вида:<br/>
``` python
{"status": "success",
"data": result_list,
"details": None}
```
![image](https://github.com/myDanik/ParserHH/assets/146641293/88abab51-4b41-4b02-8ca1-ded3dd99240f)<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/543fc496-d30b-47a5-b8a4-b059d13c9872)<br/>
Его и получаем<br/>
2.Введем случайные парметры<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/eeca27cc-6de6-48d8-b5db-19ba3ae2ab2c)<br/>
Получаем<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/e32d587d-685c-4856-9ccc-e376410afa69)<br/>
3.Введем параметры, совокупность которых не даст подходящих резюме<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/bd7cdd9a-4e13-4657-abbd-1e4256a99b01)<br/>
Ответ(парсинг по этой [ссылке](https://hh.ru/search/resume?isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&hhtmFrom=vacancy_search_list&hhtmFromLabel=resume_search_line&search_period=0&order_by=relevance&filter_exp_period=all_time&relocation=living_or_relocation&gender=female&area=113&job_search_status=active_search&job_search_status_changed_by_user=true&employment=volunteer&schedule=flyInFlyOut&experience=noExperience&education_level=doctor&text=повар)):
![image](https://github.com/myDanik/ParserHH/assets/146641293/cce1969a-029f-48e0-94e9-175219e6e779)<br/>
**/vacancy**<br/>
1. Параметры так же в Enum, каждый удачный ответ выглядит следующим образом<br/>
``` python
{"status": "success",
"data": result_list,
"details": None}
```
Введем во все возможные парметры "Пропустить"<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/89eeffcc-862f-4e44-b986-690257639aa2)<br/>
Получаем нужный json<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/7aa9bdf8-73c0-43bc-bdb6-6a1d8d956bf7)<br/>
2.Введем случайные параметры<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/95da678b-7c32-470b-8898-2a1de5a635cd)<br/>
Получим ожидаемый ответ:<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/0a8eaf9e-7c9f-4a00-9b86-35c6c8f688ab)<br/>
3.Введем значение не приводящие к существующим вакансиям:<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/32846ea2-9e2b-4ac2-bb95-298065910bc9)<br/>
Ожидаемый ответ c пустым списком([ccылка](https://hh.ru/search/vacancy?hhtmFrom=main&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&L_save_area=true&area=113&education=higher&part_time=start_after_sixteen&experience=noExperience&schedule=flexible&text=Rust_senior&page=0)):<br/>
![image](https://github.com/myDanik/ParserHH/assets/146641293/1e799b12-9808-4d64-9470-f0f61724f395)<br/>









