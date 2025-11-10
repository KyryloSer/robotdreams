from lec02.hw.job1.dal import local_disk, sales_api


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
    """
    Retrieve sales data for a given date and save it to local storage.
    Parameters
    ----------
    date : str
        Sales date in format "YYYY-MM-DD".
    raw_dir : str
        Path to the target directory where the data should be saved.
        Example: "/path/to/storage/raw/sales/2022-08-09"

    Returns
    -------
    None
        The function does not return anything. If no sales data found,
        nothing will be saved.
    """
    sales = sales_api.get_sales(date)
    if not sales:
        print("No sales data from API")
        return
    local_disk.save_to_disk(path=raw_dir, json_content=sales)
