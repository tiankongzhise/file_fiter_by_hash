from tkinter import Pack
from ..config.classify_config import ClassifyConfig
from ..service.classfiy_service import classify_folder,classify_item
import pathlib
def pre_classify(config: ClassifyConfig):
    result = {}
    for item in config.sources_list:
        temp = pathlib.Path(item)
        if temp in result:
            continue
        if temp.is_dir():
            result[temp] = classify_folder(temp)
        elif temp.is_file():
            result[temp] = classify_item(temp)
    return result

def save_pre_classify_result(pre_classify_result: dict):
    pass

def calculate_hash_result(save_pre_classify_result: dict):
    pass

def save_hash_result(hash_result: dict):
    pass

def zip_item(item_info):
    pass
def save_zip_result(zip_result: dict):
    pass
def calculate_ziped_item_hash(zip_item):
    pass
def save_ziped_item_hash(ziped_item_hash: dict):
    pass
def rezip_item(zip_item):
    pass
def save_rezip_result(rezip_result: dict):
    pass
def compare_rezip_source():
    pass
def save_compare_result(compare_result: dict):
    pass
def upload_ziped_file(zip_file):
    pass
def save_upload_result(upload_result: dict):
    pass
def del_zipped_file(zip_file):
    pass
def save_del_result(del_result: dict):
    pass
def del_source_file():
    pass
def save_del_source_result(del_source_result: dict):
    pass
