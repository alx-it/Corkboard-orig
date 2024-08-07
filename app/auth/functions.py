import hashlib
import hmac
import time

from app.auth.exceptions import TelegramDataError, TelegramDataIsOutdated
from app.auth.schemas import TelegramAuth


def validate_telegram_data(bot_token: str, data: TelegramAuth) -> dict:
    data = data.model_dump()

    print(f"Auth request data: {data}")
    received_hash = data.pop("hash", None)
    auth_date = data.get("auth_date")

    if _verify_telegram_session_outdate(auth_date):
        raise TelegramDataIsOutdated("Telegram authentication session is expired.")

    generated_hash = _generate_hash(data, bot_token)

    if generated_hash != received_hash:
        raise TelegramDataError("Request data is incorrect")

    return data


def _verify_telegram_session_outdate(auth_date: str) -> bool:
    one_day_in_second = 86400
    unix_time_now = int(time.time())
    unix_time_auth_date = int(auth_date)
    timedelta = unix_time_now - unix_time_auth_date

    if timedelta > one_day_in_second:
        return True
    return False


def _generate_hash(data: dict, token: str) -> str:
    request_data_alpha_sorted = sorted(data.items(), key=lambda v: v[0])
    print(f"generate_hash request_data_alpha_sorted: {request_data_alpha_sorted}")

    data_check_string = "\n".join(
        f"{key}={value}" for key, value in request_data_alpha_sorted
    )

    secret_key = hashlib.sha256(token.encode()).digest()
    generated_hash = hmac.new(
        key=secret_key, msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()

    return generated_hash
