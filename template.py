#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from modules.log import Log
from argparse import ArgumentParser
from modules import main, utils, constants, messages
from timeit import default_timer as timer


class Template:
    def __init__(self, **kwargs):
        self.main = None
        self.mongo = None
        self.log = None
        self.debug = kwargs.get("debug")
        self.__dict__.update(kwargs)


    def run(self):
        start_timer = timer()

        log_kwargs = {"days_to_keep": self.main.DAYS_TO_KEEP_LOGS,
                      "debug": self.debug}
        self.log = Log(**log_kwargs).setup_logging()
        self.log.info(f"[PID:{os.getpid()}]:{messages.STARTING} v{constants.VERSION}")

        main.start(self)

        total_segundos = round(timer() - start_timer, 3)
        self.log.info(f"[{messages.FINISHED}]:{messages.TOTAL_SECONDS}: {total_segundos}")


if __name__ == "__main__":
    if not constants.PYTHON_OK:
        sys.stderr.write(f"[ERROR]:{messages.EXITING}:"
                         f"Python {constants.MIN_PYTHON_VERSION} {messages.NOT_FOUND}\n")
        sys.exit(1)
    if not os.path.isfile(constants.CFG_FILE):
        sys.stderr.write(f"[ERROR]:{messages.EXITING}:"
                         f"{messages.CONFIG_FILE} {messages.NOT_FOUND}: {constants.CFG_FILE}\n")
        sys.exit(1)
    os.environ["COLUMNS"] = "200"
    parser = ArgumentParser(add_help=False)
    parser.add_argument("-d", "--debug",
                        required=False,
                        action="store_true",
                        help=f"{messages.HELP_DEBUG}")
    args = parser.parse_args()
    settings_vars = utils.get_all_ini_file_settings(constants.CFG_FILE)
    settings_vars.update({"debug": args.debug})
    t = Template(**settings_vars)
    del settings_vars
    t.run()
