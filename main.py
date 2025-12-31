import os
import hashlib
import json
import multiprocessing
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from concurrent.futures import ProcessPoolExecutor, as_completed

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

def process_single_file(args):
    """处理单个文件，返回结果"""
    file_path, = args
    try:
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1] or "unknown"
        sha256 = calculate_hash(file_path, 'sha256')
        md5 = calculate_hash(file_path, 'md5')
        return {
            "name": file_name,
            "type": file_ext,
            "sha256": sha256,
            "md5": md5
        }
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return None

def main():
    """主程序入口"""
    # 配置参数
    folder_path = "L:\动物行为学"  # 替换为您的文件夹路径
    output_json = "test.json"

    # 验证文件夹路径
    if not os.path.isdir(folder_path):
        raise ValueError(f"Invalid folder path: {folder_path}")

    results = []
    start_time = time.time()

    # 处理文件夹（第一层级）- 计算文件夹哈希
    folder_hash = process_single_file((folder_path,))
    if folder_hash:
        folder_hash["type"] = "folder"
        folder_hash["name"] = os.path.basename(folder_path)
        results.append(folder_hash)
        print(f"Folder: {folder_hash['name']}")
        print(f"  SHA256: {folder_hash['sha256'][:16]}...")
        print(f"  MD5: {folder_hash['md5'][:16]}...")

    # 获取第一层级文件列表
    file_paths = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            file_paths.append(item_path)

    total_files = len(file_paths)
    processed_count = 0

    print(f"\nTotal files to process: {total_files}\n")

    # 使用ProcessPoolExecutor处理文件
    if file_paths:
        num_processes = min(multiprocessing.cpu_count(), 8)

        with ProcessPoolExecutor(max_workers=num_processes) as executor:
            # 提交所有任务
            futures = {executor.submit(process_single_file, (fp,)): fp for fp in file_paths}

            # 使用as_completed获取结果并显示进度条
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

                processed_count += 1
                progress = processed_count / total_files
                bar_length = 40
                filled_length = int(bar_length * progress)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                percent = progress * 100

                # 清除行并重新绘制进度条
                print(f'\r进度: |{bar}| {percent:5.1f}% ({processed_count}/{total_files})', end='', flush=True)

        print()  # 换行

    # 写入JSON文件
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults written to {output_json}")

    elapsed_time = time.time() - start_time
    print(f"\nAll processing completed successfully!")
    print(f"Total time: {elapsed_time:.2f}s | Files: {total_files} | Speed: {total_files/elapsed_time:.2f} files/s")

if __name__ == "__main__":
    main()