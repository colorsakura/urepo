from typing import Union
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print(f"函数 {func.__name__} 运行时间：{run_time} 秒")
        return result

    return wrapper


def pretty_size(
    file_size: Union[str, int, float],
    units: list = [" B", " KB", " MB", " GB", " TB", " PB", " EB"],
) -> str:
    """Get human readable size, it keep two decimal places.
       For example, 12345 -> 12.06 KB.
       Ref: https://stackoverflow.com/a/43750422

    Args:
        file_size (float): File size.
        units (list, optional): List of size units. Defaults to
         [" B", " KB", " MB", " GB", " TB", " PB", " EB"].

    Returns:
        str: Human readable size.
    """
    return (
        "{:.1f}{}".format(float(file_size), units[0])
        if file_size < 1024
        else pretty_size(file_size / 1024, units[1:])
    )
