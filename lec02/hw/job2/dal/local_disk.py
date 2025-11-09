from typing import Any, Dict, List

from fastavro import parse_schema, writer

from lec02.utils.file_utils import prepare_and_get_file_path

SALES_SCHEMA = {
    "type": "record",
    "name": "Sale",
    "namespace": "my.sales",
    "fields": [
        {"name": "client", "type": "string"},
        {"name": "purchase_date", "type": "string"},
        {"name": "product", "type": "string"},
        {"name": "price", "type": "int"},
    ],
}

PARSED_SCHEMA = parse_schema(SALES_SCHEMA)


def save_to_avro(records: List[Dict[str, Any]], path: str) -> None:
    """
    Save sales records to Avro format in the specified directory.

    Parameters
    ----------
    records : List[Dict[str, Any]]
        Sales records (must match the Avro schema).
    path : str
        Directory where the Avro file should be written.

    Returns
    -------
    None
    """
    file_path = prepare_and_get_file_path(path, extension="avro")
    with open(file_path, "wb") as out:
        writer(out, PARSED_SCHEMA, records)
