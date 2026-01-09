import hashlib
import pathlib
from ...schmeas import HashInfo, HashResult, HashParams
from ...logger import get_logger

logger = get_logger("calculate_hash")

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
            hash_result[alg] = calculate_file_hash_base(params.item_path, alg)
            logger.info(message=f'文件 {params.item_path.name} 哈希值 {alg} 计算完成，哈希值为 {hash_result[alg]}')
    except Exception as e:
        logger.error(message=f'文件 {params.item_path.name} 哈希值 {params.algorithm} 计算失败，错误信息为 {str(e)}')
        return HashResult(status='error', info=HashInfo(name=params.item_path.name, type='file', algorithm=params.algorithm, size=params.item_path.stat().st_size, hash_info={}), message=str(e))


    return HashResult(status='success', info=HashInfo(name=params.item_path.name, type='file', algorithm=params.algorithm, size=params.item_path.stat().st_size, hash_info=hash_result))


if __name__ == '__main__':
    params = HashParams(item_path=pathlib.Path("k:\转储temp\动物行为学.7z.135"), algorithm=['sha1','md5','sha256'])
    md5 = calculate_file_hash(params)
    print(md5)
    target_md5= '967089a10i391049fb1a744be3dd6d26'
    if md5 == target_md5:
        print("文件匹配")
    else:
        print("文件不匹配")
