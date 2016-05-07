#!/usr/bin/python -tt

import os
import sys
import logging
import traceback



def init_logger(log_file):
    """ Set up logging support for framework """

    log_format = (
        "%(asctime)s:%(threadName)-10s:%(filename)s."
        "%(lineno)d:%(levelname)s: %(message)s")

    logging.basicConfig(level=logging.DEBUG, format=log_format,
                        filename=log_file, filemode='w')

    root_logger = logging.getLogger('')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(message)s'))
    root_logger.addHandler(console)


def make_dirs(dir_path):
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
        except (IOError, OSError):
            print("Unable to create dir %s" % dir_path)
            traceback.print_exc()
            sys.exit(1)


def get_logger(name):
    return logging.getLogger(name)


def except_handler(a_type, value, a_traceback):
    logging.error("Uncaught Exception", exc_info=(a_type, value, a_traceback))

make_dirs(CONF.log_dir)
make_dirs(CONF.result_dir)
make_dirs(CONF.crashdumps_dir)

init_logger()

#To print uncaught exception trace into log file besides onto Console
sys.excepthook = except_handler
