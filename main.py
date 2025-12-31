import hashlib
import json
import time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from os import cpu_count

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

def process_single_file(args):
    """处理单个文件，返回结果"""
    file_path, = args
    try:
        path = Path(file_path)
        file_name = path.name
        file_ext = path.suffix or "unknown"
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
    folder_path = Path("L:\动物行为学")  # 替换为您的文件夹路径
    output_json = "test.json"

    # 验证文件夹路径
    if not folder_path.is_dir():
        raise ValueError(f"Invalid folder path: {folder_path}")

    results = []
    start_time = time.time()

    # 处理文件夹（第一层级）- 计算文件夹哈希
    folder_hash = process_single_file((str(folder_path),))
    if folder_hash:
        folder_hash["type"] = "folder"
        folder_hash["name"] = folder_path.name
        results.append(folder_hash)
        print(f"Folder: {folder_hash['name']}")
        print(f"  SHA256: {folder_hash['sha256'][:16]}...")
        print(f"  MD5: {folder_hash['md5'][:16]}...")

    # 获取第一层级文件列表
    file_paths = [str(p) for p in folder_path.iterdir() if p.is_file()]

    total_files = len(file_paths)
    processed_count = 0

    print(f"\nTotal files to process: {total_files}\n")

    # 使用ProcessPoolExecutor处理文件
    if file_paths:
        num_processes = min(cpu_count() or 1, 8)

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