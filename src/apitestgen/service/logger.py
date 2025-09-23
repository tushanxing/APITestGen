import logging.config

# 日志配置（等级字段固定宽度，确保竖线对齐）
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "aligned_format": {
            # 使用 %(levelname)-8s 确保等级字段占8个字符宽度（左对齐）
            "format": "%(asctime)s | 等级: %(levelname)-8s | 函数: %(funcName)s | 行号: %(lineno)d | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console_handler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "aligned_format",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "app_logger": {
            "level": "DEBUG",
            "handlers": ["console_handler"],
            "propagate": False,
        }
    },
}

# 应用配置
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app_logger")

# 使用示例
if __name__ == "__main__":

    def process_data(input_str: str, data_set: set[str]):
        logger.debug(f"接收参数 - 字符串: {input_str}, 集合: {data_set}")
        logger.info(f"开始处理：字符串长度{len(input_str)}，集合元素数{len(data_set)}")

        if len(data_set) < 3:
            logger.warning(
                f"集合元素不足3个（当前{len(data_set)}个），可能影响分析结果"
            )

        try:
            if "invalid" in input_str.lower():
                raise ValueError("输入字符串包含无效关键词")
        except ValueError as e:
            logger.error(f"数据校验失败: {str(e)}")

        if not input_str or not data_set:
            logger.critical(
                f"核心参数缺失（字符串：{bool(input_str)}，集合：{bool(data_set)}），终止处理"
            )
            return False

        return True

    # 测试1：正常场景
    _ = process_data("用户订单数据", {"order_001", "order_002", "order_003"})
    # 测试2：异常场景
    print("-" * 80)
    _ = process_data("Invalid_数据", {"order_004"})
