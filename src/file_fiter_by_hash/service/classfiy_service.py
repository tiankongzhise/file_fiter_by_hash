
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
    判断文件是否小于等于百度网盘允许上传的最大限制
    """
    return item.is_file() and item.stat().st_size <= ClassifyConfig.baidu_pan_upload_max_size
def is_big_file(item:pathlib.Path):
    """
    判断文件是否大于百度网盘允许上传的最大限制
    """
    return item.is_file() and item.stat().st_size > ClassifyConfig.baidu_pan_upload_max_size

def is_empty_folder(item:pathlib.Path):
    return item.is_dir() and not any(item.iterdir())


def is_folder_oversize(item:list[pathlib.Path]):
    """
    判断文件夹是否大于百度网盘允许上传的最大限制
    """
    return sum([i.stat().st_size for i in item]) > ClassifyConfig.baidu_pan_upload_max_size


def is_folder_filecount_exceed(item:list[pathlib.Path]):
    """
    判断文件夹是否包含超过100个文件
    """
    return len(item) > ClassifyConfig.max_processing_folder_file_count



def classify_item(item:list[PathLike]|PathLike):
    '''
    对文件或文件夹进行分类
    @param item: 文件或文件夹路径, str or pathlib.Path
    @return: 分类结果, dict, key为文件路径, value为分类结果
    '''

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


def classify_folder(folder:PathLike):
    '''
    对文件夹进行分类,仅对第一层进行分类，不递归分类
    @param folder: 文件夹路径, str or pathlib.Path
    @return: 分类结果, list[dict], key为文件或文件夹路径, value为分类结果
    '''
    folder = pathlib.Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"folder {folder} not exists")
    return [classify_item(i) for i in folder.glob("*")]
