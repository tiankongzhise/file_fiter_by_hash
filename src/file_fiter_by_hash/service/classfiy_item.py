
import pathlib
from os import PathLike
from ..config import zipped_suffix,ClassifyConfig



def is_zip_file(item:pathlib.Path):
    """
    判断文件是否为压缩文件
    """
    return item.suffix in zipped_suffix
def is_normal_file(item:pathlib.Path):
    """
    判断文件是否小于等于19GB
    """
    return item.is_file() and item.stat().st_size <= 1024 * 1024 * 1024 * 19
def is_big_file(item:pathlib.Path):
    """
    判断文件是否大于19GB
    """
    return item.is_file() and item.stat().st_size > 1024 * 1024 * 1024*19

def is_empty_folder(item:pathlib.Path):
    return item.is_dir() and not any(item.iterdir())


def is_folder_oversize(item:list[pathlib.Path]):
    """
    判断文件夹是否大于19GB
    """
    return sum([i.stat().st_size for i in item]) > 1024 * 1024 * 1024 * 19


def is_folder_filecount_exceed(item:list[pathlib.Path]):
    """
    判断文件夹是否包含超过100个文件
    """
    return len(item) > ClassifyConfig.max_processing_folder_file_count



def classify_item(item:list[PathLike]|PathLike):
    if not isinstance(item,list):
        item = [item]
    result = {}
    for item in item:
        item = pathlib.Path(item)
        if not item.exists():
            raise FileNotFoundError(f"item {item} not exists")
        

        if is_big_file(item):
            result[item] = 'big_file'
            continue
        if is_zip_file(item):
            result[item] = 'zip_file'
            continue
        if is_normal_file(item):
            result[item] = 'normal_file'
            continue
        if is_empty_folder(item):
            result[item] = 'empty_folder'
            continue
        all_file_iter = [i for i in item.rglob("*") if i.is_file()]
        if is_folder_filecount_exceed(all_file_iter):
            result[item] = 'folder_exceed_count'
            continue
        if is_folder_oversize(all_file_iter):
            result[item] = 'folder_oversize'
            continue
        result[item] = 'normal_folder'
    return result
