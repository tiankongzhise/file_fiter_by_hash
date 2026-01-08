from datetime import timezone,datetime


# ✅ 抽离公共工具方法，可全局复用
def get_current_timestamp(ms: bool = True) -> int:
    """获取当前时间戳，默认毫秒级，ms=False则返回秒级"""
    if ms:
        return int(datetime.now().timestamp() * 1000)
    return int(datetime.now().timestamp())

def timestamp_to_local_time(ts: int, fmt: str = "%Y-%m-%d %H:%M:%S", ms: bool = True) -> str | None:
    """
    时间戳转本地时区格式化时间
    :param ts: 时间戳(秒/毫秒)
    :param fmt: 格式化字符串，默认：年-月-日 时:分:秒
    :param ms: 是否是毫秒级时间戳
    :return: 本地时间字符串 / None
    """
    if not ts:
        return None
    _ts = ts / 1000 if ms else ts
    # 强制转【本地时区】，杜绝时区偏差
    local_dt = datetime.fromtimestamp(_ts).astimezone(timezone.utc).astimezone()
    # 如果是毫秒级时间戳,应当显示毫秒部分
    if ms:
        fmt += ".%f"
    return local_dt.strftime(fmt)[:-3] if ms else local_dt.strftime(fmt)
