# -*- encoding: utf-8 -*-
import os
import sys
from pathlib import Path

__req_python_version__ = (3, 12, 0)
_script_path = Path(os.path.dirname(sys.argv[0])).absolute()
_script_name = os.path.basename(sys.argv[0]).split('.')[0]

# MAIN
PYTHON_OK = sys.version_info >= __req_python_version__
MIN_PYTHON_VERSION = ".".join(str(x) for x in __req_python_version__)
DIR_LOGS = os.path.join(_script_path, "logs")
