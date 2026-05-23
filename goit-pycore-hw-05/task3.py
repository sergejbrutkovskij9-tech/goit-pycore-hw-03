import sys
from typing import Callable


def parse_log_line(line: str) -> dict:
    """Парсить один рядок логу у словник."""
    parts = line.strip().split(" ", 3)
    return {
        "date":    parts[0],
        "time":    parts[1],
        "level":   parts[2],
        "message": parts[3] if len(parts) > 3 else "",
    }


def load_logs(file_path: str) -> list:
    """Завантажує та парсить усі рядки лог-файлу."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [parse_log_line(line) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено.")
        sys.exit(1)
    except OSError as e:
        print(f"Помилка читання файлу: {e}")
        sys.exit(1)


def filter_logs_by_level(logs: list, level: str) -> list:
    """Повертає записи логу для заданого рівня (функціональний стиль)."""
    return list(filter(lambda log: log["level"] == level.upper(), logs))


def count_logs_by_level(logs: list) -> dict:
    """Підраховує кількість записів для кожного рівня логування."""
    counts = {}
    for log in logs:
        counts[log["level"]] = counts.get(log["level"], 0) + 1
    return counts


def display_log_counts(counts: dict) -> None:
    """Виводить статистику рівнів логування у вигляді таблиці."""
    col_w = 17
    print(f"{'Рівень логування':<{col_w}}| Кількість")
    print(f"{'-' * col_w}|----------")
    for level, count in counts.items():
        print(f"{level:<{col_w}}| {count}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_логу> [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]
    filter_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if filter_level:
        filtered = filter_logs_by_level(logs, filter_level)
        print(f"\nДеталі логів для рівня '{filter_level}':")
        if filtered:
            for log in filtered:
                print(f"{log['date']} {log['time']} - {log['message']}")
        else:
            print("Записів не знайдено.")


if __name__ == "__main__":
    main()