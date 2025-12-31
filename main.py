import os
import hashlib
import json
import multiprocessing
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple

def calculate_hash(file_path: str, algorithm: str) -> str:
    """计算文件的指定算法Hash值（仅支持sha256和md5）"""
    if algorithm == 'sha256':
        hash_func = hashlib.sha256
    elif algorithm == 'md5':
        hash_func = hashlib.md5
    else:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    hash_obj = hash_func()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def process_file(file_path: str, queue: multiprocessing.Queue):
    """处理单个文件：计算Hash并发送到队列"""
    try:
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1] or "unknown"
        
        # 计算两种Hash
        sha256 = calculate_hash(file_path, 'sha256')
        md5 = calculate_hash(file_path, 'md5')
        
        # 构建结果字典
        result = {
            "name": file_name,
            "type": file_ext,  # 文件后缀
            "sha256": sha256,
            "md5": md5
        }
        queue.put(result)
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
def calculate_file_hash(file_path: Path, algorithm: str = 'sha256') -> str:
    """计算单个文件的哈希值"""
    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def calculate_folder_hash(folder_path: str | Path, algorithm: str = 'sha256') -> str:
    """
    计算文件夹的哈希值（使用pathlib实现，不依赖os）
    
    参数:
    folder_path: 文件夹路径（字符串或Path对象）
    algorithm: 哈希算法（默认sha256）
    
    返回:
    文件夹哈希值（十六进制字符串）
    """
    folder = Path(folder_path)
    
    # 检查是否为目录
    if not folder.is_dir():
        raise ValueError(f"路径 '{folder}' 不是目录")
    
    # 获取所有文件（递归遍历，排除目录）
    files = [f for f in folder.rglob('*') if f.is_file()]
    
    # 按相对路径排序（确保顺序一致）
    files.sort(key=lambda x: str(x.relative_to(folder)))
    
    # 计算每个文件的哈希
    file_hashes = [calculate_file_hash(file, algorithm) for file in files]
    
    # 将所有文件哈希连接后计算总哈希
    combined = ''.join(file_hashes)
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(combined.encode('utf-8'))
    return hash_obj.hexdigest()

def process_folder(folder_path: str, queue: multiprocessing.Queue):
    """处理文件夹：记录文件夹信息（不计算Hash）"""
    try:
        sha256 = calculate_folder_hash(folder_path, 'sha256')
        md5 = calculate_folder_hash(folder_path, 'md5')
        queue.put({
            "name": os.path.basename(folder_path),
            "type": "folder",
            "sha256": sha256,
            "md5": md5
        })
    except Exception as e:
        print(f"Error processing folder {folder_path}: {str(e)}")

def record_results(queue: multiprocessing.Queue, output_file: str):
    """异步记录结果到JSON文件"""
    results = []
    while True:
        item = queue.get()
        if item is None:  # 结束标记
            break
        results.append(item)
    
    # 写入JSON文件
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Results written to {output_file}")

def main():
    """主程序入口"""
    # 配置参数
    folder_path = "L:\动物行为学"  # 替换为您的文件夹路径
    output_json = "test.json"
    
    # 验证文件夹路径
    if not os.path.isdir(folder_path):
        raise ValueError(f"Invalid folder path: {folder_path}")
    
    # 创建进程间队列
    queue = multiprocessing.Queue()
    
    # 启动记录进程
    recorder = multiprocessing.Process(
        target=record_results, 
        args=(queue, output_json)
    )
    recorder.start()
    
    # 处理文件夹（第一层级）
    process_folder(folder_path, queue)
    
    # 获取第一层级文件列表
    file_paths = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_paths.append(item_path)
    
    # 启动多进程计算
    if file_paths:
        num_processes = min(multiprocessing.cpu_count(), 8)  # 限制最大进程数
        chunk_size = max(1, len(file_paths) // num_processes)
        
        processes = []
        for i in range(num_processes):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, len(file_paths))
            chunk = file_paths[start:end]
            
            p = multiprocessing.Process(
                target=process_file, 
                args=(chunk, queue) if isinstance(chunk, list) else (chunk, queue)
            )
            p.start()
            processes.append(p)
        
        # 等待所有计算进程完成
        for p in processes:
            p.join()
    
    # 发送结束标记
    queue.put(None)
    
    # 等待记录进程完成
    recorder.join()
    
    print("All processing completed successfully!")

if __name__ == "__main__":
    main()