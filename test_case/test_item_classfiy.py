from file_fiter_by_hash.service.classfiy_item import classify_item
from pathlib import Path


def test_zip_file(item_path):
    result = classify_item(item_path)
    print(f'test_zip_file result = {result}')
    assert result[item_path] == 'zip_file'

def test_big_file(item_path):
    result = classify_item(item_path)
    print(f'test_big_file result = {result}')
    assert result[item_path] == 'big_file'

def test_normal_file(item_path):
    result = classify_item(item_path)
    print(f'test_normal_file result = {result}')
    assert result[item_path] == 'normal_file'

def test_empty_folder(item_path):
    result = classify_item(item_path)
    print(f'test_empty_folder result = {result}')
    assert result[item_path] == 'empty_folder'

def test_folder_exceed_count(item_path):
    result = classify_item(item_path)
    print(f'test_folder_exceed_count result = {result}')
    assert result[item_path] == 'folder_exceed_count'

def test_folder_exceed_size(item_path):
    result = classify_item(item_path)
    print(f'test_folder_exceed_size result = {result}')
    assert result[item_path] == 'folder_oversize'

def test_folder_normal(item_path):
    result = classify_item(item_path)
    print(f'test_folder_normal result = {result}')  
    assert result[item_path] == 'normal_folder'


if __name__ == '__main__':
    print('start test')
    zip_file_path = Path(r'e:\BaiduNetdiskDownload\数字人\SadTalker.rar')
    big_file_path = Path(r'E:\FreeBNS--RU.zip')
    normal_file_path = Path(r'e:\B站视频下载\【民国风采】有趣的民国药品广告唱片《新星三宝歌》头段\1-【民国风采】有趣的民国药品广告唱片《新星三宝歌》头段-1080P 高清-AVC.mp4')
    empty_folder_path = Path(r'E:\移动文件测试源')
    folder_exceed_count_path = Path(r'E:\codeup')
    folder_exceed_size_path = Path(r'E:\迅雷下载')
    folder_normal_path = Path(r'E:\B站视频下载')

    test_zip_file(zip_file_path)
    test_big_file(big_file_path)
    test_normal_file(normal_file_path)
    test_empty_folder(empty_folder_path)
    test_folder_exceed_count(folder_exceed_count_path)
    test_folder_exceed_size(folder_exceed_size_path)
    test_folder_normal(folder_normal_path)
