import sys
import os

from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QSizePolicy
from PySide2.QtCore import Qt, QFile, QSizeF
from PySide2.QtUiTools import QUiLoader
from PySide2.QtDataVisualization import QtDataVisualization


def dataToBarDataRow(data):
    return list(QtDataVisualization.QBarDataItem(d) for d in data)


def dataToBarDataArray(data):
    return list(dataToBarDataRow(row) for row in data)


class BarsMap3D(QtDataVisualization.Q3DBars):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.bars = QtDataVisualization.Q3DBars()

        self.columnAxis = QtDataVisualization.QCategory3DAxis()
        self.columnAxis.setTitle('Columns')
        self.columnAxis.setTitleVisible(True)
        self.columnAxis.setLabels(['Column1', 'Column2'])
        self.columnAxis.setLabelAutoRotation(30)

        self.rowAxis = QtDataVisualization.QCategory3DAxis()
        self.rowAxis.setTitle('Rows')
        self.rowAxis.setTitleVisible(True)
        self.rowAxis.setLabels(['Row1', 'Row2'])
        self.rowAxis.setLabelAutoRotation(30)

        self.valueAxis = QtDataVisualization.QValue3DAxis()
        self.valueAxis.setTitle('Values')
        self.valueAxis.setTitleVisible(True)
        self.valueAxis.setRange(0, 5)

        self.setRowAxis(self.rowAxis)
        self.setColumnAxis(self.columnAxis)
        self.setValueAxis(self.valueAxis)

        self.series = QtDataVisualization.QBar3DSeries()

        self.arrayData = [[0.1, 0.2, 0.3],
                          [0.3, 0.4, 0.5]]
        self.series.dataProxy().addRows(dataToBarDataArray(self.arrayData))

        self.setPrimarySeries(self.series)

        camera = self.scene().activeCamera()
        camera.setYRotation(22.5)


class GapFillHeatMap(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        ui = self.__load_ui(parent)
        self.setCentralWidget(ui)
        self.resize(ui.frameSize())

        self.setWindowTitle('Qt DataVisualization 3D Bars')

        self.bars = BarsMap3D()

        self.container = QWidget.createWindowContainer(self.bars)

        if not self.bars.hasContext():
            print("Couldn't initialize the OpenGL context.")
            sys.exit(-1)

        # self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.container.setFocusPolicy(Qt.StrongFocus)
        self.container.setParent(ui.widget)

        self.__ui = ui

    def __load_ui(self, parent):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "q3d_bars.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, parent)
        ui_file.close()

        return ui

    def init_resize(self):
        fs = self.__ui.widget.frameSize()
        self.container.resize(fs)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        fs = self.__ui.widget.frameSize()
        self.container.resize(fs)


if __name__ == "__main__":
    from PySide2.QtCore import QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = GapFillHeatMap()
    widget.show()
    widget.init_resize()
    sys.exit(app.exec_())
