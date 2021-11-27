import sys
import os
from PyQt5.QtWidgets import QApplication
from narwhallet.control import NarwhalletController
from narwhallet.control.shared import MShared
from narwhallet.core.kui.main import NarwhalletUI


def main():
    NarwhalletMain = QApplication(sys.argv)
    view = NarwhalletUI()
    # TODO: pass override args to controller such as settings file path
    _program_path = os.path.dirname(__file__)
    ctr = NarwhalletController(view, _program_path, NarwhalletMain.clipboard())

    _qss = MShared.get_resource_path('style.css')
    _style = ''
    with open(_qss, 'r', encoding='utf-8') as style_file:
        _style = style_file.read()

    NarwhalletMain.setStyleSheet(_style)

    view.show()
    xit = NarwhalletMain.exec_()
    print('Narwhallet cleaning up...')
    ctr.t_cleanup()
    print('Done cleanup, exiting Narwhallet.')
    sys.exit(xit)


if __name__ == '__main__':
    main()
