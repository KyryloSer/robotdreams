import json
from pathlib import Path
from typing import Any, Dict, List

from lec02.utils.file_utils import get_file_name


def get_sales(raw_dir: str) -> List[Dict[str, Any]]:
    """
    Get data from local directory sales for specified date.

    :param raw_dir: raw_dir path where save sales data is stored.
    :return: list of records
    """

    result: List[Dict[str, Any]] = []
    directory = Path(raw_dir)
    file_name = get_file_name(path=raw_dir, extension="json")
    if Path(directory / file_name).exists():
        with open(directory / file_name, "r", encoding="utf-8") as f:
            result = json.load(f)
    return result
