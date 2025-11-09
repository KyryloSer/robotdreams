import json
from typing import Any, Dict, List

from lec02.utils.prepare_dir import prepare_dir


def save_to_disk(json_content: List[Dict[str, Any]], path: str) -> None:
    path = prepare_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(json_content, f, indent=4)
