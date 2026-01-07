import pathlib
from os import PathLike

def calculate_item_size(item:PathLike) -> int:
    """计算给定的文件或文件夹的大小"""
    size = 0
    item = pathlib.Path(item)
    if not item.exists():
        raise ValueError(f'{item}不存在')
    try:
        if item.is_file():
            return item.stat().st_size
        elif item.is_dir():
            for temp_item in item.rglob('*'):
                if temp_item.is_file():
                    size += temp_item.stat().st_size
            return size
    except Exception as e:
        raise ValueError(f'计算{item}大小时出现异常：{e}')
