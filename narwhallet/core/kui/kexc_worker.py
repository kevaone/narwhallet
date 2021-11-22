import time
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Worker(QObject):
    finished = pyqtSignal()
    work_done = pyqtSignal(str, str, int)

    def __init__(self, name: str, command, command_params_1,
                 command_params_2, optional: int = None):
        super().__init__()

        self.name = name
        self.command = command
        self.command_params_1 = command_params_1
        self.command_params_2 = command_params_2
        self.optional = optional
        self.b = 0

    @pyqtSlot()
    def do_timer_work(self):
        _sec_cap = 0
        while _sec_cap < self.command_params_1:
            time.sleep(1)
            _sec_cap += 1
            if self.b == 1:
                break
        self.work_done.emit(self.name, 'ret', self.optional)
        self.finished.emit()

    @pyqtSlot()
    def do_work(self):
        if self.command_params_1:
            if self.command_params_2:
                ret = self.command(self.command_params_1,
                                   self.command_params_2)
            elif self.command_params_2 == []:
                ret = self.command(self.command_params_1,
                                   self.command_params_2)
            else:
                ret = self.command(self.command_params_1)
        else:
            ret = self.command()

        if isinstance(ret, bytes):
            ret = ret.decode()

        self.optional = self.optional if self.optional is not None else -1
        self.work_done.emit(self.name, ret, self.optional)
        self.finished.emit()
