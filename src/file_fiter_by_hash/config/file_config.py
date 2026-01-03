from dataclasses import dataclass

@dataclass
class FileConfig:
    backup_dir: str = r'D:\待备份'
    processing_dir: str = r'D:\待人工处理'
    local_duplicate_dir: str = r'D:\本地重复'
    duplicate_dir: str = r'D:\待删除'
