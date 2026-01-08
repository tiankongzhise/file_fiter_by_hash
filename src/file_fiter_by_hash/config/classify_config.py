from dataclasses import dataclass


@dataclass
class ClassifyConfig:
    # 记录需要处理的源文件夹或者源文件
    sources_list:list[str] = [r'']
    
    # 压缩后的结果保存到此文件夹
    zipped_folder: str = r''

    # 将压缩后的文件解压到此文件夹与源文件进行比较
    rezip_folder: str = r''
    
    # 压缩时每次压缩的文件大小阈值，单位字节
    max_processing_file_size: int = 1024 * 1024 * 500 # 500M
    
    # 最大处理文件夹文件数量
    max_processing_folder_file_count: int = 100

    # 百度网盘上传文件大小限制
    baidu_pan_upload_max_size: int = 1024 * 1024 * 1024 *19
