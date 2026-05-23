import os

def total_salary(path):
    try:
        with open(path, encoding="utf-8") as file:
            salaries = []
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split(",")
                if len(parts) != 2:
                    raise ValueError(f"Рядок {line_num}: очікується формат 'Ім'я,Зарплата', отримано: '{line}'")

                name, salary_str = parts
                try:
                    salary = float(salary_str)
                except ValueError:
                    raise ValueError(f"Рядок {line_num}: '{salary_str}' не є числом")

                salaries.append(salary)

        if not salaries:
            return (0, 0)

        total = sum(salaries)
        average = total / len(salaries)
        return (total, average)

    except FileNotFoundError:
        print(f"Помилка: файл '{path}' не знайдено.")
        raise
    except ValueError as e:
        print(f"Помилка даних: {e}")
        raise


if __name__ == "__main__":
    # Шлях відносно розташування самого скрипта
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "salary_file.txt")

    # Створюємо тестовий файл, якщо він відсутній
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("Alex Korp,3000\nNikita Borisenko,2000\nSitarama Raju,1000\n")
        print(f"Створено тестовий файл: {file_path}")

    total, average = total_salary(file_path)
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")