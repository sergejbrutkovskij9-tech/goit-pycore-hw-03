import re


def normalize_phone(phone_number):

    cleaned_number = re.sub(r"\D", "", phone_number)

    if cleaned_number.startswith("380"):
        normalized = "+" + cleaned_number

    elif cleaned_number.startswith("0"):
        normalized = "+38" + cleaned_number

    else:
        normalized = "+38" + cleaned_number

    return normalized


raw_numbers = [
    "067\\t123 4567",
    "(095) 234-5678\\n",
    "+380 44 123 4567",
    "380501234567",
    "    +38(050)123-32-34",
    "     0503451234",
    "(050)8889900",
    "38050-111-22-22",
    "38050 111 22 11   ",
]

sanitized_numbers = [normalize_phone(num) for num in raw_numbers]

print(sanitized_numbers)