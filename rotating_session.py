import os
import time
from typing import Any

import requests
from requests import Response
from requests.exceptions import RequestException

PROXY_HOST = os.environ["PROXY_HOST"]
PROXY_PORT = os.getenv("PROXY_PORT", "7777")
PROXY_USER = os.environ["PROXY_USER"]
PROXY_PASS = os.environ["PROXY_PASS"]

CHECK_URL = "https://httpbin.org/ip"
MAX_ATTEMPTS = 4


def proxy_url(username: str) -> str:
    return (
        f"http://{username}:{PROXY_PASS}"
        f"@{PROXY_HOST}:{PROXY_PORT}"
    )


def get_with_backoff(url: str) -> Response:
    proxies = {
        "http": proxy_url(PROXY_USER),
        "https": proxy_url(PROXY_USER),
    }

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = requests.get(
                url,
                proxies=proxies,
                timeout=(5, 20),
            )
            response.raise_for_status()
            return response
        except RequestException:
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(2 ** (attempt - 1))

    raise RuntimeError("Unreachable")


def main() -> None:
    for request_number in range(1, 6):
        response = get_with_backoff(CHECK_URL)
        payload: dict[str, Any] = response.json()
        print(
            f"Request {request_number}: "
            f"{payload.get('origin', 'unknown')}"
        )


if __name__ == "__main__":
    main()
