from file_fiter_by_hash.service.zip_serice import zip_item,unzip_item
from pathlib import Path
from file_fiter_by_hash.service.calculate_hash_service import calculate_folder_hash,calculate_file_hash,HashParams
import datetime


def test_compare_hash(file1):
    file1_path = Path(file1)
    zip_folder = Path(r'D:\移动文件测试源')
    unzip_folder = Path(r'D:\待人工处理')

    file1_hash = calculate_folder_hash(hash_params=HashParams(item_path=file1_path,algorithm=['sha1','sha256','md5']))
    zipped_file_path = zip_item(file1_path,zip_folder,'H_x123456789',0)
    zip_hash = calculate_file_hash(HashParams(item_path=zipped_file_path,algorithm=['sha1','sha256','md5']))
    print(zip_hash)
    unzipped_file_path = unzip_item(zipped_file_path,unzip_folder,'H_x123456789')
    unzipped_file_hash = calculate_folder_hash(HashParams(item_path=unzipped_file_path,algorithm=['sha1','sha256','md5']))
    for hash_fun,hash_value in file1_hash.info.hash_info.items():
        if hash_value != unzipped_file_hash.info.hash_info[hash_fun]:
            print(f"Hash mismatch for {hash_fun}: {hash_value} != {unzipped_file_hash.info.hash_info[hash_fun]}")
    print("Hash comparison completed.")
    return zipped_file_path,unzipped_file_path

def del_file(zipped_file:Path,unzip_folder:Path):
    import shutil
    zipped_file.unlink()
    shutil.rmtree(unzip_folder)

def test_unzip(zip_file_path,unzip_folder):
    unzip_item(zip_file_path, unzip_folder, 'H_x123456789')

if __name__ == "__main__":
    beg_time = datetime.datetime.now()
    result = test_compare_hash(r'E:\迅雷云盘')
    end_time = datetime.datetime.now()
    print(f"Test completed in {end_time - beg_time} seconds")
    print(result)
    del_file(*result)

    # test_unzip(r'd:\移动文件测试源\20260109\解压密码_H_x123456789\B站视频下载.zip', r'D:\待备份')
