import os
from typing import Any, Dict, List

import requests

API_URL = "https://fake-api-vycpfa6oca-uc.a.run.app/"


def get_sales(date: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: data retrieve the data from
    :return: list of records
    """
    auth_token = os.environ.get("AUTH_TOKEN")
    headers = {"Authorization": auth_token}

    result: List[Dict[str, Any]] = []
    page = 1
    while True:
        try:
            url = f"{API_URL}sales?date={date}&page={page}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            break

        try:
            data = response.json()
        except requests.JSONDecodeError:
            break

        if not data:
            break

        result.extend(data)
        page += 1

    return result
