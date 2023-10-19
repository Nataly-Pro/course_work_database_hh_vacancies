from funcs import get_employers_by_names, get_vacancies_by_employers_names, \
    get_employers_from_file, get_vacancies_by_id_from_file
from DBManager import DBManager


def main():

    user_choice = input('Выберите вариант поиска вакансий:\n'
                        '1 - по указанным Вами компаниям, \n'
                        '2 - среди 11 лучших IT-компаний по рейтингу Хабр Карьеры:\n')
    if user_choice == '1':
        employer_names = input('Введите названия интересующих вас компаний '
                               'через запятую: ').strip().split(', ')

        employers = get_employers_by_names(employer_names)
        vacancies = get_vacancies_by_employers_names(employers)

    elif user_choice == '2':
        employers = get_employers_from_file('employers.csv')
        vacancies = get_vacancies_by_id_from_file('employers.csv')

    db_manager = DBManager('hh_vacancies')
    db_manager.create_database()
    print(f"БД hh_vacancies успешно создана")

    db_manager.create_table_employers()
    print("Таблица employers успешно создана")

    db_manager.create_table_vacancies()
    print("Таблица vacancies успешно создана")

    db_manager.add_employers_to_db(employers)
    print("Таблица employers успешно заполнена")

    db_manager.add_vacancies_to_db(vacancies)
    print("Таблица vacancies успешно заполнена")

    while True:
        print()
        user_choice = input('Выберите дальнейшее действие:\n'
                            '1 - Показать найденных работодателей и их вакансии,\n'
                            '2 - Показать все найденные вакансии,\n'
                            '3 - Вывести среднюю зарплату по вакансиям,\n'
                            '4 - Показать вакансии с зарплатой выше средней,\n'
                            '5 - Вывести вакансии по ключевому слову в названии,\n'
                            '0 - Выйти\n')
        if user_choice == '1':
            db_manager.get_companies_and_vacancies_count()
        elif user_choice == '2':
            db_manager.get_all_vacancies()
        elif user_choice == '3':
            db_manager.get_avg_salary()
        elif user_choice == '4':
            db_manager.get_vacancies_with_higher_salary()
        elif user_choice == '5':
            key_word = input('Ключевое слово для поиска вакансий: ')
            db_manager.get_vacancies_with_keyword(key_word)
        elif user_choice == '0':
            break


if __name__ == '__main__':
    main()

