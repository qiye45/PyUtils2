# logger.py
import os
import logging
from colorama import Fore, Style, init

# 初始化 colorama
init(autoreset=True)

# 定义颜色格式的 Formatter
class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA
    }

    def format(self, record):
        log_color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"

# 初始化日志配置
def init_logger(log_file_path="log/log.txt", log_level=logging.DEBUG):
    # 创建日志文件夹
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # 配置日志记录（文件）
    logging.basicConfig(
        format='[%(asctime)s %(filename)s line:%(lineno)d] %(levelname)s: %(message)s',  # 日志格式
        level=log_level,  # 日志级别
        filename=log_file_path,  # 日志文件路径
        filemode="w",  # 覆盖写入
        encoding="utf-8"  # 文件编码
    )

    # 创建控制台处理器
    console = logging.StreamHandler()
    console.setLevel(log_level)  # 设置控制台日志级别
    console.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))  # 使用带颜色的格式

    # 获取根日志器并添加控制台处理器
    logging.getLogger().addHandler(console)

    # 返回日志器（可选）
    return logging.getLogger()

# main.py
import logging
from logger import init_logger

# 初始化日志（可以指定日志文件路径和日志级别）
logger = init_logger(log_file_path="log/log.txt", log_level=logging.DEBUG)

# 打印不同级别的日志消息
logger.debug('This message should appear in the log file and console (blue)')
logger.info('So should this (green)')
logger.warning('And this, too (yellow)')
logger.error('This is an error message (red)')
logger.critical('This is critical (magenta)')
