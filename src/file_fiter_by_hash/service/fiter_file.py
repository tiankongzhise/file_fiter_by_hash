
import pathlib
from ..logger import get_logger
from ..utils import calculate_big_folder_size,get_all_file_path
from ..utils.dto import transform_special_folder_list_to_dict
from ..mysql_db.query_item import get_all_special_folder

class FilterFile:
    def __init__(self, file_path: str|pathlib.Path):
        self.file_path = file_path if isinstance(file_path, pathlib.Path) else pathlib.Path(file_path)
        self.logger = get_logger()
        self.file_list = []
        self.folder_list = []
        self.normal_folder_list = []
        self.big_folder_list = []
        self.empty_folder_list = []
        
        
    def step_one(self):
        '''
        步骤一：将文件夹第一层分类为文件和文件夹
        '''
        # 文件夹第一层分类为文件和文件夹
        for item in self.file_path.iterdir():
            if item.is_file():
                self.file_list.append(item)
            elif item.is_dir():
                self.folder_list.append(item)
        self.logger.info(f'文件夹第一层分类为文件和文件夹，文件数量为{len(self.file_list)}，文件夹数量为{len(self.folder_list)}')
    
    def step_two(self):
        '''
        步骤二：将文件夹类进行分类，分为普通文件夹类和超大文件夹类和空文件夹
        '''
        for folder in self.folder_list:
            all_file_list = get_all_file_path(folder)
            if not all_file_list:
                self.empty_folder_list.append(folder)
            elif len(all_file_list) > 100:
                self.big_folder_list.append({folder:all_file_list})
            else:
                self.normal_folder_list.append({folder:all_file_list})
        self.logger.info(f'第二步分类为普通文件夹类和超大文件夹类和空文件夹，普通文件夹数量为{len(self.normal_folder_list)}，超大文件夹数量为{len(self.big_folder_list)}，空文件夹数量为{len(self.empty_folder_list)}')
    def step_three(self):
        '''
        步骤三：处理超大文件夹类，从特殊文件夹数据库，拉取全部数据。然后在本地比对名称和文件大小是否一致，一致说明已经被处理。文件夹移动到待删除文件夹，否则移动到待备份文件夹。
        '''
        # 从特殊文件夹数据库，拉取全部数据
        special_folder_squeue = get_all_special_folder()
        special_folder_dict = transform_special_folder_list_to_dict(special_folder_squeue)
        for big_folder in self.big_folder_list:
            folder_name = list(big_folder.keys())[0]
            if folder_name not in special_folder_dict.keys():
                remove_to_pending_backup(folder_name)
            
            
                folder_size = calculate_big_folder_size(big_folder[folder_name])
            if folder_name in special_folder_dict and special_folder_dict[folder_name] == folder_size:
                self.empty_folder_list.append(folder_name)
            else:
                self.normal_folder_list.append(big_folder)
        
        
    def step_four(self):
        '''
        步骤四：处理空文件夹类，直接删除文件夹
        '''
    def step_five(self):
        '''
        步骤五：处理普通文件夹类，根据哈希值查询数据库，判断是否存在。如果存在，说明已经被处理。文件夹移动到待删除文件夹，否则移动到待备份文件夹。
        '''
    def step_six(self):
        '''
        步骤六：处理文件，根据哈希值查询数据库，判断是否存在。如果存在，说明已经被处理。文件移动到待删除文件夹，否则移动到待备份文件夹。
        '''
