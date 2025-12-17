"""
Esse módulo contém funções utilitárias
referentes a logging.
"""
from pathlib import Path
from logging import getLogger, FileHandler, Formatter, StreamHandler, DEBUG
from src.core.type_hints import LoggingLevel
from src.core.config import LOGGING_PATH_OUTPUT
from src.utils.files_utils import clear_file

formatter = Formatter(
    "[%(asctime)s] [%(levelname)s] (%(name)s): %(message)s"
)
DEFAULT_STREAM_HANDLER = StreamHandler()
DEFAULT_STREAM_HANDLER.setFormatter(formatter)

# file_handlers = {}
logger_files = {}

def _output_folder(filename: str) -> str:
    path = Path(LOGGING_PATH_OUTPUT) / filename
    return str(path)

def _normalize_output_name(output_name: str) -> str:
    path = output_name.replace(".", "_") + ".log"
    return path

def log(
    message: str,
    level: LoggingLevel,
    logger_name: str,
    output: bool = False,
    clear_old_log: bool = False
) -> None:
    """
    Gera e salva um log.

    Se `output` for False, enviará ao terminal,
    caso contrário, num arquivo em *./log/**logger_name**.log*
    """
    logger = getLogger(logger_name)
    logger.setLevel(DEBUG)
    try:
        method = getattr(logger, level)
    except AttributeError:
        raise AttributeError(f"O 'level' de log é inválido: {level}") from None
    if output is False:
        handler = StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    elif file_handlers.get(output) is None:
        output_file_name = _normalize_output_name(logger_name)
        output_path = _output_folder(output_file_name)
        handler = FileHandler(output_path, encoding="utf-8")
        handler.setFormatter(formatter)
        file_handlers[logger] = handler
        logger.addHandler(handler)
        if clear_old_log and logger_has_cleared_file.get(logger) is not True:
            clear_file(output_path)
            logger_has_cleared_file[logger] = True
    method(message)
