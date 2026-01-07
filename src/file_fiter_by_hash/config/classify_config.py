from dataclasses import dataclass

@dataclass
class ClassifyConfig:
    # 记录需要处理的文件夹的源文件
    source_file:str = r''
    
    # 需要备份的文件或文件夹移动到此文件夹等待处理
    backup_dir: str = r'D:\待备份'
    
    # 大型文件夹等待人工处理
    processing_dir: str = r'D:\待人工处理'
    
    # 已经被备份过的文件,等待被删除
    duplicate_dir: str = r'D:\待删除'
    
    # 本次处理过程中发现的重复文件,移动到此文件夹,等待处理
    local_duplicate_dir: str = r'D:\本地重复'
    
    
    # 最大处理文件大小,单位字节
    max_processing_file_size: int = 1024 * 1024 * 100
    
    # 最大处理文件夹文件数量
    max_processing_folder_file_count: int = 200

    # 百度网盘上传文件大小限制
    baidu_pan_upload_max_size: int = 1024 * 1024 * 1024 *19
