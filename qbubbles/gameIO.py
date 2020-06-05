import builtins
import io
import sys as _sys
import os as _os
import typing as _t
from time import strftime


# noinspection PyShadowingBuiltins
def print(*text, sep=" ", end="", file=_sys.stdout):
    if file == _sys.stdout:
        Logging.info("STDOUT", sep.join([str(text) for text in text])+end)
    elif file == _sys.stderr:
        Logging.info("STDERR", sep.join([str(text) for text in text])+end)
    else:
        Logging.info("PRINT", sep.join([str(text) for text in text])+end)


# TODO: Remove when this leads to serious problems.
builtins.print = print


def printerr(*text, sep=" "):
    Logging.error("STDERR", sep.join([*text]))


def printwrn(*text, sep=" "):
    Logging.warning("STDWRN", sep.join([*text]))


def printdebug(*text, sep=" "):
    Logging.debug("STDDBG", sep.join([*text]))


def printfatal(*text, sep=" "):
    Logging.fatal("STDFTL", sep.join([*text]))


class Logging(object):
    """
    Logging class for logs
    """

    txtlog = ""
    _tme: strftime
    save_file: str
    _pos: int
    _log_var: str

    # noinspection PyCallByClass
    @classmethod
    def __new__(cls, clas, save_path):
        cls._tme = strftime
        # print(save_path)
        if not _os.path.exists(save_path):
            _os.makedirs(save_path)

        cls.save_file = _os.path.join(save_path, cls._tme("log_%d-%m-%Y_%H.%M.%S.log"))
        cls._pos = 1
        cls._log_var = ""

    @classmethod
    def log(cls, level, cmd, msg: str, *, file: _t.TextIO):
        """
        Logs a message

        :param file: The file object to write the message to.
        :param level: The log level.
        :param cmd: The caller's name.
        :param msg: The message to log
        :return:
        """

        if len(msg.splitlines(keepends=False)) > 1:
            cls.loglines(level, cmd, *msg.splitlines(keepends=False), file=file)

        level = str(level)
        cmd = str(cmd)
        msg = str(msg)
        out = f"[{cls._tme('%d-%m-%Y %H:%M:%S')}] [{level.upper()}] [{cmd}]: {msg}\n"
        file.write(out)
        cls.txtlog += out
        cls.save()

    @classmethod
    def loglines(cls, level, cmd, *msgs, file):
        """
        Log multiple messages to the log.

        :param level: Log level.
        :param cmd: The caller's name.
        :param msgs: The messages to log
        :param file: The file object to write the messages to.
        :return:
        """

        for msg in msgs:
            cls.log(level, cmd, msg, file=file)

    @classmethod
    def logtext(cls, text):
        """
        Logs a text message.

        :param text: The text to log
        :return:
        """

        import inspect
        cls.log("INFO", inspect.currentframe().f_back.f_code.co_name, text, file=_sys.stdout)

    @classmethod
    def debug(cls, cmd, message):
        cls.log("DEBUG", cmd, message, file=_sys.stderr)

    @classmethod
    def info(cls, cmd, message):
        cls.log("INFO", cmd, message, file=_sys.stdout)

    @classmethod
    def warning(cls, cmd, message):
        cls.log("WARNING", cmd, message, file=_sys.stderr)

    @classmethod
    def error(cls, cmd, message):
        cls.log("ERROR", cmd, message, file=_sys.stderr)

    @classmethod
    def fatal(cls, cmd, message):
        cls.log("FATAL", cmd, message, file=_sys.stderr)
        cls.save()
        _sys.exit(1)
        # raise Exception(f"{cmd}: {message}")

    @classmethod
    def save(cls):
        """
        Saves the log

        :return:
        """

        # print(cls.save_file)

        fa = io.open(cls.save_file, "w", encoding="utf-8")
        fa.write(cls.txtlog)
        fa.close()
