import logging
from datetime import datetime

logging.basicConfig(
    filename="forensics.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def forensic_wrapper(func):
    """
    Decorator that logs function entry, arguments, return value,
    and any exceptions. This is the core of your 'forensics' work.
    """
    def inner(*args, **kwargs):
        func_name = func.__name__
        logging.info(f"[CALL] {func_name} args={args} kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"[RETURN] {func_name} result={result!r}")
            return result
        except Exception as e:
            logging.exception(f"[EXCEPTION] {func_name} raised {type(e).__name__}: {e}")
            raise
    return inner
