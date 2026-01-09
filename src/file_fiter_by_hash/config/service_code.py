from copy import deepcopy

logger_service_code = {
    'L010010011': '日志配置读取成功',
    'L010010012': '日志配置读取失败',
    'L020010011': '数据库初始化成功',
    'L020010012': '数据库初始化失败',
    'L020020011': '日志数据库写入成功',
    'L020020012': '日志数据库写入失败',
}

calculate_hash_service_code = {
    'C010010011': '文件hash计算成功',
    'C010010012': '文件hash计算失败',
    'C020010011': '文件夹hash计算成功',
    'C020010012': '文件夹hash计算失败',
    'C020020011': '超大文件夹,统计文件夹大小成功',
    'C020020012': '超大文件夹,统计文件夹大小失败',
    'C020030011': '空文件夹，无需计算',
    'C010010013': '压缩文件hash计算成功',
    'C010010014': '压缩文件hash计算失败',
}

file_operation_service_code = {
    'F000010011': '移动操作成功，不区分文件或文件夹',
    'F000010012': '移动操作失败，不区分文件或文件夹',
    'F000020011': '删除操作成功，不区分文件或文件夹',
    'F000020012': '删除操作失败，不区分文件或文件夹',
    'F000030011': '压缩操作成功，不区分文件或文件夹',
    'F000030012': '压缩操作失败，不区分文件或文件夹',
    'F010010011': '文件移动成功',
    'F010010012': '文件移动失败',
    'F010020011': '文件删除成功',
    'F010020012': '文件删除失败',
    'F010030011': '文件压缩成功',
    'F010030012': '文件压缩失败',
    'F020010011': '文件夹移动成功',
    'F020010012': '文件夹移动失败',
    'F020020011': '文件夹删除成功',
    'F020020012': '文件夹删除失败',
    'F020020022': '由于业务原因删除文件夹失败',
    'F020030011': '文件夹压缩成功',
    'F020030012': '文件夹压缩失败',
}

# filter_process 流程控制服务代码
filter_process_code = {
    'P010010011': '预分类完成',
    'P010010012': '预分类结果保存成功',
    'P010010013': '预分类结果保存失败',
    'P020010011': '哈希结果保存成功',
    'P020010012': '哈希结果保存失败',
    'P030010011': '压缩结果保存成功',
    'P030010012': '压缩结果保存失败',
    'P040010011': '压缩项目哈希保存成功',
    'P040010012': '压缩项目哈希保存失败',
    'P050010011': '重新压缩成功',
    'P050010012': '重新压缩失败',
    'P050010013': '重新压缩结果保存成功',
    'P050010014': '重新压缩结果保存失败',
    'P060010011': '比较成功',
    'P060010012': '比较失败',
    'P060010013': '比较结果保存成功',
    'P060010014': '比较结果保存失败',
}

all_service_code = {
    **logger_service_code,
    **calculate_hash_service_code,
    **file_operation_service_code,
    **filter_process_code,
}

def trans_mean_to_code():
    return {mean: code for code, mean in all_service_code.items()}

def get_service_code_map():
    temp_dict = deepcopy(all_service_code)
    temp_dict.update(trans_mean_to_code())
    return temp_dict

def get_service_code(service_event: str) -> str:
    code = get_service_code_map().get(service_event)
    if not code:
        raise ValueError(f'服务事件 {service_event} 没有对应的服务代码')
    return code

def get_service_code_mean(service_code: str) -> str:
    mean_code = get_service_code_map().get(service_code)
    if not mean_code:
        raise ValueError(f'服务代码 {service_code} 没有对应的服务事件')
    return mean_code
