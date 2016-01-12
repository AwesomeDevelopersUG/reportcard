from jinja2 import Environment, PackageLoader

from . import BaseReporter


env = Environment(loader=PackageLoader('reportcard', 'assets'))


class HtmlReporter(BaseReporter):

    def __init__(self):
        self._system = []
        self._app = []
        self._max_level = -1

    def report_package(self, package):
        if package.alert > self._max_level:
            self._max_level = package.alert

        if package.system:
            self._system.append(package)
        else:
            self._app.append(package)

    def finalize(self):
        with open('scorecard-out.html', 'w') as f:
            f.write(env.get_template('scorecard.html').render(
                app=self._app,
                system=self._system,
                summary_alert=self._max_level
            ))