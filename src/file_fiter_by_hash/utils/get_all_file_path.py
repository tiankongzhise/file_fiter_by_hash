from functools import cache
import pathlib

@cache
def get_all_file_path(folder_path: pathlib.Path = None) -> list:
    """返回文件夹下所有文件的绝对路径组成的list"""
    file_path = []
    for item in folder_path.iterdir():
        if item.is_file():
            # 路径的文本表示
            file_path.append(item.as_posix())
        elif item.is_dir():
            file_path.extend(get_all_file_path(item))
    return file_path
