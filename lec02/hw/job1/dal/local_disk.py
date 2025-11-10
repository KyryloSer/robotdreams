import json
from typing import Any, Dict, List

from lec02.utils.file_utils import prepare_and_get_file_path


def save_to_disk(json_content: List[Dict[str, Any]], path: str) -> None:
    """
    Save sales data to a JSON file in the specified directory.

    Parameters
    ----------
    json_content : List[Dict[str, Any]]
        The list of records to be saved. Must be JSON-serializable.
    path : str
        Directory path where the file should be saved.
        Example: "/path/to/storage/raw/sales/2022-08-09"

    Returns
    -------
    None
        Writes a JSON file to disk and returns nothing.
    """
    file_path = prepare_and_get_file_path(path, extension="json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=4)
