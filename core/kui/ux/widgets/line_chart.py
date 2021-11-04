import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QGraphicsScene, QGraphicsView,
                             QGraphicsLineItem, QGraphicsRectItem)
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush


class performance_chart(QGraphicsScene):
    def __init__(self, color: str = 'black'):
        super().__init__()

        self.setSceneRect(0, 0, 168*2, 100)

        self.lines: list = []

        self.border = 2
        self.box_size = 50
        self.segments = 170

    def drawrect(self, row, col):
        # _sz_p = self.sceneRect().size().width()

        _color_flag = 0
        _segment_flag = 0
        _counter = 0

        for segments in range(self.segments):
            _rect = QGraphicsRectItem(_segment_flag, 0, 1, 100)
            _counter += 1
            if _counter == 25:
                if _color_flag == 0:
                    _color_flag = 1
                else:
                    _color_flag = 0
                _counter = 0

            if _color_flag == 0:
                co = QColor(QtCore.Qt.red)
            else:
                co = QColor(QtCore.Qt.blue)

            co.setAlpha(25)
            p = QPen(co, 1, QtCore.Qt.SolidLine,
                     QtCore.Qt.SquareCap,
                     QtCore.Qt.MiterJoin)
            b = QBrush(co, QtCore.Qt.SolidPattern)
            p.setBrush(b)
            _rect.setPen(p)

            self.addItem(_rect)
            _segment_flag = _segment_flag + 2

    def get_pen(self, color: str):
        return QPen(QColor(color), 1,
                    QtCore.Qt.SolidLine,
                    QtCore.Qt.RoundCap,
                    QtCore.Qt.RoundJoin)

    @staticmethod
    def draw_line_segment(x1, y1, x2, y2, line_pen):
        _line = QGraphicsLineItem(x1, y1, x2, y2)
        _line.setPen(line_pen)
        return _line

    def gen_line(self, data: list):
        # data_1 = {'name': 'kva', 'color': 'black', 'data': []}

        def _co():
            q = random.randint(0, 3)

            if q == 0:
                _return = 'black'
            elif q == 1:
                _return = 'red'
            elif q == 2:
                _return = 'green'
            elif q == 3:
                _return = 'blue'
            return _return

        _data = {'name': 'wallet', 'color': _co(), 'data': [], 'scaler': 0.0}
        for i in data:
            if i[1] > _data['scaler']:
                _data['scaler'] = i[1]

            _data['data'].append(i[1])

        if _data['scaler'] == 0.0:
            _data['scaler'] = 1

        _data['scaler'] = _data['scaler'] / self.sceneRect().size().height()
        self.lines.append(_data)

    def redraw(self):
        self.clear()
        self.draw()

    def draw(self):
        self.drawrect(10, 20)
        for line in enumerate(self.lines):
            _dat = line
            for i in range(0, len(_dat['data'])):
                if i > 0:
                    # _sz_p = self.sceneRect().size().width()
                    _sz = 2  # _sz_p/(len(_dat['data'])-1)
                    _sz_h = 100  # self.sceneRect().size().height()

                    _pt_a = {'x': i*_sz,
                             'y': _sz_h-(_dat['data'][i-1]/_dat['scaler'])+1}
                    _pt_b = {'x': i*_sz+_sz,
                             'y': _sz_h-(_dat['data'][i]/_dat['scaler'])+1}

                    _line = self.draw_line_segment(_pt_a['x'], _pt_a['y'],
                                                   _pt_b['x'], _pt_b['y'],
                                                   self.get_pen(_dat['color']))
                    self.addItem(_line)
