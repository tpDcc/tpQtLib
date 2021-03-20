#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpDcc.libs.qt
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import inspect
import logging

from Qt.QtWidgets import QApplication

# =================================================================================

PACKAGE = 'tpDcc.libs.qt'
main = __import__('__main__')

# =================================================================================


def init(dev=False):
    """
    Initializes module
    :param dev: bool, Whether tpDcc-libs-qt is initialized in dev mode or not
    """

    logger = create_logger(dev=dev)

    # NOTE: We register all classes using tpDcc register (not tpDcc.libs.qt one).
    # # We do it in this way to access those classes easily
    # dcc_register.register_class('InputsMgr', inputs_manager.InputsManagerSingleton)
    # dcc_register.register_class('ToolsetsMgr', toolsets_manager.ToolsetsManagerSingleton)

    def init_dcc():
        """
        Checks DCC we are working on an initializes proper variables
        """

        dcc_loaded = False
        try:
            if 'cmds' in main.__dict__:
                from tpDcc.dccs.maya import loader as dcc_loader
                dcc_loaded = True
            elif 'MaxPlus' in main.__dict__:
                from tpDcc.dccs.max import loader as dcc_loader
                dcc_loaded = True
            elif 'hou' in main.__dict__:
                from tpDcc.dccs.houdini import loader as dcc_loader
                dcc_loaded = True
            elif 'nuke' in main.__dict__:
                from tpDcc.dccs.nuke import loader as dcc_loader
                dcc_loaded = True
            else:
                try:
                    import unreal
                    from tpDcc.dccs.unreal import loader as dcc_loader
                    dcc_loaded = True
                except Exception:
                    pass
        except ImportError:
            logger.warning('Impossible to setup DCC. DCC not found. Abstract one will be used.')
        except Exception as exc:
            logger.warning('Error while setting DCC: {}. Abstract one will be used.'.format(exc))

        if dcc_loaded:
            if hasattr(dcc_loader, 'init_ui') and callable(dcc_loader.init_ui):
                dcc_loader.init_ui()

    app = QApplication.instance() or QApplication(sys.argv)

    update_paths()

    init_dcc()


def get_module_path():
    """
    Returns path where tpQtLib module is stored
    :return: str
    """

    try:
        mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
    except Exception:
        try:
            mod_dir = os.path.dirname(__file__)
        except Exception:
            try:
                import tpDcc.libs.qt
                mod_dir = tpDcc.libs.qt.__path__[0]
            except Exception:
                return None

    return mod_dir


def update_paths():
    """
    Adds path to system paths at startup
    """

    paths_to_update = [externals_path()]

    for p in paths_to_update:
        if os.path.exists(p) and p not in sys.path:
            sys.path.append(p)


def externals_path():
    """
    Returns the paths where tpPyUtils externals packages are stored
    :return: str
    """

    return os.path.join(get_module_path(), 'externals')


def create_logger(dev=False):
    """
    Returns logger of current module
    """

    logger_directory = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpDcc', 'logs'))
    if not os.path.isdir(logger_directory):
        os.makedirs(logger_directory)

    logging_config = os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))

    logging.config.fileConfig(logging_config, disable_existing_loggers=False)
    logger = logging.getLogger(PACKAGE.replace('.', '-'))
    dev = os.getenv('TPDCC_DEV', dev)
    if dev:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)

    return logger


create_logger()
