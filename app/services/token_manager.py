import subprocess
import time
from app.config import settings

last_token_update = 0
TOKEN_LIFETIME = 3600  # время жизни токена в секундах (1 час)

def generate_iam_token():
    global last_token_update
    try:
        subprocess.run(
            ["yc", "config", "set", "token", settings.OAUTH_TOKEN],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        token = subprocess.check_output(
            ["yc", "iam", "create-token"],
            stderr=subprocess.STDOUT
        ).strip()
        last_token_update = time.time()  # обновляем время после генерации токена
        return token.decode("utf-8")
    except FileNotFoundError:
        raise Exception("Команда 'yc' не найдена. Убедитесь, что Yandex CLI установлен и доступен в PATH.")
    except subprocess.CalledProcessError as e:
        raise Exception(f"Ошибка при генерации IAM-токена: {e.output.decode('utf-8')}")

def token_has_expired():
    global last_token_update
    current_time = time.time()
    if current_time - last_token_update > TOKEN_LIFETIME:
        return True
    return False

def ensure_valid_iam_token(current_token):
    if current_token is None or token_has_expired():
        return generate_iam_token()
    return current_token
