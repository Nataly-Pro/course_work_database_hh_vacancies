import requests
import csv
from time import sleep


def get_employers_by_names(names: list[str]) -> list[dict]:
    """Запрашивает по API Headhunter информацию о работодателях
    по переданным названиям,
    возвращает данные в виде списка словарей.
    """
    url = "https://api.hh.ru/employers"
    id_list = []
    employers_list = []

    for name in names:
        params = {
            'text': name,
            'area': '113',
            'only_with_vacancies': True,
        }
        response = requests.get(url, params)
        data = response.json()
        for employer in data['items']:
            if employer['id'] not in id_list:
                id_list.append(employer)
                employers_list.append(employer)
            else:
                continue
        sleep(0.25)

    return employers_list


def get_vacancies_by_employers_names(employers: list[dict]) -> list[dict]:
    """Запрашивает по API Headhunter информацию о вакансиях по
    ID работодателя,
    возвращает данные в виде списка словарей.
    """
    url = "https://api.hh.ru/vacancies"
    vacancies_list = []

    for employer in employers:
        for page in range(5):
            params = {
                'employer_id': employer['id'],
                'area': '113',
                'page': page,
                'per_page': 100,
            }
            response = requests.get(url, params)
            data = response.json()
            if not data['items']:
                break
            else:
                vacancies_list.extend(data['items'])
    return vacancies_list


def get_employers_from_file(filename) -> list[dict]:
    """Получает ID компании из csv-файла,
    передает его в URL запроса по API hh.ru,
    получает данные о компании-работодателе в виде словаря python.
    Возвращает список словарей.
    """
    url = "https://api.hh.ru/employers/"
    employers_list = []

    with open(filename, 'r', encoding='utf-8') as file:
        employers = csv.DictReader(file)
        for row in employers:
            response = requests.get(url+row['ID'])
            data = response.json()
            employers_list.append(data)
            sleep(0.25)
    return employers_list


def get_vacancies_by_id_from_file(filename) -> list[dict]:
    """Получает ID компании из csv-файла,
    передает его в параметры запроса по API hh.ru,
    получает данные о вакансиях работодателя в виде словаря.
    Возвращает список словарей.
    """

    url = "https://api.hh.ru/vacancies"
    vacancies_list = []

    with open(filename, 'r', encoding='utf-8') as file:
        employers = csv.DictReader(file)
        for row in employers:
            for page in range(5):
                params = {
                    'employer_id': row['ID'],
                    'area': '113',
                    'page': page,
                    'per_page': 100,
                }
                response = requests.get(url, params)
                data = response.json()
                if not data['items']:
                    break
                else:
                    vacancies_list.extend(data['items'])
    return vacancies_list
