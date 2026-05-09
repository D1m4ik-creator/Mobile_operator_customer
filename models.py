import re


PASSPORT_PATTERN = re.compile(r"^\d{4}-\d{6}$")
SIM_PATTERN = re.compile(r"^\d{3}-\d{7}$")


class Client:
    def __init__(self, passport, passport_info, full_name, birth_year, address):
        if not PASSPORT_PATTERN.match(passport):
            raise ValueError("Формат: NNNN-NNNNNN")

        self.passport = passport
        self.passport_info = passport_info
        self.full_name = full_name
        self.birth_year = int(birth_year)
        self.address = address

    def __str__(self):
        return f"{self.passport} | {self.full_name} | {self.address}"


class SIMCard:
    def __init__(self, number, tariff, issue_year, available=True):
        if not SIM_PATTERN.match(number):
            raise ValueError("Формат: NNN-NNNNNNN")

        self.number = number
        self.tariff = tariff
        self.issue_year = int(issue_year)
        self.available = available

    def __str__(self):
        status = "В наличии" if self.available else "Выдана"
        return f"{self.number} | {self.tariff} | {status}"


class IssueRecord:
    def __init__(self, passport, sim_number, issue_date, end_date):
        self.passport = passport
        self.sim_number = sim_number
        self.issue_date = issue_date
        self.end_date = end_date

    def __str__(self):
        return f"Паспорт {self.passport} -> SIM {self.sim_number} (до {self.end_date})"
