import requests
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
        try:
            response = requests.get(url, params)
        except requests.exceptions.RequestException as er:
            print("Exception request")
            print(er.args[0])
            break
        else:
            data = response.json()
            for employer in data['items']:
                if employer['id'] not in id_list:
                    id_list.append(employer)
                    employers_list.append(employer)
                else:
                    continue
            sleep(0.25)
    return employers_list


def get_vacancies(employers: list[dict]) -> list[dict]:
    """Запрашивает по API Headhunter информацию о вакансиях по
    ID работодателя,
    возвращает данные в виде списка словарей.
    """
    url = "https://api.hh.ru/vacancies"
    vacancies_list = []

    for employer in employers:
        for page in range(10):
            params = {
                'employer_id': employer['id'],
                'area': '113',
                'page': page,
                'per_page': 100,
            }
            try:
                response = requests.get(url, params)
                data = response.json()
                if not data['items']:
                    break
                else:
                    vacancies_list.extend(data['items'])
            except requests.exceptions.RequestException as er:
                print("Exception request\n", er.args[0])
                break

    return vacancies_list
