#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from src.log_utils.timed_rotating_logs import TimedRotatingLog
from timeit import default_timer as timer
from src import constants, messages
from dotenv import load_dotenv


class Main:
    def __init__(self, **kwargs):
        self.log = None
        self.environ = kwargs

    def init(self):
        start_timer = timer()

        log_kwargs = {
            "level": self.environ["LOG_LEVEL"],
            "days_to_keep": self.environ["DAYS_TO_KEEP_LOGS"],
            "directory": constants.DIR_LOGS,
        }
        self.log = TimedRotatingLog(**log_kwargs).init()
        self.log.info(f"[PID:{os.getpid()}]:{messages.STARTING}")

        #main.start(self)

        total_seconds = round(timer() - start_timer, 3)
        self.log.info(f"[{messages.FINISHED}]:{messages.TOTAL_SECONDS}: {total_seconds}")


if __name__ == "__main__":
    if not constants.PYTHON_OK:
        sys.stderr.write(f"[ERROR]:{messages.EXITING}:"
                         f"Python {constants.MIN_PYTHON_VERSION} "
                         f"{messages.NOT_FOUND}\n")
        sys.exit(1)

    load_dotenv()
    conf = dict(os.environ)
    t = Main(**conf)
    t.init()
