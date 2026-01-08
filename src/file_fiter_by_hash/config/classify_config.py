from dataclasses import dataclass


@dataclass
class ClassifyConfig:
    # 记录需要处理的源文件夹或者源文件
    sources_list:list[str] = [r'']
    
    # 经过检测，无特殊情况，没有备份过的项目,需要被压缩的，被转移到此文件夹
    normal_folder: str = r'D:\待压缩后备份'
    
    # 没有备份过，被压缩过后，生成的文件在此文件夹
    upload_folder: str = r'D:\待上传'

    # 文件数量超过阈值的文件夹被转移到此文件夹
    overcount_folder: str = r'D:\数量超过阈值'
    
    # 文件或文件夹大小超过阈值的被转移到此文件夹
    oversize_folder: str = r'D:\大小超过阈值'
    
    # 已经被备份过的文件,等待被删除
    duplicate_folder: str = r'D:\与备份文件重复'
    
    # 本次处理过程中发现的重复文件,移动到此文件夹,等待处理
    local_duplicate_folder: str = r'D:\本地重复'
    
    
    # 压缩时每次压缩的文件大小阈值，单位字节
    max_processing_file_size: int = 1024 * 1024 * 500 # 500M
    
    # 最大处理文件夹文件数量
    max_processing_folder_file_count: int = 100

    # 百度网盘上传文件大小限制
    baidu_pan_upload_max_size: int = 1024 * 1024 * 1024 *19
