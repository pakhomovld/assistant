import subprocess
from app.config import settings

def generate_iam_token():
    try:
        token = subprocess.check_output(["/root/yandex-cloud/bin/yc", "iam", "create-token"], stderr=subprocess.STDOUT).strip()
        return token.decode("utf-8")
    except FileNotFoundError:
        raise Exception("Команда 'yc' не найдена. Убедитесь, что Yandex CLI установлен и доступен в PATH.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка при генерации IAM-токена: {e.output.decode('utf-8')}")

def ensure_valid_iam_token(current_token):
    if current_token is None or token_has_expired():
        return generate_iam_token()
    return current_token

def token_has_expired():
    # Здесь должна быть проверка на истечение токена
    return False

