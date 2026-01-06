import subprocess
from pathlib import Path
import locale

# 配置路径和参数
source_folder = Path(r'K:\迅雷下载\VEC285')
output_folder = Path(r'K:\测试文件夹')
archive_name = 'VEC285.7z'
password = 'H_X123456789'
volume_size = '2048m'

# 自动获取系统默认编码（中文 Windows 通常是 cp936）
system_encoding = locale.getpreferredencoding()

# 确保输出目录存在
output_folder.mkdir(parents=True, exist_ok=True)

# 7-Zip 可执行文件路径（请根据实际安装位置调整）
seven_zip_exe = Path(r'C:\Program Files (x86)\7-Zip\7z.exe')

# 创建临时注释文件（包含密码）
comment_file = output_folder / 'comment.txt'
comment_file.write_text(password, encoding='utf-8')

# 构建 7z 命令
cmd = [
    str(seven_zip_exe),
    'a',
    '-t7z',
    '-mx=0',                    # 仅存储，不压缩
    f'-v{volume_size}',         # 分卷大小
    f'-p{password}',            # 设置密码
    '-mhe=on',                  # 加密文件名
    '-scsUTF-8',                # 注释编码
    str(output_folder / archive_name),
    str(source_folder)
]

# 执行命令
try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding=system_encoding)
    print("✅ 压缩成功！")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ 压缩失败：")
    print(e.stderr)
finally:
    # 清理临时注释文件
    if comment_file.exists():
        comment_file.unlink()