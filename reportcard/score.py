import argparse
import pip
import pip.commands
from pip._vendor.packaging import version

SYSTEM_PACKAGES = [
    'pip', 'setuptools', 'wheel', 'distutils', 'distribute'
]


class PackageDescriptor:

    ALERT_OK = 0
    ALERT_WARN = 1
    ALERT_SCREAM = 2

    ALERT_STR = {
        0: "OK",
        1: "WARNING",
        2: "SCREAM"
    }

    version = None
    name = None
    system = False
    latest = None
    description = None
    url = None

    def __init__(self, pkg_version, name):
        self.version = version.parse(pkg_version)
        self.name = name
        self.system = name in SYSTEM_PACKAGES
        self.latest = pkg_version

    @property
    def alert(self):
        scream_expr = \
            self.version._version.release[0] == \
            self.latest._version.release[0] and \
            self.version._version.release[1] == \
            self.latest._version.release[1]

        if self.version < self.latest:
            if scream_expr:
                return self.ALERT_SCREAM
            else:
                return self.ALERT_WARN
        return self.ALERT_OK

    def __str__(self):
        return "{}: {} ({}) {} {} | {}".format(
                self.ALERT_STR[self.alert], self.name, self.version,
                "=" if self.version == self.latest else "<",
                self.latest, self.description
        )


def _load_package_data():
    installed = pip.get_installed_distributions()
    outdated_raw = pip.commands.ListCommand()
    outdated_raw = outdated_raw.find_packages_latest_versions(
        outdated_raw.parser.get_default_values()
    )

    outdated = {x[0].project_name: x[1] for x in outdated_raw}

    for pkginfo in installed:
        descriptor = PackageDescriptor(pkginfo.version, pkginfo.project_name)
        info = list(
                pip.commands.show.search_packages_info([pkginfo.project_name])
        )[0]

        descriptor.url = info['home-page']
        descriptor.description = info['summary']

        if descriptor.name in outdated:
            descriptor.latest = outdated[descriptor.name]
            yield descriptor


def main():
    parser = argparse.ArgumentParser(
            description='Report on environment package status'
    )

    parser.add_argument("--report-out", type=bool, default=True)
    parser.add_argument("--report-tc", type=bool, default=False)
    parser.add_argument("--report-html", action='store_true', default=False)

    args = parser.parse_args()

    print(">> START")

    reporters = []
    if args.report_out:
        from .reporters import StdoutReporter
        reporters.append(StdoutReporter())
    if args.report_html:
        from .reporters import HtmlReporter
        reporters.append(HtmlReporter())

    for package in _load_package_data():
        for reporter in reporters:
            reporter.report_package(package)

    for reporter in reporters:
        reporter.finalize()

    print(">> DONE")

if __name__ == '__main__':
    main()
