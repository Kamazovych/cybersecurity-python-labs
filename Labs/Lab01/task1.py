import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import STUDENT_NAME, VARIANT_NUMBER


def analyze_passwords():
    passwords = [
        "Social@Engineer",
        "basic",
        "Phishing@D3tect",
        "client",
        "Ransomwar3@Protect",
        "general",
        "Zero@D4y",
        "generic",
        "Bug@Bounty",
        "standard123",
    ]
    criteria = {
        "min_length": 11,
        "require_digits": True,
        "require_upper": True,
        "require_special": True,
    }
    forbidden_passwords = {
        "basic",
        "client",
        "general",
        "generic",
        "standard123",
        "guest",
    }

    for _ in range(3):
        random_index = random.randint(0, len(passwords) - 1)
        passwords.append(passwords[random_index])

    print(f"Аналіз паролів для: {STUDENT_NAME} (Варіант {VARIANT_NUMBER})")

    for pwd in passwords:
        length_ok = len(pwd) >= criteria["min_length"]
        has_digit = any(char.isdigit() for char in pwd)
        has_upper = any(char.isupper() for char in pwd)
        has_lower = any(char.islower() for char in pwd)
        has_special = any(not char.isalnum() for char in pwd)

        criteria_met = sum([has_digit, has_upper, has_lower, has_special])
        is_unique = passwords.count(pwd) == 1

        if pwd in forbidden_passwords or not length_ok:
            status = "Заборонений"
        elif criteria_met == 4 and len(pwd) >= criteria["min_length"] + 4 and is_unique:
            status = "Дуже сильний"
        elif criteria_met == 4:
            status = "Сильний"
        elif criteria_met > 1:
            status = "Середній"
        else:
            status = "Слабкий"

        print(f"Пароль: {pwd:<20} | Статус: {status}")


if __name__ == "__main__":
    analyze_passwords()
