# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function


class BaseReporter:

    def report_package(self, package):
        raise NotImplementedError

    def finalize(self):
        pass

# Explicit imports
from .stdout import StdoutReporter
from .html import HtmlReporter
