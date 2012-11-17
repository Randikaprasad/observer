# -*- coding: utf-8 -*-

import argparse


def ConvertValueAction(conversion_map):
    """Wrapper for converter allowing to pass additional parameter"""
    class ConvertValueActionInternal(argparse.Action):
        """Sets value depending on parameter and conversion map"""
        def __call__(self, parser, namespace, values, option_string=None):
            self.conversion_map = conversion_map
            output = None
            if isinstance(values, list):
                output = list()
                for value in values:
                    output.append(self.conversion_map.get(value, -1))
            else:
                output = self.conversion_map.get(values, -1)
            setattr(namespace, self.dest, output)
    return ConvertValueActionInternal
