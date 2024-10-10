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


# 日志管理类
class LoggerManager:
    def __init__(self, log_file_path="log/log.txt", log_level=logging.DEBUG, max_files=7):
        self.log_file_path = log_file_path
        self.log_dir = os.path.dirname(log_file_path)
        self.log_level = log_level
        self.max_files = max_files
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        # 在初始化日志记录器之前管理现有日志文件
        self._manage_log_files()
        # 初始化日志记录器
        self._init_logger()

    # 检查日志文件的数量并删除最旧的文件
    def _manage_log_files(self):
        # 获取日志目录中的所有日志文件
        log_files = [os.path.join(self.log_dir, f) for f in os.listdir(self.log_dir) if
                     os.path.isfile(os.path.join(self.log_dir, f))]

        # 如果日志文件数量超过最大数量，则删除最旧的文件
        if len(log_files) > self.max_files:
            # 按照文件的修改时间排序（从最旧到最新）
            log_files.sort(key=lambda x: os.path.getmtime(x))
            # 需要删除的文件数量
            files_to_delete = len(log_files) - self.max_files
            # 删除最旧的文件
            for i in range(files_to_delete):
                os.remove(log_files[i])
                print(f"Deleted old log file: {log_files[i]}")

    # 初始化日志记录器
    def _init_logger(self):
        # 配置日志记录（文件）
        logging.basicConfig(
            format='[%(asctime)s %(filename)s line:%(lineno)d] %(levelname)s: %(message)s',  # 日志格式
            level=self.log_level,  # 日志级别
            filename=self.log_file_path,  # 日志文件路径
            filemode="w",  # 覆盖写入
            encoding="utf-8"  # 文件编码
        )
        # 创建控制台处理器
        console = logging.StreamHandler()
        console.setLevel(self.log_level)  # 设置控制台日志级别
        console.setFormatter(ColoredFormatter('%(levelname)s: %(message)s'))  # 使用带颜色的格式
        # 获取根日志器并添加控制台处理器
        logging.getLogger().addHandler(console)

    # 返回日志器实例（可选）
    def get_logger(self):
        return logging.getLogger()


# 使用示例
if __name__ == "__main__":
    # 初始化 LoggerManager
    logger_manager = LoggerManager(log_file_path="log/my_log.txt", log_level=logging.DEBUG, max_files=5)

    # 获取日志器
    logger = logger_manager.get_logger()

    # 测试日志输出
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
