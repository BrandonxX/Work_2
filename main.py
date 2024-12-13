import re


class Income:
    def __init__(self, date=None, source=None, amount=None):
        self.date = date
        self.source = source
        self.amount = amount

    def __str__(self):
        return f"Дата: {self.date}, Источник: {self.source}, Сумма: {self.amount} руб."

    def __lt__(self, other):
        # Сравнение для сортировки: сначала по дате, затем по сумме
        if self.date == other.date:
            return self.amount < other.amount
        return self.date < other.date


def parse_income(input_str):
    # Используем регулярное выражение для поиска всех частей
    pattern = r'(?P<date>\d{4}\.\d{2}\.\d{2})|(?P<source>"[^"]*")|(?P<amount>\d+)'

    matches = re.findall(pattern, input_str)

    # Инициализируем переменные
    date = None
    source = None
    amount = None

    for match in matches:
        if match[0]:  # Если найдена дата
            date = match[0]
        if match[1]:  # Если найден источник
            source = match[1][1:-1]  # Удаляем кавычки
        if match[2]:  # Если найдена сумма
            amount = int(match[2])

    # Проверяем, что все необходимые поля заполнены
    if date and source and amount is not None:
        return Income(date, source, amount)
    else:
        return None


def read_incomes_from_file(file_path):
    incomes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                income = parse_income(line)
                if income:
                    incomes.append(income)
                else:
                    print(f"Некорректный ввод: {line}")
    return incomes


if __name__ == "__main__":
    file_path = 'incomes.txt'  # Укажите путь к вашему файлу
    incomes = read_incomes_from_file(file_path)

    # Сортировка по дате и сумме
    incomes_sorted = sorted(incomes)

    for income in incomes_sorted:
        print(income)
