from . import BaseReporter
from ..score import PackageDescriptor


class StdoutReporter(BaseReporter):

    max_level = -1

    def report_package(self, package):
        if package.alert > self.max_level:
            self.max_level = package.alert
        print(package)

    def finalize(self):
        msg = "Summary status: {}".format(
                PackageDescriptor.ALERT_STR[self.max_level]
        )
        print("-" * len(msg))
        print(msg)
