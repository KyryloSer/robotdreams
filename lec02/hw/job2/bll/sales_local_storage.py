from lec02.hw.job2.dal import local_disk, sales_local_dir


def save_sales_to_local_disk_as_avro(stg_dir: str, raw_dir: str) -> None:
    """
    Convert previously downloaded sales data from JSON
    and save it into Avro format.

    Parameters
    ----------
    stg_dir : str
        Directory where Avro output should be written.
        Example: "/path/to/storage/stg/sales/2022-08-09"
    raw_dir : str
        Directory where JSON input is stored.
        Example: "/path/to/storage/raw/sales/2022-08-09"

    Returns
    -------
    None
        If no data exists in raw_dir, function does nothing.
    """
    sales = sales_local_dir.get_sales(raw_dir)
    if sales is None:
        print("No sales data on lacal storage")
        return
    local_disk.save_to_avro(path=stg_dir, records=sales)
