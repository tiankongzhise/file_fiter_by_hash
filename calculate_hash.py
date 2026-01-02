import hashlib
import pathlib
from schmeas import HashInfo, HashResult, HashParams

def calculate_file_hash_base(file_path: pathlib.Path|str, algorithm: str = 'sha256') -> str:
    """计算单个文件的哈希值"""
    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        # 大文件 一次读取500MB 内存占用低
        for chunk in iter(lambda: f.read(500*1024*1024), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest().upper()

def calculate_file_hash(params: HashParams) -> HashResult:
    try:
        hash_result = {}
        for alg in params.algorithm:
            hash_result[alg] = calculate_file_hash_base(params.folder_path, alg)
    except Exception as e:
        return HashResult(status='error', info=HashInfo(name=params.folder_path.name, type='file', algorithm=params.algorithm, size=params.folder_path.stat().st_size, hash_info={}), error_message=str(e))
    return HashResult(status='success', info=HashInfo(name=params.folder_path.name, type='file', algorithm=params.algorithm, size=params.folder_path.stat().st_size, hash_info=hash_result))


if __name__ == '__main__':
    params = HashParams(folder_path=pathlib.Path("k:\转储temp\动物行为学.7z.135"), algorithm=['sha1','md5','sha256'])
    md5 = calculate_file_hash(params)
    print(md5)
    target_md5= '967089a10i391049fb1a744be3dd6d26'
    if md5 == target_md5:
        print("文件匹配")
    else:
        print("文件不匹配")