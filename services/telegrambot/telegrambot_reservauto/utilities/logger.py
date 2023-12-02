import logging

emoji_dict = {
    'DEBUG': '🐛',
    'INFO': '',
    'WARNING': '❗',
    'ERROR': '❌',
    'CRITICAL': '💥',
}

class EmojiFormatter(logging.Formatter):
    def format(self, record):
        level_name = record.levelname
        emoji = emoji_dict.get(level_name, '')
        record.levelname = f'{level_name} {emoji}'
        return super().format(record)

class CustomLogger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        log_to_console = logging.StreamHandler()
        log_to_console.setLevel(logging.DEBUG)
        log_format = EmojiFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_to_console.setFormatter(log_format)
        self.addHandler(log_to_console)
    
    def set_level(self, level: int):
        super().setLevel(level)

