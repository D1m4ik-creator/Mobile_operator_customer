from fixtures import TEST_CLIENTS, TEST_ISSUES, TEST_SIMS
from models import Client, IssueRecord, SIMCard
from structures import AVLTree, HashTableSIM, IssueList


class MobileOperatorSystem:
    def __init__(self):
        self.clients = AVLTree()
        self.sims = HashTableSIM()
        self.issues = IssueList()

    def load_test_data(self):
        added_clients = sum(1 for client in TEST_CLIENTS if self.add_client(*client) == "OK")
        added_sims = sum(1 for sim in TEST_SIMS if self.add_sim(*sim) == "OK")
        issued_sims = sum(1 for issue in TEST_ISSUES if self.issue_sim(*issue) == "Успешно выдано.")
        return added_clients, added_sims, issued_sims

    def add_client(self, passport, passport_info, full_name, birth_year, address):
        try:
            client = Client(passport, passport_info, full_name, birth_year, address)
        except ValueError as error:
            return f"Ошибка: {error}"

        if self.clients.insert(client.passport, client):
            return "OK"
        return "Ошибка: Дубликат паспорта."

    def delete_client(self, passport):
        if self.issues.find_by_passport(passport):
            return "Ошибка: У клиента есть активные SIM."
        if self.clients.delete(passport):
            return "OK"
        return "Ошибка: Клиент не найден."

    def clear_clients(self):
        self.clients.clear()

    def get_clients(self):
        return self.clients.preorder()

    def find_client(self, passport):
        return self.clients.search(passport)

    def find_clients_by_fragment(self, fragment):
        return self.clients.find_clients_by_fragment(fragment)

    def add_sim(self, number, tariff, issue_year):
        try:
            sim = SIMCard(number, tariff, issue_year)
        except ValueError as error:
            return f"Ошибка: {error}"

        if self.sims.insert(sim):
            return "OK"
        return "Ошибка: Дубликат SIM."

    def delete_sim(self, sim_number):
        if self.issues.find_by_sim(sim_number):
            return "Ошибка: SIM числится выданной."
        if self.sims.delete(sim_number):
            return "OK"
        return "Ошибка: SIM не найдена."

    def clear_sims(self):
        self.sims.clear()

    def get_sims(self):
        return self.sims.get_all()

    def find_sim(self, sim_number):
        return self.sims.search(sim_number)

    def find_sims_by_tariff(self, tariff):
        return self.sims.search_by_tariff(tariff)

    def issue_sim(self, passport, sim_number, issue_date, end_date):
        if not self.clients.search(passport):
            return "Ошибка: Клиент не найден."

        sim = self.sims.search(sim_number)
        if sim is None or not sim.available:
            return "Ошибка: SIM не найдена или уже выдана."

        sim.available = False
        self.issues.insert_sorted(IssueRecord(passport, sim_number, issue_date, end_date))
        return "Успешно выдано."

    def return_sim(self, passport, sim_number):
        sim = self.sims.search(sim_number)
        if self.issues.delete(passport, sim_number) and sim:
            sim.available = True
            return "Успешно возвращено."
        return "Ошибка: Запись о выдаче не найдена."

    def get_issues(self):
        return self.issues.get_all()
