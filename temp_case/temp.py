import pathlib
import datetime
from functools import cache

target_folder = pathlib.Path(r'C:\Users\hbc_thinkbook16\Documents\Tencent Files\2541600292')

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


def my_func(item:pathlib.Path):
    print(f'开始处理文件夹{item}')
    beg_time = datetime.datetime.now()
    temp_list = []
    item_count = 0
    folder_size = 0
    for temp in item.iterdir():
        if temp.is_file():
            temp_list.append(temp.as_posix())
        elif temp.is_dir():
            temp_list.extend(get_all_file_path(temp))
    for temp_item in temp_list:
        temp = pathlib.Path(temp_item)
        item_count += 1
        folder_size += temp.stat().st_size
    end_time = datetime.datetime.now()
    print(f'文件夹{item}下有{item_count}个文件，占用{folder_size}字节，耗时{end_time - beg_time}')
    return item_count, folder_size

def pathlib_func(item:pathlib.Path):
    print(f'开始处理文件夹{item}')
    beg_time = datetime.datetime.now()
    item_count = 0
    folder_size = 0
    for temp_item in item.rglob('*'):
        if temp_item.is_file():
            item_count += 1
            folder_size += temp_item.stat().st_size
    end_time = datetime.datetime.now()
    print(f'文件夹{item}下有{item_count}个文件，占用{folder_size}字节，耗时{end_time - beg_time}')
    return item_count, folder_size

if __name__ == '__main__':
    my_func(target_folder)
    pathlib_func(target_folder)
