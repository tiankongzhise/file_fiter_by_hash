import pathlib
import json
from .calculate_hash import calculate_folder_hash, calculate_file_hash
from .schmeas import HashParams, HashResult
from tqdm import tqdm


def get_all_items(folder_path: pathlib.Path) -> list[dict[str, pathlib.Path]]:
    """获取文件夹下所有文件和子文件夹"""
    all_items = {"files": [], "dirs": []}
    for item in folder_path.iterdir():
        if item.is_file():
            all_items["files"].append(item)
        elif item.is_dir():
            all_items["dirs"].append(item)
    return all_items


def save_hash_result(hash_result: HashResult, save_path: pathlib.Path = None):
    """保存哈希结果到文件"""
    if save_path is None:
        save_path = pathlib.Path(r"./hash_result")
    success_result = save_path / "success.json"
    error_result = save_path / "err.json"
    empty_result = save_path / "empty.json"
    big_folder_result = save_path / "big_folder.json"

    success_result.parent.mkdir(parents=True, exist_ok=True)
    error_result.parent.mkdir(parents=True, exist_ok=True)
    empty_result.parent.mkdir(parents=True, exist_ok=True)
    big_folder_result.parent.mkdir(parents=True, exist_ok=True)

    match hash_result.status:
        case "success":
            with open(success_result, "a", encoding="utf-8") as f:
                json.dump(hash_result.model_dump(), f, ensure_ascii=False, indent=4)
        case "error":
            with open(error_result, "a", encoding="utf-8") as f:
                json.dump(hash_result.model_dump(), f, ensure_ascii=False, indent=4)
        case "empty":
            with open(empty_result, "a", encoding="utf-8") as f:
                json.dump(hash_result.model_dump(), f, ensure_ascii=False, indent=4)
        case "big_folder":
            with open(big_folder_result, "a", encoding="utf-8") as f:
                json.dump(hash_result.model_dump(), f, ensure_ascii=False, indent=4)
        case _:
            print(f"Unknown status: {hash_result.status},hash_result:{hash_result}")
    return True


def main(target_folder: str):
    folder_path = pathlib.Path(target_folder)
    all_items = get_all_items(folder_path)
    print(f"items:{len(all_items['files']) + len(all_items['dirs'])}")
    for item in tqdm(all_items["files"], desc="files"):
        hash_result = calculate_file_hash(
            HashParams(folder_path=item, algorithm=["sha1", "sha256", "md5"])
        )
        save_hash_result(hash_result)
    for item in tqdm(all_items["dirs"], desc="dirs"):
        hash_result = calculate_folder_hash(
            HashParams(folder_path=item, algorithm=["sha1", "sha256", "md5"])
        )
        save_hash_result(hash_result)
    print("done")


if __name__ == "__main__":
    main(r"L:\动物行为学")
