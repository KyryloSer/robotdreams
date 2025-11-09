import shutil
from pathlib import Path


def get_file_name(path: str) -> str:
    date_str = Path(path).name
    return f"sales_{date_str}.json"


def prepare_dir(path: str) -> Path:
    p = Path(path)

    p.mkdir(parents=True, exist_ok=True)

    for item in p.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    return p


def prepare_and_get_file_path(path: str) -> Path:
    directory = prepare_dir(path)
    file_name = get_file_name(path)
    return directory / file_name
