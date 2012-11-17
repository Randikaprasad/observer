# -*- coding: utf-8 -*-

import logging


class DefaultLogger(object):
    """Sets up default logger for a class, accessible by self.log"""
    DEFAULT_LOGGER_FORMAT = "[%(asctime)s] %(name)s.%(funcName)s %(levelname)s: %(message)s"

    def set_logger(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(DefaultLogger.DEFAULT_LOGGER_FORMAT)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
