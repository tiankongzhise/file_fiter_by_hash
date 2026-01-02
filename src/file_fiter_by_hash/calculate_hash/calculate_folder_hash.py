import pathlib
import hashlib
from functools import cache
from calculate_hash import calculate_file_hash_base
from tqdm import tqdm
from schmeas import HashParams, HashInfo, HashResult


class CalculateFolderHash:
    def __init__(self):
        self.folder_path: pathlib.Path = None
        self.algorithm: str = None
    @cache
    def find_files(self, folder_path: pathlib.Path = None) -> list:
        """查找文件夹下所有文件"""
        file_path = []
        for item in folder_path.iterdir():
            if item.is_file():
                # 路径的文本表示
                file_path.append(item.as_posix())
            elif item.is_dir():
                file_path.extend(self.find_files(item))
        return file_path
    
    def calculate_hash(self) -> str:
        """计算文件夹下所有文件的哈希值"""
        all_file_list = self.find_files(self.folder_path)
        if not all_file_list:
            return HashResult(status='empty', info=HashInfo(name=self.folder_path.name, type='folder', size=0, hash_info={}), message='folder is empty')
        if len(all_file_list) > 100:
            return HashResult(status='big_folder', info=HashInfo(name=self.folder_path.name, type='folder', size=0, hash_info={}), message='文件加下小文件过多,请人工处理')
        sorted_file_path = sorted(all_file_list)
        hash_result = {}
        size = 0
        for alg in self.algorithm:
            hash_obj = hashlib.new(alg)
            for file_path in tqdm(sorted_file_path, desc=f'{self.folder_path.name} Hashing files with {alg}'):
                hash_obj.update(calculate_file_hash_base(file_path, alg).encode())
                size += pathlib.Path(file_path).stat().st_size
        hash_result[alg] = hash_obj.hexdigest().upper()
        return HashResult(status='success', info=HashInfo(name=self.folder_path.name, type='folder', size=size, hash_info=hash_result))
    
    def __call__(self,hash_params: HashParams) -> HashResult:
        self.folder_path = hash_params.folder_path
        self.algorithm = hash_params.algorithm
        return self.calculate_hash()
 
calculate_folder_hash = CalculateFolderHash()

if __name__ == '__main__':
    # folder_path = pathlib.Path(r"L:\动物行为学\PHPWAMP_IN1")
    folder_path = pathlib.Path(r"L:\动物行为学\[魔穗字幕组][PoRO]らぶ2Quad 「完璧ドS淑女-エル～優雅に尻敷くフェイス＆ボッキ」[1280x720 x264 AAC]")
    # folder_path = pathlib.Path(r"L:\动物行为学描述文档\[魔穗字幕组][PoRO]らぶ2Quad 「完璧ドS淑女-エル～優雅に尻敷くフェイス＆ボッキ」[1280x720 x264 AAC]")
    hash_params = HashParams(folder_path=folder_path, algorithm=['sha1','md5','sha256'])
    calculate_folder_hash = CalculateFolderHash()
    print(calculate_folder_hash(hash_params))
