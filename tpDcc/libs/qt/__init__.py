#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDcc-libs-qt
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging.config

from Qt.QtWidgets import QApplication


def create_logger(dev=False):
    """
    Creates logger for current tpDcc-libs-qt package
    """

    logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs', 'libs'))
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)

    logging_config = os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))

    logging.config.fileConfig(logging_config, disable_existing_loggers=False)
    logger = logging.getLogger('tpDcc-libs-qt')
    dev = os.getenv('TPDCC_DEV', dev)
    if dev:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    return logger


create_logger()

app = QApplication.instance() or QApplication(sys.argv)