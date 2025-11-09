import shutil
from pathlib import Path


def prepare_dir(path: str) -> Path:
    p = Path(path)

    p.mkdir(parents=True, exist_ok=True)

    for item in p.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()

    return p
