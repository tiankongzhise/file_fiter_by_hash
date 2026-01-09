from dataclasses import dataclass, field


@dataclass
class FileConfig:
    # 待备份文件夹
    backup_dir: str = r'D:\待备份'

    # 待人工处理文件夹
    processing_dir: str = r'D:\待人工处理'

    # 待删除文件夹（重复文件）
    duplicate_dir: str = r'D:\待删除'

    # 本地重复文件夹
    local_duplicate_dir: str = r'D:\本地重复'
