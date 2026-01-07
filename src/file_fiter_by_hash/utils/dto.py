from ..mysql_db.models import SpecialFolderTable,FileOperationRecordTable
from ..schmeas import FileOperationRecord
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
def trans_file_operation_dto_to_dao(file_operation_record: FileOperationRecord):
    return FileOperationRecordTable(
        operation=file_operation_record.operation,
        source_path=file_operation_record.source_path.as_posix(),
        target_path=file_operation_record.target_path.as_posix(),
        file_name=file_operation_record.file_name,
        file_type=file_operation_record.file_type,
        hash_info=file_operation_record.hash_info,
        operation_status=file_operation_record.operation_status,
        error_message=file_operation_record.error_message,
    )
