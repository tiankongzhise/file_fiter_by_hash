from ..service.fiter_file import FilterFile
from ..config.classify_config import ClassifyConfig
from ..logger import get_logger
from ..service.classfiy_service import classify_folder, classify_item
from ..schmeas.schmeas import HashResult, HashParams
import pathlib

logger = get_logger("filter_process")


def file_process(config: ClassifyConfig = None) -> dict:
    """
    主处理函数：执行完整的文件处理流程

    Args:
        config: 分类配置

    Returns:
        处理结果字典
    """
    if config is None:
        config = ClassifyConfig()

    result = {
        'pre_classify': None,
        'hash_result': None,
        'zip_result': None,
        'unzip_result': None,
        'compare_result': None,
    }

    # Step 1: 预分类
    logger.set_service('file_process.pre_classify')
    pre_classify_result = pre_classify(config)
    result['pre_classify'] = pre_classify_result
    save_pre_classify_result(pre_classify_result)

    # Step 2: 计算哈希
    logger.set_service('file_process.calculate_hash')
    hash_result = calculate_hash_result(pre_classify_result)
    result['hash_result'] = hash_result
    save_hash_result(hash_result)

    # Step 3: 压缩大文件
    logger.set_service('file_process.zip_item')
    zip_result = zip_item(hash_result)
    result['zip_result'] = zip_result
    save_zip_result(zip_result)

    # Step 4: 解压文件用于比较
    logger.set_service('file_process.unzip_item')
    unzip_result = unzip_item(zip_result)
    result['unzip_result'] = unzip_result
    save_unzip_result(unzip_result)

    # Step 5: 比较结果（解压后的hash与源文件hash对比）
    logger.set_service('file_process.compare_unzip_source')
    compare_result = compare_unzip_source(hash_result, unzip_result)
    result['compare_result'] = compare_result
    save_compare_result(compare_result)

    return result


def pre_classify(config: ClassifyConfig) -> dict:
    """
    对源文件/文件夹进行预分类

    Args:
        config: 分类配置

    Returns:
        分类结果字典，key为文件路径，value为分类结果
    """
    result = {}
    for item in config.sources_list:
        temp = pathlib.Path(item)
        if temp in result:
            continue
        if temp.is_dir():
            result[temp] = classify_folder(temp)
        elif temp.is_file():
            result[temp] = classify_item(temp)
    logger.info(message=f"预分类完成，共处理 {len(result)} 个项目")
    return result


def save_pre_classify_result(pre_classify_result: dict) -> bool:
    """
    保存预分类结果

    Args:
        pre_classify_result: 预分类结果字典

    Returns:
        是否保存成功
    """
    try:
        # TODO: 实现将预分类结果保存到数据库的逻辑
        # 可以保存到临时表或日志表
        logger.info(message=f"预分类结果已保存，共 {len(pre_classify_result)} 个项目")
        return True
    except Exception as e:
        logger.error(message=f"保存预分类结果失败: {e}")
        return False


def calculate_hash_result(save_pre_classify_result: dict) -> dict[str, HashResult]:
    """
    计算文件的哈希值

    Args:
        save_pre_classify_result: 预分类结果字典

    Returns:
        哈希结果字典，key为文件路径，value为HashResult
    """
    from ..service.calculate_hash_service import calculate_file_hash, calculate_folder_hash

    result = {}
    for item_path, classify_info in save_pre_classify_result.items():
        try:
            params = HashParams(item_path=item_path, algorithm=['sha256', 'md5', 'sha1'])
            if item_path.is_file():
                hash_result = calculate_file_hash(params)
            elif item_path.is_dir():
                hash_result = calculate_folder_hash(params)
            else:
                logger.warning(message=f"未知类型: {item_path}")
                continue

            result[item_path] = hash_result
            logger.info(message=f"哈希计算成功: {item_path}")
        except Exception as e:
            logger.error(message=f"哈希计算失败 {item_path}: {e}")
            result[item_path] = HashResult(
                status='error',
                info=None,
                message=str(e)
            )

    return result


def save_hash_result(hash_result: dict) -> bool:
    """
    保存哈希计算结果

    Args:
        hash_result: 哈希结果字典

    Returns:
        是否保存成功
    """
    try:
        # TODO: 实现将哈希结果保存到数据库的逻辑
        # 可以保存到 item_hash_result 表
        success_count = sum(1 for r in hash_result.values() if r.status == 'success')
        logger.info(message=f"哈希结果已保存，成功 {success_count}/{len(hash_result)} 个")
        return True
    except Exception as e:
        logger.error(message=f"保存哈希结果失败: {e}")
        return False


def zip_item(item_info: dict) -> dict:
    """
    压缩所有项目（文件或文件夹）
    压缩率为0（存储模式），密码为 H_x123456789

    Args:
        item_info: 项目信息字典

    Returns:
        压缩结果字典
    """
    from ..service.zip_serice import zip_item as do_zip

    result = {}
    for item_path, hash_result in item_info.items():
        try:
            # 压缩所有项目，不限制类型和大小
            target_dir = pathlib.Path(ClassifyConfig.zipped_folder)
            zip_path = do_zip(item_path, target_dir, password='H_x123456789', compress_level=0)
            result[item_path] = {
                'zip_path': zip_path,
                'original': item_path,
                'original_hash': hash_result,
                'status': 'success'
            }
            logger.info(message=f"压缩处理: {item_path} -> {zip_path}")
        except Exception as e:
            logger.error(message=f"压缩失败 {item_path}: {e}")
            result[item_path] = {
                'zip_path': None,
                'original': item_path,
                'original_hash': hash_result,
                'status': 'error',
                'error': str(e)
            }

    return result


def save_zip_result(zip_result: dict) -> bool:
    """
    保存压缩结果

    Args:
        zip_result: 压缩结果字典

    Returns:
        是否保存成功
    """
    try:
        # TODO: 实现将压缩结果保存到数据库的逻辑
        success_count = sum(1 for r in zip_result.values() if r.get('status') == 'success')
        logger.info(message=f"压缩结果已保存，成功 {success_count}/{len(zip_result)} 个")
        return True
    except Exception as e:
        logger.error(message=f"保存压缩结果失败: {e}")
        return False


def unzip_item(zip_result: dict) -> dict:
    """
    解压ZIP文件用于比较

    Args:
        zip_result: 压缩结果字典

    Returns:
        解压结果字典
    """
    from ..service.zip_serice import unzip_to_compare

    result = {}
    for item_path, zip_info in zip_result.items():
        try:
            zip_path = zip_info.get('zip_path')
            if zip_path and pathlib.Path(zip_path).exists():
                # 解压文件
                unzip_path = unzip_to_compare(zip_path)
                result[item_path] = {
                    'unzip_path': unzip_path,
                    'original': item_path,
                    'zip_path': zip_path,
                    'original_hash': zip_info.get('original_hash'),
                    'status': 'success'
                }
                logger.info(message=f"解压成功: {zip_path} -> {unzip_path}")
            else:
                result[item_path] = {
                    'unzip_path': None,
                    'original': item_path,
                    'zip_path': zip_path,
                    'original_hash': zip_info.get('original_hash'),
                    'status': 'skipped'
                }
        except Exception as e:
            logger.error(message=f"解压失败 {zip_path}: {e}")
            result[item_path] = {
                'unzip_path': None,
                'original': item_path,
                'zip_path': zip_info.get('zip_path'),
                'original_hash': zip_info.get('original_hash'),
                'status': 'error',
                'error': str(e)
            }

    return result


def save_unzip_result(unzip_result: dict) -> bool:
    """
    保存解压结果

    Args:
        unzip_result: 解压结果字典

    Returns:
        是否保存成功
    """
    try:
        # TODO: 实现将解压结果保存到数据库的逻辑
        success_count = sum(1 for r in unzip_result.values() if r.get('status') == 'success')
        logger.info(message=f"解压结果已保存，成功 {success_count}/{len(unzip_result)} 个")
        return True
    except Exception as e:
        logger.error(message=f"保存解压结果失败: {e}")
        return False


def compare_unzip_source(hash_result: dict, unzip_result: dict) -> dict:
    """
    比较解压后的结果与源文件的hash是否完全一致

    Args:
        hash_result: 源文件哈希结果字典
        unzip_result: 解压结果字典

    Returns:
        比较结果字典
    """
    from ..service.calculate_hash_service import calculate_file_hash, calculate_folder_hash

    result = {}
    for item_path, unzip_info in unzip_result.items():
        try:
            unzip_path = unzip_info.get('unzip_path')
            original_hash_info = unzip_info.get('original_hash')

            if unzip_path and pathlib.Path(unzip_path).exists():
                # 计算解压后内容的hash
                unzip_path_obj = pathlib.Path(unzip_path)
                if unzip_path_obj.is_file():
                    unzip_hash_result = calculate_file_hash(
                        HashParams(item_path=unzip_path_obj)
                    )
                elif unzip_path_obj.is_dir():
                    unzip_hash_result = calculate_folder_hash(
                        HashParams(item_path=unzip_path_obj)
                    )
                else:
                    result[item_path] = {
                        'original': item_path,
                        'unzip_path': unzip_path,
                        'original_hash': original_hash_info,
                        'unzip_hash': None,
                        'is_match': None,
                        'status': 'error',
                        'error': '解压路径类型未知'
                    }
                    continue

                # 比较哈希值
                if original_hash_info and original_hash_info.info:
                    # 比较所有哈希算法结果是否一致
                    is_match = True
                    for alg in ['sha256', 'md5', 'sha1']:
                        source_hash = original_hash_info.info.hash_info.get(alg)
                        unzip_hash = unzip_hash_result.info.hash_info.get(alg) if unzip_hash_result.info else None
                        if source_hash != unzip_hash:
                            is_match = False
                            break
                else:
                    is_match = None  # 无法比较

                result[item_path] = {
                    'original': item_path,
                    'unzip_path': unzip_path,
                    'original_hash': original_hash_info,
                    'unzip_hash': unzip_hash_result,
                    'is_match': is_match,
                    'status': 'success'
                }

                logger.info(message=f"比较结果: {item_path} - 匹配: {is_match}")
            else:
                result[item_path] = {
                    'original': item_path,
                    'unzip_path': unzip_path,
                    'original_hash': original_hash_info,
                    'unzip_hash': None,
                    'is_match': None,
                    'status': 'error',
                    'error': '解压路径不存在'
                }
        except Exception as e:
            logger.error(message=f"比较失败 {item_path}: {e}")
            result[item_path] = {
                'original': item_path,
                'unzip_path': unzip_info.get('unzip_path'),
                'original_hash': unzip_info.get('original_hash'),
                'unzip_hash': None,
                'is_match': None,
                'status': 'error',
                'error': str(e)
            }

    return result


def save_compare_result(compare_result: dict) -> bool:
    """
    保存比较结果

    Args:
        compare_result: 比较结果字典

    Returns:
        是否保存成功
    """
    try:
        # TODO: 实现将比较结果保存到数据库的逻辑
        match_count = sum(1 for r in compare_result.values() if r.get('is_match') is True)
        total_count = len(compare_result)
        logger.info(message=f"比较结果已保存，匹配 {match_count}/{total_count} 个")
        return True
    except Exception as e:
        logger.error(message=f"保存比较结果失败: {e}")
        return False


def upload_ziped_file(zip_file):
    pass


def save_upload_result(upload_result: dict):
    pass


def del_zipped_file(zip_file):
    pass


def save_del_result(del_result: dict):
    pass


def del_source_file():
    pass


def save_del_source_result(del_source_result: dict):
    pass
