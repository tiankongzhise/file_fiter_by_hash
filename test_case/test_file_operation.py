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
    file_name = pathlib.Path(r"e:\移动文件测试源\测试.txt")
    target_file_name = target_dir / file_name.name
    file_result = remove_to_pending_backup(file_name)
    assert not file_name.exists()
    assert target_file_name.exists()
    assert file_result is True

    # 存在的空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试-空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_pending_backup(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 存在的非空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试 - 非空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_pending_backup(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 不存在的文件移动测试
    not_exist_file_name = pathlib.Path(r"E:\迅雷下载\不存在的文件.txt")
    target_not_exist_file_name = target_dir / not_exist_file_name.name
    not_exist_file_result = remove_to_pending_backup(not_exist_file_name)
    assert not not_exist_file_name.exists()
    assert not target_not_exist_file_name.exists()
    assert not_exist_file_result is False
    
     # 不存在的文件夹移动测试
    not_exist_folder_name = pathlib.Path(r"E:\迅雷下载\不存在的文件夹")
    target_not_exist_folder_name = target_dir / not_exist_folder_name.name
    not_exist_folder_result = remove_to_pending_backup(not_exist_folder_name)
    assert not not_exist_folder_name.exists()
    assert not target_not_exist_folder_name.exists()
    assert not_exist_folder_result is False


def test_remove_to_processing():
    target_dir = FileConfig.processing_dir
    if not isinstance(target_dir, pathlib.Path):
        target_dir = pathlib.Path(target_dir)

    # 存在的文件移动测试
    file_name = pathlib.Path(r"e:\移动文件测试源\测试.txt")
    target_file_name = target_dir / file_name.name
    file_result = remove_to_processing(file_name)
    assert not file_name.exists()
    assert target_file_name.exists()
    assert file_result is True

    # 存在的空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试-空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_processing(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 存在的非空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试 - 非空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_processing(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 不存在的文件移动测试
    not_exist_file_name = pathlib.Path(r"E:\迅雷下载\不存在的文件.txt")
    target_not_exist_file_name = target_dir / not_exist_file_name.name
    not_exist_file_result = remove_to_processing(not_exist_file_name)
    assert not not_exist_file_name.exists()
    assert not target_not_exist_file_name.exists()
    assert not_exist_file_result is False
    
     # 不存在的文件夹移动测试
    not_exist_folder_name = pathlib.Path(r"E:\迅雷下载\不存在的文件夹")
    target_not_exist_folder_name = target_dir / not_exist_folder_name.name
    not_exist_folder_result = remove_to_processing(not_exist_folder_name)
    assert not not_exist_folder_name.exists()
    assert not target_not_exist_folder_name.exists()
    assert not_exist_folder_result is False



def test_remove_to_pending_delete():
    target_dir = FileConfig.duplicate_dir
    if not isinstance(target_dir, pathlib.Path):
        target_dir = pathlib.Path(target_dir)

    # 存在的文件移动测试
    file_name = pathlib.Path(r"e:\移动文件测试源\测试.txt")
    target_file_name = target_dir / file_name.name
    file_result = remove_to_panding_delete(file_name)
    assert not file_name.exists()
    assert target_file_name.exists()
    assert file_result is True

    # 存在的空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试-空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_panding_delete(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 存在的非空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试 - 非空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_panding_delete(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 不存在的文件移动测试
    not_exist_file_name = pathlib.Path(r"E:\迅雷下载\不存在的文件.txt")
    target_not_exist_file_name = target_dir / not_exist_file_name.name
    not_exist_file_result = remove_to_panding_delete(not_exist_file_name)
    assert not not_exist_file_name.exists()
    assert not target_not_exist_file_name.exists()
    assert not_exist_file_result is False
    
     # 不存在的文件夹移动测试
    not_exist_folder_name = pathlib.Path(r"E:\迅雷下载\不存在的文件夹")
    target_not_exist_folder_name = target_dir / not_exist_folder_name.name
    not_exist_folder_result = remove_to_panding_delete(not_exist_folder_name)
    assert not not_exist_folder_name.exists()
    assert not target_not_exist_folder_name.exists()
    assert not_exist_folder_result is False


def test_delete_empty_folder():
    folder_name = pathlib.Path(r"E:\移动文件测试源\存在文件夹测试-空")
    del_result = delete_empty_folder(folder_name)
    assert del_result is True
    
    err_test = pathlib.Path(r"E:\移动文件测试源\存在文件夹测试 - 非空")
    del_result = delete_empty_folder(err_test)
    assert del_result is False


def test_remove_to_local_duplicate():
    target_dir = FileConfig.local_duplicate_dir
    if not isinstance(target_dir, pathlib.Path):
        target_dir = pathlib.Path(target_dir)

    # 存在的文件移动测试
    file_name = pathlib.Path(r"e:\移动文件测试源\测试.txt")
    target_file_name = target_dir / file_name.name
    file_result = remove_to_local_duplicate(file_name)
    assert not file_name.exists()
    assert target_file_name.exists()
    assert file_result is True

    # 存在的空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试-空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_local_duplicate(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 存在的非空文件夹移动测试
    folder_name = pathlib.Path(r"e:\移动文件测试源\存在文件夹测试 - 非空")
    target_folder_name = target_dir / folder_name.name
    folder_result = remove_to_local_duplicate(folder_name)
    assert not folder_name.exists()
    assert target_folder_name.exists()
    assert folder_result is True
    
    # 不存在的文件移动测试
    not_exist_file_name = pathlib.Path(r"E:\迅雷下载\不存在的文件.txt")
    target_not_exist_file_name = target_dir / not_exist_file_name.name
    not_exist_file_result = remove_to_local_duplicate(not_exist_file_name)
    assert not not_exist_file_name.exists()
    assert not target_not_exist_file_name.exists()
    assert not_exist_file_result is False
    
     # 不存在的文件夹移动测试
    not_exist_folder_name = pathlib.Path(r"E:\迅雷下载\不存在的文件夹")
    target_not_exist_folder_name = target_dir / not_exist_folder_name.name
    not_exist_folder_result = remove_to_local_duplicate(not_exist_folder_name)
    assert not not_exist_folder_name.exists()
    assert not target_not_exist_folder_name.exists()
    assert not_exist_folder_result is False



if __name__ == '__main__':
    # test_remove_to_pending_backup()
    # test_remove_to_processing()
    # test_remove_to_pending_delete()
    # test_delete_empty_folder()
    test_remove_to_local_duplicate()
