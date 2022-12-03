# -*- coding: utf-8 -*-
import sys
import os
import configparser
from modules import messages, constants
from datetime import datetime, timedelta
from cryptography.fernet import Fernet, InvalidToken


class Object:
    def __init__(self):
        self._created = datetime.now().isoformat()


def decode(log, encoded_text):
    log.debug(f"{messages.PASSW_DECODING}")
    if encoded_text is not None and len(encoded_text) > 0:
        private_key = "sMZo38VwRdigN78FBnHj8mETNlofL4Qhj_x5cvyxJsc="
        cipher_suite = Fernet(bytes(private_key, "UTF-8"))
        try:
            bet = bytes(encoded_text, "UTF-8")
            decoded_text = cipher_suite.decrypt(bet).decode("UTF-8")
            return str(decoded_text)
        except InvalidToken:
            error_msg = f"{messages.PASSW_NOT_ENC_ERROR}: {encoded_text}"
            if len(encoded_text) == 100:
                error_msg = f"{messages.PASSW_OTHER_KEY_ERROR}: {encoded_text}"
        except Exception as e:
            error_msg = f"{messages.PASSW_DECODE_ERROR}: {get_exception(e)}"
        if log is not None:
            log.error(error_msg)
        else:
            sys.stderr.write(f"[ERROR]: {error_msg}\n")
    return None


def is_file_older_than_x_days(file_path, xdays):
    file_time = datetime.fromtimestamp(os.path.getctime(file_path))
    if int(xdays) == 1:
        cutoff_time = datetime.today()
    else:
        cutoff_time = datetime.today() - timedelta(days=int(xdays))
    file_time = file_time.replace(hour=0,
                                  minute=0,
                                  second=0,
                                  microsecond=0)
    cutoff_time = cutoff_time.replace(hour=0,
                                      minute=0,
                                      second=0,
                                      microsecond=0)
    if file_time < cutoff_time:
        return True
    return False


def get_all_ini_file_settings(file_name):
    final_data = {}
    parser = configparser.ConfigParser()
    parser.optionxform = str
    try:
        parser.read(file_name)
        for section in parser.sections():
            final_data[section] = {}
            obj = Object()
            for option in parser.options(section):
                try:
                    value = parser.get(section, option).replace("\"", "")
                except Exception:
                    value = None
                if value is not None and len(value) == 0:
                    value = None
                setattr(obj, option, value)
            final_data[section] = obj
        return final_data
    except Exception as e:
        sys.stderr.write(get_exception(e))
        sys.exit(1)


def get_ini_section_settings(file_name, section):
    final_data = {}
    parser = configparser.ConfigParser()
    parser.optionxform = str
    try:
        parser.read(file_name)
        obj = Object()
        for option in parser.options(section):
            try:
                value = parser.get(section, option).replace("\"", "")
            except Exception:
                value = None
            if value is not None and len(value) == 0:
                value = None
            final_data[option] = value
            setattr(obj, option, value)
        final_data = obj
        return final_data
    except Exception as e:
        sys.stderr.write(get_exception(e))
        sys.exit(1)


def get_ini_setting(file_name, section, config_name):
    parser = configparser.ConfigParser(delimiters="=", allow_no_value=True)
    parser.optionxform = str
    parser._interpolation = configparser.ExtendedInterpolation()
    parser.read(file_name)
    try:
        value = parser.get(section, config_name).replace("\"", "")
    except Exception:
        value = None
    if value is not None and len(value) == 0:
        value = None
    return value


def get_exception(e):
    module = e.__class__.__module__
    if module is None or module == str.__class__.__module__:
        module_and_exception = f"{e.__class__.__name__}:{e}"
    else:
        module_and_exception = f"{module}.{e.__class__.__name__}:{e}"
    return module_and_exception.replace("\r\n", " ").replace("\n", " ")


def search_inside_list(lst, el):
    found = False
    idx = -1
    if el is not None and len(lst) > 0:
        for idx, v in enumerate(lst):
            for i, p in enumerate(v):
                if p[0] == el:
                    found = True
                    break
    return [found, idx]


def convert_size(size_bytes):
    import math
    if size_bytes == 0:
        return "0 Bytes"
    size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def list_files(directory, file_extension):
    files_list = []
    if os.path.isdir(directory):
        files_list = [os.path.join(directory, f) for f in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory, f))
                      and f.lower().endswith(file_extension.lower())]
        files_list.sort(key=os.path.getmtime)
    return files_list


def list_files_bymask(directory, mask):
    import re
    files_list = []
    rx = re.compile(mask)
    if os.path.isdir(directory):
        files_list = [os.path.join(directory, f) for f in os.listdir(directory)
                      if os.path.isfile(os.path.join(directory,
                                                     f)) and rx.match(f)]
        files_list.sort(key=lambda f: os.path.getmtime(os.path.join(directory,
                                                                    f)))
    return files_list


def remove_dup_list(lst):
    from collections import deque
    q = deque([])
    for v in lst:
        if isinstance(v, str) and v not in q:
            q.append(v)
    return q


def format_path_dates(var, date):
    if var is not None and date is not None:
        var = var.replace("F", date.strftime("%f")[:-3])\
            .replace("HHMMSS", date.strftime("%H%M%S"))\
            .replace("DD", date.strftime("%d"))\
            .replace("MM", date.strftime("%m"))\
            .replace("YYYY", date.strftime("%Y"))
        if date.month <= 6:
            var = var.replace("SE", date.strftime("01"))
        else:
            var = var.replace("SE", date.strftime("02"))
    return var


def get_hostname():
    try:
        local_hostname = os.uname()[1]
    except (ValueError, AttributeError):
        local_hostname = os.environ["COMPUTERNAME"]
    return local_hostname


# def next_running_time(loop_time_seconds):
#     time_formatter = "%H:%M:%S.%f"
#     tdelta = timedelta(seconds=loop_time_seconds)
#     now = datetime.now()
#     next_exec = (now + tdelta).strftime(time_formatter)
#     return next_exec


def create_dirs(self, dirs):
    try:
        os.makedirs(dirs, exist_ok=True) if not os.path.isdir(dirs) else None
    except OSError as e:
        self.log.error(f"{messages.DIR_CREATE_ERROR}:{get_exception(e)}: "
                       f"{os.path.normpath(dirs)}")
        return False
    return True


def remove_dir(self, dir_path):
    import shutil
    try:
        shutil.rmtree(dir_path,
                      ignore_errors=True) if os.path.isdir(dir_path) else None
    except Exception as e:
        self.log.error(f"{messages.DIR_REMOVE_ERROR}:{get_exception(e)}: "
                       f"{os.path.normpath(dir_path)}")
        return False
    return True


def remove_file(self, file_path):
    try:
        os.remove(file_path) if os.path.isfile(file_path) else None
    except Exception as e:
        self.log.error(f"{messages.FILE_REMOVE_ERROR}:{get_exception(e)}: "
                       f"{os.path.normpath(file_path)}")
        return False
    return True


def rename_file(self, src_file_path, dst_file_path):
    try:
        os.rename(src_file_path,
                  dst_file_path) if os.path.isfile(src_file_path) else None
    except Exception as e:
        self.log.error(f"{messages.FILE_RENAME_ERROR}:{get_exception(e)}: "
                       f"{os.path.normpath(src_file_path)} -> "
                       f"{os.path.normpath(dst_file_path)}")
        return False
    return True


def copy_file(self, src_file_path, dst_file_path):
    try:
        import shutil
        shutil.copy2(src_file_path, dst_file_path) if os.path.isfile(
            src_file_path) else None
    except Exception as e:
        self.log.error(f"{messages.FILE_COPY_ERROR}:{get_exception(e)}: "
                       f"{os.path.normpath(src_file_path)} -> "
                       f"{os.path.normpath(dst_file_path)}")
        return False
    return True


def move_file(self, src_file_path, dst_path):
    dst_file_path = os.path.join(dst_path, os.path.basename(src_file_path))

    try:
        import shutil
        shutil.move(src_file_path, dst_file_path) if os.path.isfile(
            src_file_path) else None
    except Exception as e:
        self.log.error(f"{messages.FILE_MOVE_ERROR}:{get_exception(e)}: "
                       f"{os.path.normpath(src_file_path)} -> "
                       f"{os.path.normpath(dst_file_path)}")
        return False
    return True
