import pathlib
import time
from functools import cache
folder_path = pathlib.Path(r"L:\动物行为学")
file_count = 0

def calculate_items(folder_path: pathlib.Path) -> int:
    """计算文件夹下所有文件和文件夹的数量"""
    item_count = 0
    for item in folder_path.iterdir():
        item_count += 1
    return item_count

# 递归计算文件夹内所有的文件数目 缓存结果
@cache
def calculate_files_recursively(folder_path: pathlib.Path) -> int:
    """递归计算文件夹内所有的文件数目"""
    file_path = []
    for item in folder_path.iterdir():
        if item.is_file():
            # 路径的文本表示
            file_path.append(item.as_posix())
        elif item.is_dir():
            print(f'count dir: {item.name}')
            file_path.extend(calculate_files_recursively(item))
            print(file_path)
    return {folder_path.name: file_path}


def test_calculate_items():
    total_to_test = calculate_items(folder_path)
    counted_number = 0
    files_number= 0
    folder_count_time_total = 0
    folder_count_time_average = 0
    folder_file_count_total = 0
    folder_number = 0
    total_file = 0
    all_path = {}
    for item in folder_path.iterdir():
        if item.is_file():
            all_path[item.name] = item.as_posix()
            
            print(f'is file: {item.name}')
            files_number += 1
        elif item.is_dir():
            print(f'is count dir: {item.name}')
            folder_number += 1
            time_start = time.time()
            file_count = calculate_files_recursively(item)
            all_path.update(file_count)
            time_end = time.time()
            count_time = round((time_end - time_start), 2)
            folder_count_time_total += count_time
            folder_file_count_total += len(file_count[item.name])
            average_time_count = round(count_time / (len(file_count[item.name]) or 1), 2)
            print(f'count dir: {item.name} file count: {len(file_count[item.name])} time: {count_time} s,avrage file cost time: {average_time_count} s')
    print(f'{total_file} files, count time: {folder_count_time_total} s, avrage time: {round(folder_count_time_total / folder_number, 2)} s')
    print(f'all_path: {len(all_path)}')
    for key, value in all_path.items():
        print(f'{key}: {len(value) if isinstance(value, list) else 1}')


if __name__ == '__main__':
    test_calculate_items()