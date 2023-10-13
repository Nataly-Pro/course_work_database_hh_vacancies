import psycopg2


class DBManager:

    def __init__(self, host, user, password, port, db_name):
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=db_name
        )

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и
        количество вакансий у каждой компании.
        """
        query = 'SELECT работодатель, количество_вакансий FROM employers'
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

            for row in cur.fetchall():
                print(f'Работодатель: {row[0]}, вакансий: {row[1]}')

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        """
        query = """SELECT e.работодатель, название_вакансии, зарплата, ссылка
            FROM vacancies AS v
            INNER JOIN employers AS e
            ON v.id_работодателя=e.id
        """
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

            for row in cur.fetchall():
                print(f'Работодатель: {row[0]}, вакансия: {row[1]}, '
                      f'зарплата: {row[2]}, ссылка: {row[3]}')

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям.
        """
        query = """SELECT e.работодатель, round(AVG(зарплата))
            AS средняя_зарплата
            FROM vacancies AS v
            JOIN employers AS e ON v.id_работодателя=e.id
            GROUP BY работодатель
            ORDER BY средняя_зарплата DESC
        """
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

            for row in cur.fetchall():
                list_row = list(row)
                if list_row[1] == 0E-20:
                    list_row[1] = 0
                print(f'Работодатель: {row[0]}, '
                      f'средняя зарплата: {list_row[1]}')

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий,
        у которых зарплата выше средней по всем вакансиям.
        """
        query = """SELECT название_вакансии, зарплата, ссылка
                    FROM vacancies
                    WHERE зарплата > (SELECT AVG(зарплата) FROM vacancies)
                    ORDER BY зарплата DESC
        """
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

            for row in cur.fetchall():
                print(f'Вакансия: {row[0]}, '
                      f'зарплата: {row[1]}, '
                      f'ссылка: {row[2]}')

    def get_vacancies_with_keyword(self, key_words):
        """Получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.
        """
        query = f"""SELECT название_вакансии, зарплата, ссылка FROM vacancies
                    WHERE название_вакансии LIKE '%{key_words}%'
        """
        with self.connection.cursor() as cur:
            cur.execute(query)
            self.connection.commit()

            for row in cur.fetchall():
                print(*row)

    def __del__(self):
        self.connection.close()
