import pathlib
import hashlib
from .calculate_hash import calculate_file_hash_base
from tqdm import tqdm
from ...schmeas import HashParams, HashInfo, HashResult
from ...logger import get_logger
from ...config import ClassifyConfig

logger = get_logger("calculate_folder_hash")


class CalculateFolderHash:
    def __init__(self):
        self.folder_path: pathlib.Path = None
        self.algorithm: str = None
        self.logger = get_logger("CalculateFolderHash")
        self.all_file_list: list = None


    def _is_empty_folder(self) -> bool:
        """判断文件夹是否为空"""
        return not any(self.folder_path.iterdir())

    def _is_folder_filecount_exceed(self) -> bool:
        """判断文件夹下文件数量是否超过100个"""
        all_item = self.folder_path.rglob("*")
        self.all_file_list = [item for item in all_item if item.is_file()]
        return len(self.all_file_list) > ClassifyConfig.max_processing_folder_file_count


    def calculate_hash(self) -> str:
        """计算文件夹下所有文件的哈希值"""
        if self._is_empty_folder():
            self.logger.info(
                message=f"文件夹 {self.folder_path.name} 下没有文件",
            )
            return HashResult(
                status="empty",
                info=HashInfo(
                    name=self.folder_path.name, type="folder", size=0, hash_info={}
                ),
                message="folder is empty",
            )

        if self._is_folder_filecount_exceed():
            try:
                big_folder_size = sum([item.stat().st_size for item in self.all_file_list])
            except Exception as e:
                self.logger.error(
                    message=f"文件夹 {self.folder_path.name} 下有 {len(self.all_file_list)} 个文件，文件大小总和计算失败，错误信息为 {str(e)}",
                )
                return HashResult(
                    status="error",
                    info=HashInfo(
                        name=self.folder_path.name, type="folder", size=0, hash_info={}
                    ),
                    message="folder size calculate error",
                )
            self.logger.info(
                message=f"文件夹 {self.folder_path} 下有 {len(self.all_file_list)} 个文件，文件大小总和为 {big_folder_size}，请确认是否需要计算",
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
        sorted_file_path = sorted(self.all_file_list)
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
                    message=f"文件夹 {self.folder_path.name} 下所有文件的 {alg} 哈希值为 {hash_result[alg]}",
                )
            benchmark = size_list[0]
            for item in size_list:
                if item != benchmark:
                    self.logger.warning(
                        message=f"文件夹{self.folder_path.name}下hash计算出现文件大小不一致，基准大小为{benchmark}，当前文件大小为{item}",
                    )
        except Exception as e:
            self.logger.error(
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
