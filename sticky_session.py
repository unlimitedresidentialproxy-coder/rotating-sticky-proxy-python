import os
import secrets
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


def build_sticky_username(base_username: str, session_id: str) -> str:
    """
    Replace this generic placeholder with the sticky-session username
    syntax documented for your gateway account.
    """
    return f"{base_username}-session-{session_id}"


def proxy_url(username: str) -> str:
    return (
        f"http://{username}:{PROXY_PASS}"
        f"@{PROXY_HOST}:{PROXY_PORT}"
    )


def get_with_backoff(
    session: requests.Session,
    url: str,
    proxies: dict[str, str],
) -> Response:
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            response = session.get(
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
    session_id = secrets.token_hex(6)
    sticky_username = build_sticky_username(
        PROXY_USER,
        session_id,
    )
    sticky_proxy = proxy_url(sticky_username)
    proxies = {
        "http": sticky_proxy,
        "https": sticky_proxy,
    }

    with requests.Session() as session:
        for step in range(1, 6):
            response = get_with_backoff(
                session,
                CHECK_URL,
                proxies,
            )
            payload: dict[str, Any] = response.json()
            print(
                f"Step {step}, session {session_id}: "
                f"{payload.get('origin', 'unknown')}"
            )


if __name__ == "__main__":
    main()
