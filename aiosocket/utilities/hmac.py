import hmac
import hashlib
import base64
import json

from datetime import datetime, timezone
from typing import Dict, Any


def verify_hmac(key: bytes, data: bytes, provided_hmac: str) -> bool:
    provided_hmac_bytes = base64.b64decode(provided_hmac)
    generated_hmac = hmac.new(key, data, hashlib.sha256).digest()
    return hmac.compare_digest(provided_hmac_bytes, generated_hmac)


def validate_message(
    key: bytes, received_message: Dict[str, Any], max_age_seconds: int = 5
) -> bool:

    provided_hmac = received_message.pop("hmac", None)
    if not provided_hmac:
        return False

    timestamp_str = received_message.get("timestamp")
    if not timestamp_str:
        return False

    try:
        message_time = datetime.fromisoformat(timestamp_str).replace(
            tzinfo=timezone.utc
        )

        current_time = datetime.now(timezone.utc)
        time_difference = (current_time - message_time).total_seconds()

        if time_difference > max_age_seconds:
            return False

    except ValueError:
        return False

    json_data = json.dumps(received_message, separators=(",", ":"))
    data_to_sign = json_data.encode("utf-8")

    if verify_hmac(key, data_to_sign, provided_hmac):
        return True
    else:
        return False
