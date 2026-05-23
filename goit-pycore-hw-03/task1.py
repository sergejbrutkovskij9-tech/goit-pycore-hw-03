from datetime import datetime


def get_days_from_today(date):
    try:
        input_date = datetime.strptime(date, "%Y-%m-%d").date()
        today = datetime.today().date()

        difference = today - input_date

        return difference.days

    except ValueError:
        return "Неправильний формат дати"


print(get_days_from_today("2025-10-09"))