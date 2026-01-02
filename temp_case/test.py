import pathlib
import hashlib
import time



file_path = pathlib.Path("L:\动物行为学")
total_items = 0
file_count = 0
folder_count = 0
# 计算所有文件的md5 耗时 单位秒
calculate_time_count = 0
average_time_count = 0
def calculate_file_hash(file_path: pathlib.Path, algorithm: str = 'sha256') -> str:
    """计算单个文件的哈希值"""
    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        # 大文件 一次读取500MB 内存占用低
        for chunk in iter(lambda: f.read(500*1024*1024), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


for item in file_path.iterdir():
    print(item)
    total_items += 1
    if item.is_file():
        file_count += 1
        time_start = time.time()
        md5 = calculate_file_hash(item, 'md5')
        time_end = time.time()
        # 计算耗时 单位秒
        current_file_calculate_time = round((time_end - time_start), 2)
        calculate_time_count += current_file_calculate_time
        print(f"File: {item.name}, MD5: {md5}, Calculate time: {current_file_calculate_time} s")
    elif item.is_dir():
        folder_count += 1
print(f"Total items: {total_items}")
print(f"Files: {file_count}")
print(f"Folders: {folder_count}")
# 计算所有文件的md5 耗时 单位秒
average_time_count = round(calculate_time_count / file_count, 2)
print(f"Total calculate time: {calculate_time_count} s")
print(f"Average calculate time: {average_time_count} s")
