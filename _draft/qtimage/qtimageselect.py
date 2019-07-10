from PyQt5 import QtCore, QtGui, QtWidgets

__pts__  = []

class Crosshair(QtWidgets.QGraphicsItem):
    def __init__(self):
        QtGui.QGraphicsItem.__init__(self)
        self.setFlag(self.ItemIgnoresTransformations)

    def paint(self, p, *args):
        p.setPen(QtGui.QPen(QtCore.Qt.darkYellow, 1))
        p.drawLine(-10, 0, 10, 0)
        p.drawLine(0, -10, 0, 10)

    def boundingRect(self):
        return QtCore.QRectF(-10, -10, 20, 20)


class GraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(
            QtCore.QRectF(-500, -500, 1000, 1000), parent
        )
        self._start = QtWidgets.QGraphicsEllipseItem()
        self._current_pt = None

    def mousePressEvent(self, event):
        if self.itemAt(event.scenePos(), QtGui.QTransform()) is None:
            self._current_pt = QtWidgets.QGraphicsEllipseItem()
            self._current_pt.setBrush(QtCore.Qt.green)
            self._current_pt.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            self.addItem(self._current_pt)
            self._start = event.scenePos()
            x, y = self._start.x(), self._start.y()
            r = QtCore.QRectF(
                QtCore.QPointF(x - 2, y - 2), QtCore.QPointF(x + 2, y + 2)
            )
            self._current_pt.setRect(r)
            __pts__.append(self._current_pt)
        super(GraphicsScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._current_pt is not None:
            pos = event.scenePos()
            x, y = pos.x(), pos.y()
            r = QtCore.QRectF(
                QtCore.QPointF(x - 2, y - 2), QtCore.QPointF(x + 2, y + 2)
            )
            self._current_pt.setRect(r)
        super(GraphicsScene, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._current_pt_current_pt = None
        super(GraphicsScene, self).mouseReleaseEvent(event)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.scene = GraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.view)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.resize(640, 480)
    w.show()
    app.exec_()
    sys.exit(app.exec_())

print(__pts__)
