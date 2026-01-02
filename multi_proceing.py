from multiprocessing import Process
from multiprocessing import Manager  # ✅ 修复1：直接导入原生Manager，无需注册
from mysql_db.save_result import save_item_hash_result
from mysql_db.models import ItemHashResult
from mysql_db.init_db import reset_db
from logger import get_logger
import random
import time

# 生产测试数据（你的业务逻辑，未修改）
def create_test_data(data_number: int = 1):
    test_data = []
    for i in range(data_number):
        test_data.append(
            ItemHashResult(
                name=f"test_{i}",
                type=random.choice(["file", "folder"]),
                sha1=f"test_sha1_{i}",
                sha256=f"test_sha256_{i}",
                md5=f"test_md5_{i}",
                size=random.randint(100, 1000000),
                other_hash_info={"test": f"test_{i}"},
            )
        )
    return test_data

# 消费者-入库进程 ✅修复5：删除无效的KeyboardInterrupt捕获
def saver(queue):
    logger = get_logger()
    while True:
        try:
            item = queue.get()
            if item is None:  # 哨兵值，收到则优雅退出
                logger.info("saver 收到 None 信号, 退出循环")
                break
            if not isinstance(item, ItemHashResult):
                logger.error(f"item must be ItemHashResult, but got {type(item)}")
                raise ValueError(f"item must be ItemHashResult, but got {type(item)}")
            item_name = item.name
            item_sha1 = item.sha1
            item_sha256 = item.sha256
            item_md5 = item.md5
            save_result = save_item_hash_result(item)
            if save_result:
                logger.info(
                    f"{item_name} 保存哈希结果成功,sha1:{item_sha1},sha256:{item_sha256},md5:{item_md5}"
                )
            time.sleep(0.1)
        except Exception as e:  # 只捕获业务异常即可
            logger.error(f"saver 发生异常: {e}")

# 生产者-生产数据进程（你的业务逻辑，未修改）
def producer(queue):
    logger = get_logger()
    test_data = create_test_data(20)
    logger.info(f"producer 生产 {len(test_data)} 条测试数据")
    logger.info('开始生产数据')
    for item in test_data:
        queue.put(item)
        time.sleep(1)
    logger.info('生产数据完成')
    queue.put(None)  # 发送哨兵值，通知消费者退出

def test_multi_processing():
    logger = get_logger()
    # ✅ 修复2：manager创建+启动 移到函数内部，全局无任何进程相关代码
    manager = Manager()
    queue = manager.Queue()  # ✅ 修复1：直接使用manager自带的Queue，无需注册
    
    print('开始测试多进程,重置数据库')
    reset_db()
    
    # ✅ 修复3：添加 daemon=True 守护进程属性
    producer_process = Process(target=producer, args=(queue,), daemon=True)
    saver_process = Process(target=saver, args=(queue,), daemon=True)
    
    producer_process.start()
    saver_process.start()

    try:
        # ✅ 修复7：带超时的循环join，并行等待，不阻塞信号捕获，响应Ctrl+C
        while producer_process.is_alive() or saver_process.is_alive():
            producer_process.join(timeout=0.2)
            saver_process.join(timeout=0.2)
    except KeyboardInterrupt:
        # ✅ 修复4：主进程捕获Ctrl+C，优雅终止子进程，完美满足你的核心需求
        logger.info("接受到 Ctrl+C 信号, 开始优雅关闭进程...")
        if producer_process.is_alive():
            producer_process.terminate()
            producer_process.join()
        if saver_process.is_alive():
            saver_process.terminate()
            saver_process.join()
        logger.info("所有子进程已成功终止")
    finally:
        # 无论是否中断，都关闭管理器释放资源
        manager.shutdown()
        logger.info("manager已关闭，所有资源释放完成")

    logger.info("producer_process 已完成")
    logger.info("saver_process 已完成")

# ✅ Windows多进程铁律：所有进程相关代码都在这个代码块内调用
if __name__ == "__main__":
    test_multi_processing()
