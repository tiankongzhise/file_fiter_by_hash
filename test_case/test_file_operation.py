import pathlib
from file_fiter_by_hash.utils.file_operation import remove_to_pending_backup
from file_fiter_by_hash.utils.file_operation import remove_to_processing
from file_fiter_by_hash.utils.file_operation import remove_to_panding_delete
from file_fiter_by_hash.utils.file_operation import delete_empty_folder
from file_fiter_by_hash.utils.file_operation import remove_to_local_duplicate
from file_fiter_by_hash.config import FileConfig


def test_remove_to_pending_backup():
    target_dir = FileConfig.backup_dir
    if not isinstance(target_dir, pathlib.Path):
        target_dir = pathlib.Path(target_dir)

    # 存在的文件移动测试
    file_name = pathlib.Path(r"E:\迅雷下载")
    target_file_name = target_dir / file_name.name
    file_result = remove_to_pending_backup(file_name)
    assert not file_name.exists()
    assert target_file_name.exists()
    assert file_result is True

    # 存在的文件夹移动测试
    folder_name = pathlib.Path(r"E:\迅雷下载")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_pending_backup(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 不存在的文件移动测试
    not_exist_file_name = pathlib.Path(r"E:\迅雷下载\不存在的文件.txt")
    not_exist_file_result = remove_to_pending_backup(not_exist_file_name)
    assert not not_exist_file_name.exists()
    assert not target_file_name.exists()
    assert not_exist_file_result is False
    
     # 不存在的文件夹移动测试
    not_exist_folder_name = pathlib.Path(r"E:\迅雷下载\不存在的文件夹")
    not_exist_folder_result = remove_to_pending_backup(not_exist_folder_name)
    assert not not_exist_folder_name.exists()
    assert not target_folder_name.exists()
    assert not_exist_folder_result is False


def test_remove_to_processing():
    folder_name = pathlib.Path(r"E:\迅雷下载")
    remove_to_processing(folder_name)


def test_remove_to_panding_delete():
    folder_name = pathlib.Path(r"E:\迅雷下载")
    remove_to_panding_delete(folder_name)


def test_delete_empty_folder():
    folder_name = pathlib.Path(r"E:\迅雷下载")
    delete_empty_folder(folder_name)


def test_remove_to_local_duplicate():
    folder_name = pathlib.Path(r"E:\迅雷下载")
    remove_to_local_duplicate(folder_name)
