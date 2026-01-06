from file_fiter_by_hash.calculate_hash import calculate_folder_hash,calculate_file_hash
import pathlib
from file_fiter_by_hash.schmeas import HashParams


def test_zip_hash():
    file_list = [
        r'k:\测试\测试.7z.001',
        r'k:\测试\测试aaa.7z.001',
        r'k:\测试\测试bbb.7z.001',
    ]
    for file_path in file_list:
        temp_path = pathlib.Path(file_path)
        hash_params = HashParams(item_path=temp_path, algorithm=['sha1','md5','sha256'])
        hash_result = calculate_file_hash(hash_params)
        print(hash_result)


if __name__ == '__main__':
    # folder_path = pathlib.Path(r"E:\迅雷下载")
    # hash_params = HashParams(folder_path=folder_path, algorithm=['sha1','md5','sha256'])
    # hash_result = calculate_folder_hash(hash_params)
    # print(hash_result)
    test_zip_hash()