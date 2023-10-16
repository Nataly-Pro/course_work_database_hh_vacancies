from funcs import get_employers_by_names, get_vacancies
from DBManager import DBManager


def main():
    employer_names = input('Введите названия интересующих вас компаний '
                           'через запятую для поиска '
                           'их вакансий: ').strip().split(', ')

    employers = get_employers_by_names(employer_names)
    vacancies = get_vacancies(employers)

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

    user_choice = input('Выберите дальнейшее действие:\n'
                        '1 - Показать найденных работодателей и их вакансии,\n'
                        '2 - Показать вакансии с зарплатой выше средней,\n'
                        '3 - Вывести вакансии по ключевому слову в названии\n'
                        '0 - Выйти\n')
    if user_choice == '1':
        db_manager.get_companies_and_vacancies_count()
        db_manager.get_all_vacancies()
    elif user_choice == '2':
        db_manager.get_avg_salary()
        db_manager.get_vacancies_with_higher_salary()
    elif user_choice == '3':
        key_word = input('Ключевое слово для поиска вакансий: ')
        db_manager.get_vacancies_with_keyword(key_word)
    elif user_choice == '0':
        quit()


if __name__ == '__main__':
    main()

