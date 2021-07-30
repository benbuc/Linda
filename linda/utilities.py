# This file holds utility functions for Linda
import logging
import sys


def getLogger():
    log = logging.getLogger()
    logHandler = logging.StreamHandler()
    logFormatter = logging.Formatter(
        "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
    )
    logHandler.setFormatter(logFormatter)
    if len(log.handlers) == 0:
        log.addHandler(logHandler)

    log.setLevel(logging.DEBUG)

    return log


log = getLogger()


def checkVersion():
    if sys.version_info.major < 3:
        log.error("Python 2 detected. Try running with 'python3 %s'" % sys.argv[0])
        exit()
