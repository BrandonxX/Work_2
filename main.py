import re
from datetime import datetime
from collections import defaultdict


class Income:
    def __init__(self, date=None, source=None, amount=None):
        self.source = source
        self.date = date
        self.amount = amount

    def __str__(self):
        return f"Дата: {self.date}, Источник: {self.source}, Сумма: {self.amount} руб."


def parse_income(input_str):
    pattern = r'(?P<date>\d{4}\.\d{2}\.\d{2})|(?P<source>"[^"]*")|(?P<amount>\d+)'
    matches = re.findall(pattern, input_str)

    date, source, amount = None, None, None

    for match in matches:
        if match[0]:
            date = match[0]
        if match[1]:
            source = match[1][1:-1]
        if match[2]:
            amount = int(match[2])

    if date and source and amount is not None:
        return Income(date, source, amount)
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
    return incomes


def filter_incomes_by_source(incomes, source):
    return [income for income in incomes if income.source == source]


def aggregate_incomes(incomes):
    aggregated = defaultdict(int)
    for income in incomes:
        aggregated[income.source] += income.amount
    return aggregated


def get_top_sources(aggregated_incomes, top_n=3):
    return sorted(aggregated_incomes.items(), key=lambda x: x[1], reverse=True)[:top_n]


def sort_incomes(incomes):
    return sorted(incomes, key=lambda x: datetime.strptime(x.date, '%Y.%m.%d'))


if __name__ == "__main__":
    file_path = 'incomes.txt'  # Укажите путь к вашему файлу
    incomes = read_incomes_from_file(file_path)

    # Сортировка доходов по дате
    sorted_incomes = sort_incomes(incomes)

    # Вывод всех доходов перед началом фильтрации
    print("Все доходы (отсортированные):")
    for income in sorted_incomes:
        print(income)

    # Агрегация доходов по источникам
    aggregated_incomes = aggregate_incomes(sorted_incomes)

    # Вывод топ-3 источников
    top_sources = get_top_sources(aggregated_incomes)
    print("\nТоп-3 источника с наибольшими суммами:")
    for source, total in top_sources:
        print(f"Источник: '{source}', Общая сумма: {total} руб.")

    while True:
        source_to_filter = input("\nВведите источник для фильтрации (или 'стоп' для выхода): ")
        if source_to_filter.lower() == 'стоп':
            print("Программа завершена.")
            break

        filtered_incomes = filter_incomes_by_source(sorted_incomes, source_to_filter)

        if filtered_incomes:
            total_amount = sum(income.amount for income in filtered_incomes)
            print(f"Доходы из источника '{source_to_filter}':")
            for income in filtered_incomes:
                print(income)
            print(f"Общая сумма доходов из источника '{source_to_filter}': {total_amount} руб.")
        else:
            print(f"Нет доходов из источника '{source_to_filter}'.")