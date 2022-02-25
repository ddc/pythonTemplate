# -*- coding: utf-8 -*-
import os
import sys
import gzip
import logging.handlers
from modules import utils, messages, constants


class Log:
    def __init__(self, **kwargs):
        self.filename = kwargs.get("filename", None)
        self.days_to_keep = int(kwargs.get("days_to_keep", constants.DAYS_TO_KEEP_LOGS))
        self.level = logging.DEBUG if kwargs.get("debug") else logging.INFO
        self.dir = kwargs.get("dir", constants.DIR_LOGS)


    def setup_logging(self):
        try:
            os.makedirs(self.dir, exist_ok=True) if not os.path.isdir(self.dir) else None
        except OSError as e:
            sys.stderr.write(f"{messages.LOGS_DIR_NOT_FOUND}:"
                             f"{utils.get_exception(e)}: "
                             f"{os.path.normpath(self.dir)}\n")
            sys.exit(1)

        if self.filename is None:
            script_name, script_ext = os.path.splitext(sys.argv[0])
            self.filename = f"{os.path.basename(script_name)}.log"
        log_file_path = os.path.join(self.dir, self.filename)

        try:
            open(log_file_path, "a+").close()
        except IOError as e:
            sys.stderr.write(f"{messages.LOG_FILE_NOT_WRITABLE}:"
                             f"{utils.get_exception(e)}: "
                             f"{os.path.normpath(log_file_path)}\n")
            sys.exit(1)

        if self.level == logging.DEBUG:
            formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:[PID:{os.getpid()}]:" \
                      f"[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s"
        else:
            formatt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:[PID:{os.getpid()}]:%(message)s"

        formatter = logging.Formatter(formatt, datefmt="%Y-%m-%dT%H:%M:%S")
        logger = logging.getLogger()
        logger.setLevel(self.level)
        file_hdlr = logging.handlers.TimedRotatingFileHandler(filename=log_file_path,
                                                              encoding="UTF-8",
                                                              when="midnight",
                                                              backupCount=self.days_to_keep)

        file_hdlr.setFormatter(formatter)
        file_hdlr.suffix = "%Y%m%d"
        file_hdlr.rotator = GZipRotator(self.dir, self.days_to_keep)
        logger.addHandler(file_hdlr)

        stream_hdlr = logging.StreamHandler()
        stream_hdlr.setFormatter(formatter)
        stream_hdlr.setLevel(self.level)
        logger.addHandler(stream_hdlr)
        return logger


class GZipRotator:
    def __init__(self, dir_logs, days_to_keep):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep


    def __call__(self, source, dest):
        RemoveOldLogs(self.dir, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            try:
                sfname, sext = os.path.splitext(source)
                dfname, dext = os.path.splitext(dest)
                renamed_dst = f"{sfname}_{dext.replace('.', '')}{sext}.gz"
                with open(source, "rb") as fin:
                    with gzip.open(renamed_dst, "wb") as fout:
                        fout.writelines(fin)
            except Exception as e:
                sys.stderr.write(f"{messages.LOG_COMPRESS_ERROR}:"
                                 f"{utils.get_exception(e)}: "
                                 f"{os.path.normpath(source)}\n")
                return

            try:
                os.remove(source)
            except OSError as e:
                sys.stderr.write(f"{messages.LOG_REMOVE_ERROR}:"
                                 f"{utils.get_exception(e)}: "
                                 f"{os.path.normpath(source)}\n")


class RemoveOldLogs:
    def __init__(self, dir_logs, days_to_keep):
        if os.path.isdir(dir_logs):
            files_list = [f for f in os.listdir(dir_logs)
                          if os.path.isfile(os.path.join(dir_logs, f))
                          and f.lower().endswith(".gz")]
            for file in files_list:
                file_path = os.path.join(dir_logs, file)
                if utils.is_file_older_than_x_days(file_path, days_to_keep):
                    try:
                        os.remove(file_path)
                    except OSError as e:
                        sys.stderr.write(f"{messages.LOG_REMOVE_ERROR}:"
                                         f"{utils.get_exception(e)}: "
                                         f"{os.path.normpath(file_path)}\n")
