import psycopg2
from config import config


class DBManager:

    def __init__(self, db_name):
        self.db_name = db_name
        self.params = config()

    def create_database(self):
        """Создаёт базу данных"""
        conn = psycopg2.connect(database='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
        cur.execute(f'CREATE DATABASE {self.db_name}')
        conn.close()

    def create_table_employers(self):
        """Создаёт таблицу employers"""
        query = """
            CREATE TABLE employers 
            (
                id varchar(10) PRIMARY KEY,
                работодатель varchar(100) NOT NULL,
                количество_вакансий INTEGER
            )
        """
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
        conn.close()

    def create_table_vacancies(self):
        """Создаёт таблицу vacancies."""
        query = """CREATE TABLE vacancies 
            (
                id VARCHAR(10),
                название_вакансии VARCHAR(100),
                зарплата INTEGER,
                id_работодателя VARCHAR(10) REFERENCES employers (id),
                ссылка TEXT
            )
        """
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
        conn.close()

    def add_employers_to_db(self, employers_list: list[dict]) -> None:
        """Добавляет данные из employers_list в таблицу employers."""

        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                for employer in employers_list:
                    cur.execute("""INSERT INTO employers 
                        (id, работодатель, количество_вакансий)
                        VALUES (%s, %s, %s)""",
                        (employer['id'], employer['name'], employer['open_vacancies'])
                    )
        conn.close()

    def add_vacancies_to_db(self, vacancies_list: list[dict]) -> None:
        """Добавляет данные из vacancies_list в таблицу vacancies."""
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
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

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и
        количество вакансий у каждой компании.
        """
        query = 'SELECT работодатель, количество_вакансий FROM employers'
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                for row in cur.fetchall():
                    print(f'Работодатель: {row[0]}, вакансий: {row[1]}')
        conn.close()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = """SELECT e.работодатель, название_вакансии, зарплата, ссылка
            FROM vacancies AS v
            INNER JOIN employers AS e
            ON v.id_работодателя=e.id
        """
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                count = 0
                for row in cur.fetchall():
                    print(f'Работодатель: {row[0]}, вакансия: {row[1]}, '
                          f'зарплата(от): {row[2]}, ссылка: {row[3]}')
                    count += 1
                print(f'Найдено {count} вакансий')

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям.
        """
        query = """SELECT round(AVG(зарплата))
            AS средняя_зарплата
            FROM vacancies 
            WHERE зарплата <> 0
        """
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)

                print('Cредняя зарплата', *cur.fetchone())
        conn.close()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        """
        query = """SELECT e.работодатель, название_вакансии, зарплата, ссылка
                    FROM vacancies AS v
                    INNER JOIN employers AS e
                    ON v.id_работодателя=e.id
                    WHERE зарплата > (SELECT AVG(зарплата) FROM vacancies
                    WHERE зарплата <> 0)
                    ORDER BY зарплата DESC
        """
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                count = 0
                for row in cur.fetchall():
                    print(f'Работодатель: {row[0]}, '
                          f'Вакансия: {row[1]}, '
                          f'Зарплата(от): {row[2]}, '
                          f'Ссылка: {row[3]}')
                    count += 1
                print(f'Найдено {count} вакансий')

    def get_vacancies_with_keyword(self, key_word):
        """Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например 'python'.
        """
        query = f"""SELECT e.работодатель, название_вакансии, зарплата, ссылка 
                FROM vacancies AS v
                INNER JOIN employers AS e
                ON v.id_работодателя=e.id
                WHERE название_вакансии LIKE '%{key_word}%'
        """
        with psycopg2.connect(database=self.db_name, **self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                for row in cur.fetchall():
                    print(*row)
        conn.close()
