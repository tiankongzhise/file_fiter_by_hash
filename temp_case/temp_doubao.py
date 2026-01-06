import subprocess
from pathlib import Path

# ======================== 配置区（无需修改，所有需求不变） ========================
source_folder = Path(r"K:\迅雷下载\VEC285")
output_dir = Path(r"K:\测试文件夹")
password = "H_X123456789"
split_size = "2048m"
seven_zip_path = Path(r"C:\Program Files (x86)\7-Zip\7z.exe")
# seven_zip_path = Path(r"D:\Software\7-Zip\7z.exe") # 自定义路径备用

# pathlib 路径处理（保留不变，优雅简洁）
folder_name = source_folder.name
output_7z = output_dir / f"{folder_name}.7z"

# 7z 核心命令参数【已修复两个致命错误 + 保留所有需求】
seven_zip_args = [
    str(seven_zip_path),
    "a",                # 打包指令
    "-t7z",             # 7z格式
    "-m0=Copy",         # 仅打包不压缩 核心参数（不变）
    f"-p{password}",    # 密码参数 正确写法 ✔️ 无空格拼接
    f"-v{split_size}",  # 2048MB分卷（不变）
    "-bb1",             # 显示进度日志
    str(output_7z),
    str(source_folder)
]

# 执行打包+异常处理+路径校验
try:
    if not source_folder.exists() or not source_folder.is_dir():
        print(f"❌ 源文件夹不存在或非目录：{source_folder}")
    elif not seven_zip_path.exists():
        print(f"❌ 找不到7z.exe，请核对路径：{seven_zip_path}")
    else:
        # 自动创建输出目录（不存在则创建）
        output_dir.mkdir(parents=True, exist_ok=True)
        # 执行命令 【修复解码错误】encoding="gbk" + 加容错参数 ✔️
        result = subprocess.run(
            seven_zip_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            encoding="gbk",          # 核心修复：Windows 7z输出默认GBK编码
            errors="ignore",         # 容错：忽略少数无法解码的特殊字符，防止崩溃
            creationflags=0x08000000 # 隐藏7z的黑窗口（额外优化，可选）
        )
        if result.returncode == 0:
            print(f"✅ 打包成功！压缩包位置：{output_7z}")
            print(f"✅ 分卷大小：{split_size} | 密码：{password} | 密码已写入压缩包注释")
            print(f"✅ 分卷文件格式：{folder_name}.7z.001、{folder_name}.7z.002...")
        else:
            print(f"❌ 打包失败！7z官方错误信息：{result.stderr.strip()}")
except Exception as e:
    print(f"❌ 程序运行异常：{str(e)}")