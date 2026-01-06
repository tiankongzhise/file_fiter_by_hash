import pathlib
import hashlib
from .calculate_hash import calculate_file_hash_base
from tqdm import tqdm
from ..schmeas import HashParams, HashInfo, HashResult
from ..logger import logger
from ..config.service_code import get_service_code
from ..utils import get_all_file_path, calculate_big_folder_size


class CalculateFolderHash:
    def __init__(self):
        self.folder_path: pathlib.Path = None
        self.algorithm: str = None
        self.logger = logger

    def calculate_hash(self) -> str:
        """计算文件夹下所有文件的哈希值"""
        all_file_list = get_all_file_path(self.folder_path)
        if not all_file_list:
            self.logger.info(
                code=get_service_code("空文件夹，无需计算"),
                message=f"文件夹 {self.folder_path.name} 下没有文件",
            )
            return HashResult(
                status="empty",
                info=HashInfo(
                    name=self.folder_path.name, type="folder", size=0, hash_info={}
                ),
                message="folder is empty",
            )
        if len(all_file_list) > 100:
            try:
                big_folder_size = calculate_big_folder_size(all_file_list)
            except Exception as e:
                self.logger.error(
                    code=get_service_code("超大文件夹,统计文件夹大小失败"),
                    message=f"文件夹 {self.folder_path.name} 下有 {len(all_file_list)} 个文件，文件大小总和计算失败，错误信息为 {str(e)}",
                )
                return HashResult(
                    status="error",
                    info=HashInfo(
                        name=self.folder_path.name, type="folder", size=0, hash_info={}
                    ),
                    message="folder size calculate error",
                )
            self.logger.info(
                code=get_service_code("超大文件夹,统计文件夹大小成功"),
                message=f"文件夹 {self.folder_path.name} 下有 {len(all_file_list)} 个文件，文件大小总和为 {big_folder_size}，请确认是否需要计算",
            )
            return HashResult(
                status="big_folder",
                info=HashInfo(
                    name=self.folder_path.name,
                    type="folder",
                    size=big_folder_size,
                    hash_info={},
                ),
                message="文件加下小文件过多,请人工处理",
            )
        sorted_file_path = sorted(all_file_list)
        hash_result = {}
        size_list = []
        try:
            for alg in self.algorithm:
                size = 0
                hash_obj = hashlib.new(alg)
                for file_path in tqdm(
                    sorted_file_path,
                    desc=f"{self.folder_path.name} Hashing files with {alg}",
                ):
                    hash_obj.update(calculate_file_hash_base(file_path, alg).encode())
                    size += pathlib.Path(file_path).stat().st_size
                size_list.append(size)
            hash_result[alg] = hash_obj.hexdigest().upper()
            self.logger.info(
                code=get_service_code("文件夹hash计算成功"),
                message=f"文件夹 {self.folder_path.name} 下所有文件的 {alg} 哈希值为 {hash_result[alg]}",
            )
            benchmark = size_list[0]
            for item in size_list:
                if item != benchmark:
                    self.logger.warning(
                        code=get_service_code("文件夹hash计算文件大小不一致"),
                        message=f"文件夹{self.folder_path.name}下hash计算出现文件大小不一致，基准大小为{benchmark}，当前文件大小为{item}",
                    )
        except Exception as e:
            self.logger.error(
                code=get_service_code("文件夹hash计算失败"),
                message=f"文件夹 {self.folder_path.name} 下所有文件的 {alg} 哈希值计算失败，错误信息为 {str(e)}",
            )
        return HashResult(
            status="success",
            info=HashInfo(
                name=self.folder_path.name,
                type="folder",
                size=benchmark,
                hash_info=hash_result,
            ),
        )

    def __call__(self, hash_params: HashParams) -> HashResult:
        self.folder_path = hash_params.item_path
        self.algorithm = hash_params.algorithm
        return self.calculate_hash()


calculate_folder_hash = CalculateFolderHash()

if __name__ == "__main__":
    # folder_path = pathlib.Path(r"L:\动物行为学\PHPWAMP_IN1")
    # folder_path = pathlib.Path(r"L:\动物行为学\[魔穗字幕组][PoRO]らぶ2Quad 「完璧ドS淑女-エル～優雅に尻敷くフェイス＆ボッキ」[1280x720 x264 AAC]")
    # folder_path = pathlib.Path(r"L:\动物行为学描述文档\[魔穗字幕组][PoRO]らぶ2Quad 「完璧ドS淑女-エル～優雅に尻敷くフェイス＆ボッキ」[1280x720 x264 AAC]")
    folder_path = pathlib.Path(r"e:\B站视频下载")
    hash_params = HashParams(
        item_path=folder_path, algorithm=["sha1", "md5", "sha256"]
    )
    calculate_folder_hash = CalculateFolderHash()
    print(calculate_folder_hash(hash_params))
