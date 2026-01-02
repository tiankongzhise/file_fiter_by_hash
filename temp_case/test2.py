import pathlib
   
folder_path = pathlib.Path(r"L:\动物行为学")
file_count = 0
for file_path in folder_path.rglob('*'):
    if file_path.is_file():
        file_count += 1
print(f"Total files: {file_count}")
