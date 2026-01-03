import pathlib
def calculate_big_folder_size(file_list:list[str]) -> int:
    """计算给定的文件列表中所有文件的大小，不允许列表内包含文件夹"""
    size = 0
    err_tag = False
    file_list = []
    for item in file_list:
        if pathlib.Path(item).is_dir():
            file_list.append(item)
            err_tag = True
        elif pathlib.Path(item).is_file():
            size += pathlib.Path(item).stat().st_size
            
    if err_tag:
        raise ValueError(f'文件列表存在异常，有文件夹{','.join(file_list)}混在其中，建议排查代码')
    return size
