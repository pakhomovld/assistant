import json
import time
import requests
import jwt
from threading import Lock

class TokenManager:
    def __init__(self, json_key_path):
        self.json_key_path = json_key_path
        self.lock = Lock()
        self.token = None
        self.expiry_time = 0

    def _generate_iam_token(self):
        with open(self.json_key_path, 'r', encoding='utf-8') as f:
            key_data = json.load(f)

        service_account_id = key_data["service_account_id"]
        private_key = key_data["private_key"]
        key_id = key_data["id"]

        now = int(time.time())
        payload = {
            "aud": "https://iam.api.cloud.yandex.net/iam/v1/tokens",
            "iss": service_account_id,
            "iat": now,
            "exp": now + 900  # JWT is valid for 15 minutes
        }

        headers = {"kid": key_id}
        token_jwt = jwt.encode(payload, private_key, algorithm="PS256", headers=headers)

        iam_url = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
        headers = {"Content-Type": "application/json"}
        response = requests.post(iam_url, headers=headers, json={"jwt": token_jwt})
        response.raise_for_status()

        response_data = response.json()
        self.token = response_data["iamToken"]
        self.expiry_time = now + 840  # Update expiry to 14 minutes (buffer of 1 minute)

    def get_token(self):
        with self.lock:
            now = int(time.time())
            if self.token is None or now >= self.expiry_time:
                self._generate_iam_token()
            return self.token

def get_iam_token(json_key_path: str) -> str:
    """
    Provides an IAM token, refreshing it automatically if it has expired.
    """
    token_manager = TokenManager(json_key_path)
    return token_manager.get_token()

# Example usage
if __name__ == "__main__":
    JSON_KEY_PATH = "path/to/your/json/key.json"
    token = get_iam_token(JSON_KEY_PATH)
    print("IAM Token:", token)
