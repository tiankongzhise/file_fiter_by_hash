import pathlib

class FileOperation:
    def __init__(self, backup_dir: str|pathlib.Path,processing_dir:str|pathlib.Path):
        self.backup_dir = backup_dir if isinstance(backup_dir, pathlib.Path) else pathlib.Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.processing_dir = processing_dir if isinstance(processing_dir, pathlib.Path) else pathlib.Path(processing_dir)
        self.processing_dir.mkdir(parents=True, exist_ok=True)
    


def remove_to_pending_backup(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到待备份文件夹
    '''
    pass

def remove_to_processing(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到待人工处理文件夹
    '''
    pass
def remove_to_panding_delete(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到待删除文件夹
    '''
    pass

def delete_empty_folder(folder_name:str|pathlib.Path):
    '''
    将空文件夹进行删除
    '''
    pass

def remove_to_local_duplicate(folder_name: str|pathlib.Path):
    '''
    将本地重复文件夹移动到待删除文件夹
    '''
    pass
