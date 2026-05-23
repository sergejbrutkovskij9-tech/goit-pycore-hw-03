import re
from typing import Callable, Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Генератор, що знаходить усі дійсні числа в тексті.
    Числа мають бути відокремлені пробілами з обох боків.
    """
    pattern = r'(?<= )\d+\.\d+(?= )|(?<= )\d+(?= )'
    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable) -> float:
    """
    Підраховує загальну суму всіх дійсних чисел у тексті,
    використовуючи переданий генератор func.
    """
    return sum(func(text))


# Приклад використання
text = (
    "Загальний дохід працівника складається з декількох частин: "
    "1000.01 як основний дохід, доповнений додатковими надходженнями "
    "27.45 і 324.00 доларів."
)

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")  # Загальний дохід: 1351.46