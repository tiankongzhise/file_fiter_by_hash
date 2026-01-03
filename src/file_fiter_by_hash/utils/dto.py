from ..mysql_db.models import SpecialFolderTable
from typing import Iterable


def transform_special_folder_to_dict(special_folder: SpecialFolderTable):
    return {
        'name': special_folder.name,
        'size': special_folder.size,
    }
def transform_special_folder_list_to_dict(special_folder_list: Iterable[SpecialFolderTable]):
    result = {}
    for item in special_folder_list:
        result[item.name] = item.size
    return result
