import sys
from PySide6 import QtGui
from fbs_runtime.application_context.PySide6 import ApplicationContext, cached_property
from packages.main_window import MainWindow

class AppContext(ApplicationContext):
    def run(self):
        window = MainWindow(ctx=self)
        window.resize(1920/4, 980/2)
        window.show()
        return self.app.exec()

    @cached_property
    def image_checked(self):
        return QtGui.QIcon(self.get_resource("images/checked.png"))

    @cached_property
    def image_unchecked(self):
        return QtGui.QIcon(self.get_resource("images/unchecked.png"))


if __name__ == '__main__':
    appctxt = AppContext() # 1. Instantiate ApplicationContext
    sys.exit(appctxt.run())