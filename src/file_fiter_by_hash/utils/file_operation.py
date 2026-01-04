import pathlib
from ..config.file_config import FileConfig
from ..logger import get_logger
import shutil

logger = get_logger()

def move_file_by_pathlib(source_file: pathlib.Path, target_dir:pathlib.Path):
    """
    pathlib模块移动文件（官方推荐，适配Windows，最简洁）
    :param source_file: 待移动文件的完整路径(str/Path对象都支持)
    :param target_dir:  目标文件夹路径(str/Path对象都支持)
    """
    try:        
        # 1. 校验源文件
        if not source_file.exists():
            return Exception(f"源文件不存在 → {source_file}")
        # 2. 自动创建目标文件夹（不存在则创建，递归创建多级目录）
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 3. 核心：拼接【目标文件夹+原文件名】，实现移动
        target_file = target_dir / source_file.name
        
        # 确保目标路径文件夹路径存在
        target_file.parent.mkdir(parents=True, exist_ok=True)
        
        
        shutil.move(src= source_file, dst = target_file)
        return True
    except Exception as e:
        return e



def remove_to_pending_backup(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到待备份文件夹
    '''
    backup_dir = FileConfig.backup_dir
    if isinstance(backup_dir, str):
        backup_dir = pathlib.Path(backup_dir)
    if isinstance(folder_name, str):
        folder_name = pathlib.Path(folder_name)
    move_result = move_file_by_pathlib(folder_name, backup_dir)
    if move_result is True:
        logger.info(f"文件夹 {folder_name} 已成功移动到备份文件夹 {backup_dir}")
        return True
    else:
        logger.error(f"文件夹 {folder_name} 移动到备份文件夹 {backup_dir} 失败 → {move_result}")
        return False

def remove_to_processing(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到待人工处理文件夹
    '''
    processing_dir = FileConfig.processing_dir
    if isinstance(processing_dir, str):
        processing_dir = pathlib.Path(processing_dir)
    if isinstance(folder_name, str):
        folder_name = pathlib.Path(folder_name)
    move_result = move_file_by_pathlib(folder_name, processing_dir)
    if move_result is True:
        logger.info(f"文件夹 {folder_name} 已成功移动到待人工处理文件夹 {processing_dir}")
        return True
    else:
        logger.error(f"文件夹 {folder_name} 移动到待人工处理文件夹 {processing_dir} 失败 → {move_result}")
        return False
def remove_to_panding_delete(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到待删除文件夹
    '''
    delete_dir = FileConfig.duplicate_dir
    if isinstance(delete_dir, str):
        delete_dir = pathlib.Path(delete_dir)
    if isinstance(folder_name, str):
        folder_name = pathlib.Path(folder_name)
    move_result = move_file_by_pathlib(folder_name, delete_dir)
    if move_result is True:
        logger.info(f"文件夹 {folder_name} 已成功移动到待删除文件夹 {delete_dir}")
        return True
    else:
        logger.error(f"文件夹 {folder_name} 移动到待删除文件夹 {delete_dir} 失败 → {move_result}")
        return False

def delete_empty_folder(folder_name:str|pathlib.Path):
    '''
    将空文件夹进行删除
    '''
    if isinstance(folder_name, str):
        folder_name = pathlib.Path(folder_name)
    if folder_name.exists() and folder_name.is_dir() and not any(folder_name.iterdir()):
        folder_name.rmdir()
        logger.info(f"空文件夹 {folder_name} 已成功删除")
        return True
    else:
        logger.error(f"文件夹 {folder_name} 不是空文件夹，无法删除")
        return False

def remove_to_local_duplicate(folder_name: str|pathlib.Path):
    '''
    将本地重复文件夹移动到待删除文件夹
    '''
    delete_dir = FileConfig.local_duplicate_dir
    if isinstance(delete_dir, str):
        delete_dir = pathlib.Path(delete_dir)
    if isinstance(folder_name, str):
        folder_name = pathlib.Path(folder_name)
    move_result = move_file_by_pathlib(folder_name, delete_dir)
    if move_result is True:
        logger.info(f"文件夹 {folder_name} 已成功移动到本地待删除文件夹 {delete_dir}")
        return True
    else:
        logger.error(f"文件夹 {folder_name} 移动到本地待删除文件夹 {delete_dir} 失败 → {move_result}")
        return False
