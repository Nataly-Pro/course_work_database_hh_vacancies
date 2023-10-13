import psycopg2
from config import config
from funcs import get_employers_by_names, get_vacancies, \
    create_table_employers, create_table_vacancies, \
    add_employers_to_db, add_vacancies_to_db
from DBManager import DBManager


def main():
    employer_names = ['Angels IT', 'Boxberry',
                      'AUXO (Атос АйТи Солюшенс энд Сервисез',
                      'BI.ZONE', 'Айтекс, Центр Информационных Технологий',
                      'DNS Головной офис',
                      'DNS Технологии', 'Днс Дом', 'MoneyCat', 'Владлинк',
                      'Томору']

    params = config()
    db_name = 'hh_vacancies'

    employers = get_employers_by_names(employer_names)
    vacancies = get_vacancies(employers)

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f'DROP DATABASE IF EXISTS {db_name}')
        cur.execute(f'CREATE DATABASE {db_name}')
    conn.close()
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            create_table_employers(cur)
            print("Таблица employers успешно создана")

            create_table_vacancies(cur)
            print("Таблица vacancies успешно создана")

            add_employers_to_db(cur, employers)
            print("Таблица employers успешно заполнена")

            add_vacancies_to_db(cur, vacancies)
            print("Таблица vacancies успешно заполнена")
    conn.close()


if __name__ == '__main__':
    main()
