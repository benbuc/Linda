# Author: Benito Buchheim

# This file holds utility functions for Linda
import logging


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
