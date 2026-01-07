from file_fiter_by_hash.service.zip_item import zip_item
from file_fiter_by_hash.calculate_hash import calculate_folder_hash,calculate_file_hash,HashParams
from pathlib import Path

source_file_path =  Path(r'e:\QQDownload\[qiporn.com更新30分钟完整版]太阳花女王刘乔安援交视频12分30秒尝鲜版\太阳花女王援交视频12分30秒尝鲜版.mp4')
source_folder_path = Path(r'E:\QQDownload\[qiporn.com更新30分钟完整版]太阳花女王刘乔安援交视频12分30秒尝鲜版')
target_file_dir = Path(r'K:\转储temp\测试')

def reset_folder():
    import shutil
    shutil.rmtree(target_file_dir)
    target_file_dir.mkdir(parents=True, exist_ok=True)

def test_zip_file_with_password():
    target_dir_1 = target_file_dir / '文件' / '加密' / '1'
    target_item1 = zip_item(source_file_path, target_dir_1, password='123456', compress_level=0)
    print(f'测试zip加密文件1,压缩成功,压缩包路径:{target_item1}')
    target_file_path_2 = target_file_dir / '文件' / '加密' / '2' 
    target_item2 = zip_item(source_file_path, target_file_path_2, password='123456', compress_level=0)
    print(f'测试zip加密文件2,压缩成功,压缩包路径:{target_item2}')
    return target_item1,target_item2


def test_zip_file_without_password():
    target_dir_1 = target_file_dir / '文件' / '无加密' / '1'
    target_item1 = zip_item(source_file_path, target_dir_1, password=None, compress_level=0)
    print(f'测试zip无加密文件1,压缩成功,压缩包路径:{target_item1}')
    target_file_path_2 = target_file_dir / '文件' / '无加密' / '2' 
    target_item2 = zip_item(source_file_path, target_file_path_2, password=None, compress_level=0)
    print(f'测试zip无加密文件2,压缩成功,压缩包路径:{target_item2}')
    return target_item1,target_item2

def test_zip_folder_with_password():
    target_dir_1 = target_file_dir / '文件夹' / '加密' / '1'
    target_item1 = zip_item(source_folder_path, target_dir_1, password='123456', compress_level=0)
    print(f'测试zip加密文件夹1,压缩成功,压缩包路径:{target_item1}')
    target_file_path_2 = target_file_dir / '文件夹' / '加密' / '2' 
    target_item2 = zip_item(source_folder_path, target_file_path_2, password='123456', compress_level=0)
    print(f'测试zip加密文件夹2,压缩成功,压缩包路径:{target_item2}')
    return target_item1,target_item2
def test_zip_folder_without_password():
    target_dir_1 = target_file_dir / '文件夹' / '无加密' / '1'
    target_item1 = zip_item(source_folder_path, target_dir_1, password=None, compress_level=0)
    print(f'测试zip无加密文件夹1,压缩成功,压缩包路径:{target_item1}')
    target_file_path_2 = target_file_dir / '文件夹' / '无加密' / '2' 
    target_item2 = zip_item(source_folder_path, target_file_path_2, password=None, compress_level=0)
    print(f'测试zip无加密文件夹2,压缩成功,压缩包路径:{target_item2}')
    return target_item1,target_item2

def compare_zip_item_hash(zip_item1,zip_item2):
    hash_params1 = HashParams(item_path=zip_item1,algorithm=['sha1','md5','sha256'])
    hash_params2 = HashParams(item_path=zip_item2,algorithm=['sha1','md5','sha256'])
    
    hash1 = calculate_folder_hash(hash_params1) if zip_item1.is_dir() else calculate_file_hash(hash_params1)
    hash2 = calculate_folder_hash(hash_params2) if zip_item2.is_dir() else calculate_file_hash(hash_params2)
    print(f'测试zip文件{zip_item1.name}哈希值:{hash1.info.hash_info}')
    print(f'测试zip文件{zip_item2.name}哈希值:{hash2.info.hash_info}')
    return hash1.info.hash_info == hash2.info.hash_info



if __name__=='__main__':
    reset_folder()
    zip_item1,zip_item2 = test_zip_file_with_password()
    assert compare_zip_item_hash(zip_item1,zip_item2)
    zip_item1,zip_item2 = test_zip_file_without_password()
    assert compare_zip_item_hash(zip_item1,zip_item2)
    zip_item1,zip_item2 = test_zip_folder_with_password()
    assert compare_zip_item_hash(zip_item1,zip_item2)
    zip_item1,zip_item2 = test_zip_folder_without_password()
    assert compare_zip_item_hash(zip_item1,zip_item2)
