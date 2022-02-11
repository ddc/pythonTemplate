# -*- coding: utf-8 -*-
import os
import sys
import gzip
import logging.handlers
from datetime import datetime
from modules import utils, messages


class Log:
    def __init__(self, **kwargs):
        self.filename = kwargs.get("filename", None)
        self.dir = kwargs.get("dir", "{}/logs".format(os.path.dirname(sys.argv[0])))
        self.days_to_keep = int(kwargs.get("days_to_keep", 30))
        self.level = logging.DEBUG if kwargs.get("debug") else logging.INFO
        self.rotation_days = int(kwargs.get("rotation_days", 1))


    def setup_logging(self):
        try:
            os.makedirs(self.dir) if not os.path.isdir(self.dir) else None
        except Exception as e:
            sys.stderr.write("{}:{}: {}\n".format(messages.LOGS_DIR_NOT_FOUND,
                                                  utils.get_exception(e),
                                                  self.dir))
            sys.exit(1)

        if not self.filename:
            script_name, script_ext = os.path.splitext(os.path.basename(sys.argv[0]))
            self.filename = "{}.log".format(script_name)
        log_file_path = "%s/%s" % (self.dir, self.filename)

        GZipRotator(self.dir, log_file_path, self.days_to_keep, self.rotation_days)

        try:
            open(log_file_path, "a+").close()
        except IOError as e:
            sys.stderr.write("{}:{}: {}\n".format(messages.LOG_FILE_NOT_WRITABLE,
                                                  utils.get_exception(e),
                                                  log_file_path))
            sys.exit(1)

        if self.level == logging.DEBUG:
            formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:[PID:{}]:" \
                      "[%(filename)s:%(funcName)s:%(lineno)d]:%(message)s".format(os.getpid())
        else:
            formatt = "[%(asctime)s.%(msecs)03d]:[%(levelname)s]:[PID:{}]:%(message)s".format(os.getpid())

        datefmt = "%Y-%m-%dT%H:%M:%S"
        log_formatter = logging.Formatter(formatt, datefmt=datefmt)
        logging.basicConfig(level=self.level, filename=log_file_path, format=formatt, datefmt=datefmt)

        console = logging.StreamHandler()
        console.level = self.level
        console.setFormatter(log_formatter)

        logging.getLogger().addHandler(console)
        logger = logging.getLogger()
        logger.level = self.level
        return logger


class GZipRotator:
    def __init__(self, dir_logs, log_file_path, days_to_keep, rotation_days):
        RemoveOldLogs(dir_logs, days_to_keep)
        if os.path.isfile(log_file_path) \
                and os.stat(log_file_path).st_size > 0 \
                and utils.is_file_older_than_x_days(log_file_path, rotation_days):
            file_creation_time = (datetime.utcfromtimestamp(os.path.getctime(log_file_path))).strftime("%Y%m%d")
            fname_bkp, ext_log = os.path.splitext(os.path.basename(log_file_path))
            log_backup_name = "{}_{}{}".format(fname_bkp, file_creation_time, ext_log)
            log_backup_path = "%s/%s" % (dir_logs, log_backup_name)

            try:
                with open(log_file_path, "rb") as fin:
                    with gzip.open("{}.gz".format(log_backup_path), "wb") as fout:
                        fout.writelines(fin)
            except Exception as e:
                sys.stderr.write("{}:{}: {}\n".format(messages.LOG_COMPRESS_ERROR,
                                                      utils.get_exception(e),
                                                      log_backup_path))
                try:
                    os.rename(log_file_path, log_backup_path) if os.path.isfile(log_file_path) else None
                except IOError as e:
                    sys.stderr.write("{}: {}\n".format(messages.LOG_RENAME_ERROR,
                                                       utils.get_exception(e)))
                return

            try:
                os.remove(log_file_path) if os.path.isfile(log_file_path) else None
            except Exception as e:
                sys.stderr.write("{}:{}: {}\n".format(messages.LOG_REMOVE_ERROR,
                                                      utils.get_exception(e),
                                                      log_file_path))


class RemoveOldLogs:
    def __init__(self, dir_logs, days_to_keep):
        if os.path.isdir(dir_logs):
            files_list = [f for f in os.listdir(dir_logs)
                          if os.path.isfile("%s/%s" % (dir_logs, f)) and f.lower().endswith(".gz")]
            for f in files_list:
                full_path = "%s/%s" % (dir_logs, f)
                if utils.is_file_older_than_x_days(full_path, days_to_keep):
                    try:
                        os.remove(full_path) if os.path.isfile(full_path) else None
                    except OSError as e:
                        sys.stderr.write("{}:{}: {}\n".format(messages.LOG_REMOVE_ERROR,
                                                              utils.get_exception(e),
                                                              full_path))
