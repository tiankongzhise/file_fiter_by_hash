
import pathlib
from ..logger import logger
from ..utils import calculate_folder_size,get_all_file_path
from ..utils.file_operation import remove_to_pending_backup,remove_to_processing,delete_empty_folder,remove_to_panding_delete,remove_to_local_duplicate
from ..utils.dto import transform_special_folder_list_to_dict
from ..mysql_db.query_item import get_all_special_folder,query_item_by_hash,is_temp_hash_table
from ..calculate_hash import calculate_file_hash,calculate_folder_hash

class FilterFile:
    def __init__(self, file_path: str|pathlib.Path):
        self.file_path = file_path if isinstance(file_path, pathlib.Path) else pathlib.Path(file_path)
        self.logger = logger
        self.file_list:list[pathlib.Path] = []
        self.folder_list:list[pathlib.Path] = []
        self.normal_folder_list:list[dict[pathlib.Path,list[pathlib.Path|str]]] = []
        self.big_folder_list:list[dict[pathlib.Path,list[pathlib.Path|str]]] = []
        self.empty_folder_list:list[pathlib.Path] = []
           
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
        步骤三：处理超大文件夹类，从特殊文件夹数据库，拉取全部数据。
        然后在本地比对名称和文件大小是否一致，一致说明已经被处理。文件夹移动到待删除文件夹，
        否则比较本次临时hash表,如果没有记录,移动到待处理文件夹,如果有记录，移动到本地冲突待删除文件夹
        '''
        # 从特殊文件夹数据库，拉取全部数据
        special_folder_squeue = get_all_special_folder()
        special_folder_dict = transform_special_folder_list_to_dict(special_folder_squeue)
        for big_folder in self.big_folder_list:
            folder_name = list(big_folder.keys())[0]
            folder_size = calculate_folder_size(big_folder[folder_name])
            # 如果已经在临时hash表中，说明在之前的处理中已经处理过该文件夹，应当放入本地冲突解决文件夹。这种情况不应该发生，应当记录warning日志。
            if is_temp_hash_table(name = folder_name.name,size=folder_size):
                self.logger.warning(f'大文件夹{folder_name}已经在临时hash表中，这是不正常的')
                remove_to_local_duplicate(folder_name)
                continue
            # 如果文件名称不再特殊文件夹数据库中，说明是新的大文件夹，应当移动到待处理文件夹
            if folder_name.name not in special_folder_dict.keys():
                remove_to_processing(folder_name)
                continue
             # 如果文件名在特殊文件夹数据库中，且文件夹大小与数据库中一致，说明是一个文件夹，删去即可
            if folder_size == special_folder_dict[folder_name]:
                remove_to_panding_delete(folder_name)
                continue
            # 如果文件名在特殊文件夹数据库中，但文件夹大小与数据库中不一致，说明是一个新的文件夹，应当移动到待处理文件夹    
            remove_to_processing(folder_name)
    def step_four(self):
        '''
        步骤四：处理空文件夹类，直接删除文件夹
        '''
        for folder in self.empty_folder_list:
            delete_empty_folder(folder)
        
    def step_five(self):
        '''
        步骤五：处理普通文件夹类，根据哈希值查询数据库，判断是否存在。如果存在，说明已经被处理。文件夹移动到待删除文件夹，否则移动到待备份文件夹。
        '''
        for folder in self.normal_folder_list:
            folder_path = list(folder.keys())[0]
            hash_result = calculate_folder_hash(folder_path)
            sha1 = hash_result.info.hash_info['sha1']
            sha256 = hash_result.info.hash_info['sha256']
            md5 = hash_result.info.hash_info['md5']
            if is_temp_hash_table(hash_tag=f'{sha1}-{sha256}-{md5}'):
                self.logger.warning(f'普通文件夹{folder_path}已经在临时hash表中，这是不正常的')
                remove_to_local_duplicate(folder_path)
                continue
            query_result = query_item_by_hash(sha1,sha256,md5)
            if query_result is None:
                self.logger.warning(f'文件夹{folder_path}哈希值查询数据库失败，请注意')
                remove_to_processing(folder_path)
            if query_result:
                remove_to_panding_delete(folder_path)
            else:
                remove_to_pending_backup(folder_path)
            
            
    def step_six(self):
        '''
        步骤六：处理文件，根据哈希值查询数据库，判断是否存在。如果存在，说明已经被处理。文件移动到待删除文件夹，否则移动到待备份文件夹。
        '''
        for file in self.file_list:
            hash_result = calculate_file_hash(file)
            sha1 = hash_result.info.hash_info['sha1']
            sha256 = hash_result.info.hash_info['sha256']
            md5 = hash_result.info.hash_info['md5']
            if is_temp_hash_table(hash_tag=f'{sha1}-{sha256}-{md5}'):
                self.logger.info(f'{file}已经在临时hash表中，可能是名称不同的同一个文件,转移到本地冲突解决文件夹')
                remove_to_local_duplicate(file)
                continue
            query_result = query_item_by_hash(sha1,sha256,md5)
            if query_result is None:
                self.logger.warning(f'文件{file}哈希值查询数据库失败，请注意')
                remove_to_processing(file)
            if query_result:
                remove_to_panding_delete(file)
            else:
                remove_to_pending_backup(file)
    
    def run(self):
        self.step_one()
        self.step_two()
        self.step_three()
        self.step_four()
        self.step_five()
        self.step_six()
