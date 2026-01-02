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
    file_count = 0
    for item in folder_path.iterdir():
        if item.is_file():
            file_count += 1
        elif item.is_dir():
            file_count += calculate_files_recursively(item)
    return file_count


def test_calculate_items():
    total_to_test = calculate_items(folder_path)
    counted_number = 0
    files_number= 0
    folder_count_time_total = 0
    folder_count_time_average = 0
    folder_file_count_total = 0
    folder_number = 0
    total_file = 0
    for item in folder_path.iterdir():
        if item.is_file():
            print(f'is file: {item.name}')
            total_file += 1
            files_number += 1
        elif item.is_dir():
            print(f'is count dir: {item.name}')
            folder_number += 1
            time_start = time.time()
            file_count = calculate_files_recursively(item)
            time_end = time.time()
            count_time = round((time_end - time_start), 2)
            folder_count_time_total += count_time
            total_file += file_count
            folder_file_count_total += file_count
            average_time_count = round(count_time / (file_count or 1), 2)
            print(f'count dir: {item.name} file count: {file_count} time: {count_time} s,avrage file cost time: {average_time_count} s')
        counted_number += 1
        print(f'{total_to_test} items, {counted_number} counted, {folder_number} folders, {files_number} files, {round(counted_number/total_to_test*100, 2)}%')
    print(f'{total_file} files, count time: {folder_count_time_total} s, avrage time: {round(folder_count_time_total / folder_number, 2)} s')


if __name__ == '__main__':
    test_calculate_items()