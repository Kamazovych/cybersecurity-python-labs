import csv
import hashlib
import json
import os
from datetime import datetime, timezone


class ValidationError(Exception):
    pass


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
LOG_JSON = os.path.join(DATA_DIR, "log.json")


def log_event(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            status = "success" if result else "failure"
        except Exception as e:
            status = "failure"
            raise 
        finally:
            log_entry = {
                "event": func.__name__,
                "user": args[0] if args else "unknown",
                "result": status,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
                "args": args,
                "kwargs": kwargs,
            }
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(LOG_JSON, "a", encoding="utf-8") as f:
                json.dump(log_entry, f)
                f.write("\n")
        return result

    return wrapper


def generate_hash(password: str, salt: str = "00000") -> str:
    if not password or not salt:
        raise ValueError("Пароль або сіль не можуть бути порожніми")
    if len(password) < 10:
        raise ValidationError("Пароль надто короткий. Мінімум 10 символів.")

    combined = password + salt
    return hashlib.sha3_384(combined.encode()).hexdigest()


def create_user(username, password):
    my_salt = "00010"
    hash_value = generate_hash(password, my_salt)
    return (username, hash_value)


def create_users(users_list):
    os.makedirs(DATA_DIR, exist_ok=True)
    try:
        with open(USERS_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash"])
            for u, p in users_list:
                try:
                    writer.writerow(create_user(u, p))
                except (ValueError, ValidationError) as e:
                    print(f"Помилка створення {u}: {e}")
        print("Базу даних успішно створено.")
    except (OSError, PermissionError) as e:
        print(f"Помилка запису у файл: {e}")


@log_event
def login(username: str, password: str) -> bool:
    if not username or not password:
        raise ValueError("Логін і пароль обов'язкові")

    my_salt = "00010"
    try:
        input_hash = generate_hash(password, my_salt)
        with open(USERS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["username"] == username and row["password_hash"] == input_hash:
                    return True
        return False
    except FileNotFoundError:
        print("Базу даних не знайдено!")
        return False
    except ValidationError as e:
        print(f"Помилка валідації при вході: {e}")
        return False


def run_task3():
    users_to_register = [
        ("admin", "SuperSecret123"),
        ("vladyslav", "MyLancerPassword10"),
        ("user3", "Password12345"),
        ("user4", "SecurePass2026"),
        ("user5", "CyberSecurity!"),
        ("user6", "StrongHash999"),
        ("user7", "QWERTYuiop12"),
        ("user8", "Zxcvbnm12345"),
        ("user9", "LvivPolytech24"),
        ("user10", "GeometryDashXX"),
    ]

    create_users(users_to_register)

    print("\n--- База користувачів ---")
    try:
        with open(USERS_CSV, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                print(f"{row[0]:<15} | {row[1]}")
    except FileNotFoundError:
        pass

    print("\n--- Спроби входу ---")
    print(f"Вхід admin: {login('admin', 'SuperSecret123')}")
    print(f"Вхід vladyslav (невірний пароль): {login('vladyslav', 'WrongPassword10')}")


if __name__ == "__main__":
    run_task3()
