import sys
import os
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader


class TableWidget(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        ui = self._load_ui(parent)
        self.setCentralWidget(ui)
        self.setWindowTitle("Table Widget")

        for i in range(ui.tableWidget.rowCount()):
            ui.tableWidget.setRowHeight(i, (i + 1) * 100)

        self._ui = ui

    def _load_ui(self, parent):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "table_widget.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, parent)
        ui_file.close()

        return ui

    def resizeEvent(self, event):
        super().resizeEvent(event)

if __name__ == "__main__":
    from PySide2.QtCore import QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = TableWidget()
    widget.show()
    sys.exit(app.exec_())
