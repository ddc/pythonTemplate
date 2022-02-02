# -*- encoding: utf-8 -*-
import os
import sys
from pathlib import Path


__version_info__ = ("1", "0", "0")
__version__ = ".".join(__version_info__)
__author__ = "ddc"
__email__ = "ddc@ddc"
__req_python_version__ = (3, 6, 0)


_script_path = Path(os.path.dirname(sys.argv[0])).absolute()
try:
    TMP_DIR = os.path.normpath("{}/tmp".format(_script_path))
    os.makedirs(TMP_DIR) if not os.path.isdir(TMP_DIR) else None
except OSError as e:
    TMP_DIR = "/tmp"


################
# MAIN
################
VERSION = __version__
PYTHON_OK = sys.version_info >= __req_python_version__
MIN_PYTHON_VERSION = ".".join(str(x) for x in __req_python_version__)
DATE_TIME_FORMATTER = "%Y-%m-%d %H:%M:%S.%f"
DATE_FORMATTER = "%Y%m%d"
TIME_FORMATTER = "%H%M%S-%f"
DIR_LOGS = os.path.normpath("{}/logs".format(_script_path))
SQLITE_FILE = os.path.normpath("{}/config/database.db".format(_script_path))
CFG_FILE = os.path.normpath("{}/config/settings.ini".format(_script_path))
################
# SFTP
################
LINUX_SFTP_BIN = "/usr/bin/sftp"
PKEY_FILE = os.path.expanduser("~/.ssh/id_rsa")
SFTP_CONN_WAIT_TIME = 1.0
################
# OPTIONALS
################
#IS_WINDOWS = True if os.name == "nt" else False
#CPU_COUNT = os.cpu_count() if int(os.cpu_count()) < 4 else 4
#PID_FILE = os.path.normpath("{}/pidFile.pid".format(TMP_DIR))
################
# PROGRAM SPECIFIC
################
