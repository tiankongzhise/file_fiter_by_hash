from file_fiter_by_hash.calculate_hash import calculate_folder_hash
import pathlib
from file_fiter_by_hash.schmeas import HashParams



if __name__ == '__main__':
    folder_path = pathlib.Path(r"E:\迅雷下载")
    hash_params = HashParams(folder_path=folder_path, algorithm=['sha1','md5','sha256'])
    hash_result = calculate_folder_hash(hash_params)
    print(hash_result)
