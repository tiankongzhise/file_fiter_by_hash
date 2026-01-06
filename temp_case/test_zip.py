# 示例使用
from file_fiter_by_hash.service.zip_file import create_encrypted_7z_volumes, get_archive_comment
from pathlib import Path

if __name__ == "__main__":
    # 需要先安装py7zr库: pip install py7zr
    
    source_folder = Path("test_folder")  # 要打包的文件夹
    output_prefix = "encrypted_archive"  # 输出文件前缀
    password = "my_secret_password"  # 加密密码
    max_size_mb = 5  # 每个分卷最大5MB
    
    # 创建测试文件夹和文件
    source_folder.mkdir(exist_ok=True)
    # 创建几个测试文件，总大小超过限制以测试分卷功能
    for i in range(3):
        file_path = source_folder / f"test_file_{i}.txt"
        # 创建较大的文件以测试分卷
        with open(file_path, "w", encoding="utf-8") as f:
            # 创建较大内容以测试分卷
            f.write("这是测试文件内容 " * 100000)  # 创建较大内容以测试分卷
    
    # 打包并加密
    try:
        print(f"开始创建分卷加密7z文件，每个分卷最大 {max_size_mb} MB...")
        create_encrypted_7z_volumes(source_folder, output_prefix, password, max_size_mb)
        
        # 列出生成的文件
        import glob
        generated_files = glob.glob(f"{output_prefix}_part*.7z")
        print(f"生成了 {len(generated_files)} 个分卷文件:")
        for file in sorted(generated_files):
            size_mb = Path(file).stat().st_size / (1024 * 1024)
            print(f"  - {file} ({size_mb:.2f} MB)")
        
        # 测试解压第一个分卷（注意：实际使用时需要所有分卷文件在同目录下）
        extract_folder = Path("extracted_folder")
        extract_folder.mkdir(exist_ok=True)
        
        if generated_files:
            first_archive = generated_files[0]
            comment = get_archive_comment(first_archive, password)
            print(f"\n从第一个分卷获取的注释: {comment}")
            
    except Exception as e:
        print(f"操作失败: {e}")
        import traceback
        traceback.print_exc()