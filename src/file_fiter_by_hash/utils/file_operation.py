import pathlib

class FileOperation:
    def __init__(self, backup_dir: str|pathlib.Path,processing_dir:str|pathlib.Path):
        self.backup_dir = backup_dir if isinstance(backup_dir, pathlib.Path) else pathlib.Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.processing_dir = processing_dir if isinstance(processing_dir, pathlib.Path) else pathlib.Path(processing_dir)
        self.processing_dir.mkdir(parents=True, exist_ok=True)
    


def remove_to_pending_backup(folder_name: str|pathlib.Path):
    '''
    将文件夹移动到pending_backup文件夹
    '''
