import json
from typing import Any, Dict, List

from lec02.utils.file_utils import prepare_and_get_file_path


def save_to_disk(json_content: List[Dict[str, Any]], path: str) -> None:
    file_path = prepare_and_get_file_path(path)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=4)
