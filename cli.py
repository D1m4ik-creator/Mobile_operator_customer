from system import MobileOperatorSystem


MENU = """
╔══════════════════════════════════════════════════════════╗
║ 1. Добавить клиента     |  7. Добавить SIM               ║
║ 2. Удалить клиента      |  8. Удалить SIM                ║
║ 3. Все клиенты          |  9. Все SIM-карты              ║
║ 4. Очистить клиентов    | 10. Очистить SIM-карты         ║
║ 5. Поиск по паспорту    | 11. Поиск по № SIM             ║
║ 6. Поиск по фрагменту   | 12. Поиск по тарифу            ║
╠═════════════════════════╩════════════════════════════════╣
║ 13. Выдать SIM | 14. Вернуть SIM | 15. Список выдачи     ║
╚══════════════════════════════════════════════════════════╝
0. Выход
> """


def print_items(items, empty_message="Список пуст"):
    print("\n".join(str(item) for item in items) or empty_message)


def ask_test_data(system):
    choice = input("Добавить тестовые данные? (1 - да, 0 - нет): ").strip().lstrip("\ufeff")
    if choice == "1":
        clients_count, sims_count, issues_count = system.load_test_data()
        print(
            "Тестовые данные добавлены: "
            f"клиентов - {clients_count}, SIM-карт - {sims_count}, выдач - {issues_count}."
        )
    else:
        print("Запуск без тестовых данных.")


def add_client(system):
    print(
        system.add_client(
            input("Паспорт (NNNN-NNNNNN): "),
            input("Дата/место: "),
            input("ФИО: "),
            input("Год: "),
            input("Адрес: "),
        )
    )


def add_sim(system):
    print(
        system.add_sim(
            input("SIM (NNN-NNNNNNN): "),
            input("Тариф: "),
            input("Год: "),
        )
    )


def issue_sim(system):
    print(
        system.issue_sim(
            input("Паспорт: "),
            input("SIM: "),
            input("Дата выдачи: "),
            input("Действует до: "),
        )
    )


def run():
    system = MobileOperatorSystem()
    ask_test_data(system)

    actions = {
        "1": lambda: add_client(system),
        "2": lambda: print(system.delete_client(input("Паспорт: "))),
        "3": lambda: print_items(system.get_clients()),
        "4": lambda: (system.clear_clients(), print("Данные клиентов очищены")),
        "5": lambda: print(system.find_client(input("Паспорт: ")) or "Клиент не найден"),
        "6": lambda: print_items(
            system.find_clients_by_fragment(input("Фрагмент: ")),
            "Совпадений нет",
        ),
        "7": lambda: add_sim(system),
        "8": lambda: print(system.delete_sim(input("SIM: "))),
        "9": lambda: print_items(system.get_sims()),
        "10": lambda: (system.clear_sims(), print("Данные SIM-карт очищены")),
        "11": lambda: print(system.find_sim(input("SIM: ")) or "SIM-карта не найдена"),
        "12": lambda: print_items(
            system.find_sims_by_tariff(input("Тариф: ")),
            "Совпадений нет",
        ),
        "13": lambda: issue_sim(system),
        "14": lambda: print(system.return_sim(input("Паспорт: "), input("SIM: "))),
        "15": lambda: print_items(system.get_issues()),
    }

    while True:
        choice = input(MENU).strip()
        if choice == "0":
            break

        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный пункт меню.")
