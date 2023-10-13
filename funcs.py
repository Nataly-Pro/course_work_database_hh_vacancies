import requests
from time import sleep


def get_employers_by_names(names: list[str]) -> list[dict]:
    """Запрашивает по API Headhunter информацию о работодателях
    по переданным названиям,
    возвращает данные в виде списка словарей.
    """
    url = "https://api.hh.ru/employers"
    employers_list = []

    for name in names:
        params = {
            'text': name,
            'area': '113',  # Россия
            'only_with_vacancies': True,  # только с открытыми вакансиями
        }
        try:
            response = requests.get(url, params)
        except requests.exceptions.RequestException as er:
            print("Exception request")
            print(er.args[0])
            break
        else:
            data = response.json()
            employers_list.extend(data['items'])
            sleep(0.5)
    return employers_list


def get_vacancies(employers: list[dict]) -> list[dict]:
    """Запрашивает по API Headhunter информацию о вакансиях по
    ID работодателя,
    возвращает данные в виде списка словарей.
    """
    url = "https://api.hh.ru/vacancies"
    vacancies_list = []

    for employer in employers:
        params = {
            'employer_id': employer['id'],
            'area': '113',
        }
        try:
            response = requests.get(url, params)
            data = response.json()
            vacancies_list.extend(data['items'])
        except requests.exceptions.RequestException as er:
            print("Exception request\n", er.args[0])
            break

    return vacancies_list


def create_table_employers(cur):
    """Создаёт таблицу employers"""

    cur.execute("""
        CREATE TABLE employers (
        id varchar(10) PRIMARY KEY,
        работодатель varchar(70) NOT NULL,
        количество_вакансий INTEGER
        )
    """)


def create_table_vacancies(cur):
    """Создаёт таблицу vacancies."""

    cur.execute("""
        CREATE TABLE vacancies (
            id VARCHAR(10),
            название_вакансии VARCHAR(100),
            зарплата INTEGER,
            id_работодателя VARCHAR(10) REFERENCES employers (id),
            ссылка TEXT
            )
    """)


def add_employers_to_db(cur, employers_list: list[dict]) -> None:
    """Добавляет данные из employers_list в таблицу employers."""

    for employer in employers_list:
        cur.execute("""
            INSERT INTO employers (id, работодатель, количество_вакансий)
            VALUES (%s, %s, %s)
            """,
            (employer['id'], employer['name'], employer['open_vacancies'])
        )


def add_vacancies_to_db(cur, vacancies_list: list[dict]) -> None:
    """Добавляет данные из vacancies_list в таблицу vacancies."""

    for vacancy in vacancies_list:
        if vacancy['salary'] is None:
            salary = 0
        elif vacancy['salary']['from'] is None:
            salary = 0
        else:
            salary = int(vacancy['salary']['from'])

        cur.execute("""
            INSERT INTO vacancies (
            id, название_вакансии, зарплата,
            id_работодателя, ссылка)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (vacancy['id'],
             vacancy['name'],
             salary,
             vacancy['employer']['id'],
             vacancy['url'])
        )
