import sys
import os
import pandas as pd
from PySide2 import QtCore
from PySide2.QtCore import Qt, QDateTime, QDate, QTime, QPointF, QLineF
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow, QHeaderView
from PySide2.QtWidgets import QTableWidgetItem, QAction, QMenu
from PySide2.QtCore import QFile, QDate, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont

"""
data_mat = [
    ["2020/09/01", "1:00", 0, 101, 110, 91, 106],
    ["2020/09/01", "2:00", 0, 102, 112, 90, 103],
    ["2020/09/01", "3:00", 0, 103, 122, 89, 110],
    ["2020/09/01", "4:00", 0, 104, 117, 88, 109],
    ["2020/09/01", "5:00", 0, 105, 123, 85, 117],

    ["2020/09/02", "1:00", 1, 111, 120, 91, 113],
    ["2020/09/02", "2:00", 1, 112, 130, 81, 110],
    ["2020/09/02", "3:00", 1, 113, 125, 61, 111],
    ["2020/09/02", "4:00", 1, 114, 126, 60, 112],
    ["2020/09/02", "5:00", 1, 115, 127, 59, 113],

    ["2020/09/03", "1:00", 0, 121, 150, 61, 110],
    ["2020/09/03", "2:00", 0, 122, 130, 71, 100],
    ["2020/09/03", "3:00", 0, 123, 140, 61, 93],
    ["2020/09/03", "4:00", 0, 124, 135, 62, 90],
    ["2020/09/03", "5:00", 0, 125, 133, 63, 85],

    ["2020/09/04", "1:00", 0, 131, 180, 101, 111],
    ["2020/09/04", "2:00", 0, 132, 170, 91, 106],
    ["2020/09/04", "3:00", 0, 133, 150, 90, 121],
    ["2020/09/04", "4:00", 0, 134, 148, 88, 111],
    ["2020/09/04", "5:00", 0, 135, 145, 85, 101],

    ["2020/09/05", "1:00", 1, 141, 170, 121, 130],
    ["2020/09/05", "2:00", 1, 142, 160, 123, 150],
    ["2020/09/05", "3:00", 1, 143, 180, 111, 125],
    ["2020/09/05", "4:00", 1, 144, 181, 121, 150],
    ["2020/09/05", "5:00", 1, 145, 185, 131, 140],

    ["2020/09/06", "1:00", 1, 151, 190, 131, 152],
    ["2020/09/06", "2:00", 1, 152, 195, 125, 140],
    ["2020/09/06", "3:00", 1, 153, 185, 111, 166],
    ["2020/09/06", "4:00", 1, 154, 187, 101, 156],
    ["2020/09/06", "5:00", 1, 155, 190, 105, 146],

    ["2020/09/07", "1:00", 1, 161, 210, 136, 181],
    ["2020/09/07", "2:00", 1, 162, 185, 142, 166],
    ["2020/09/07", "3:00", 1, 163, 175, 123, 160],
    ["2020/09/07", "4:00", 1, 164, 176, 120, 161],
    ["2020/09/07", "5:00", 1, 165, 180, 110, 150],

    ["2020/09/08", "1:00", 0, 171, 220, 152, 180],
    ["2020/09/08", "2:00", 0, 172, 230, 132, 199],
    ["2020/09/08", "3:00", 0, 173, 200, 101, 144],
    ["2020/09/08", "4:00", 0, 174, 210, 111, 174],
    ["2020/09/08", "5:00", 0, 175, 205, 121, 155],

    ["2020/09/09", "1:00", 0, 181, 250, 91, 204],
    ["2020/09/09", "2:00", 0, 182, 210, 125, 189],
    ["2020/09/09", "3:00", 0, 183, 270, 135, 155],
    ["2020/09/09", "4:00", 0, 184, 271, 133, 145],
    ["2020/09/09", "5:00", 0, 185, 273, 120, 175],

    ["2020/09/10", "1:00", 0, 191, 235, 151, 210],
    ["2020/09/10", "2:00", 0, 192, 245, 160, 202],
    ["2020/09/10", "3:00", 0, 193, 265, 120, 186],
    ["2020/09/10", "4:00", 0, 194, 275, 110, 166],
    ["2020/09/10", "5:00", 0, 195, 270, 115, 156],

]
df_org = pd.DataFrame(data_mat,
                      columns=["Date", "Time", "Goto", "o", "h", "l", "c"])
df_org.set_index("Date", inplace=True)
"""

df = pd.DataFrame({'site_codes': ['01', '02', '03', '04'],
                   'status': ['open', 'open', 'open', 'closed'],
                   'Location': ['east', 'north', 'south', 'east'],
                   'data_quality': ['poor', 'moderate', 'high', 'high']})


class PandasModel(QtCore.QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()
        self.bolds = dict()

    def toDataFrame(self):
        return self._df.copy()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                try:
                    return self._df.columns.tolist()[section]
                except (IndexError,):
                    return None
            elif role == QtCore.Qt.FontRole:
                return self.bolds.get(section, None)
        elif orientation == QtCore.Qt.Vertical:
            if role == QtCore.Qt.DisplayRole:
                try:
                    # return self.df.index.tolist()
                    return self._df.index.tolist()[section]
                except (IndexError,):
                    return None
        return None

    def setFont(self, section, font):
        self.bolds[section] = font
        self.headerDataChanged.emit(QtCore.Qt.Horizontal, 0, self.columnCount())

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return None

        if not index.isValid():
            return None

        return str(self._df.iloc[index.row(), index.column()])

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()


class CustomProxyModel(QtCore.QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._filters = dict()

    @property
    def filters(self):
        return self._filters

    def setFilter(self, expresion, column):
        if expresion:
            self.filters[column] = expresion
        elif column in self.filters:
            del self.filters[column]
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for column, expresion in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()
            regex = QtCore.QRegExp(
                expresion, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp
            )
            if regex.indexIn(text) == -1:
                return False
        return True


class TreeView(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        ui = self._load_ui(parent)
        self.setCentralWidget(ui)
        # self.resize(ui.frameSize())
        self.setWindowTitle("Tree View")

        self.load_sites(ui)

        self.header = ui.treeView.header()
        self.header.setSectionsClickable(True)
        callback = self.on_view_header_sectionClicked
        self.header.sectionClicked.connect(callback)

        self._ui = ui

    def _load_ui(self, parent):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "tree_view.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, parent)
        ui_file.close()

        return ui

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def load_sites(self, ui):
        """
        df = pd.DataFrame({'site_codes': ['01', '02', '03', '04'],
                           'status': ['open', 'open', 'open', 'closed'],
                           'Location': ['east', 'north', 'south', 'east'],
                           'data_quality': ['poor', 'moderate', 'high', 'high']})
        """

        self.model = PandasModel(df)
        self.proxy = CustomProxyModel(self)
        self.proxy.setSourceModel(self.model)
        ui.treeView.setModel(self.proxy)
        # ui.treeView.resizeColumnsToContents()
        print("finished loading sites")

    def on_view_header_sectionClicked(self, logicalIndex):
        print("--- on_view_header_sectionClicked ---")

        self.logicalIndex = logicalIndex
        self.menuValues = QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self)
        """
        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)
        """

        valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()

        #actionAll = QAction("All", self)
        actionAll = QAction("All")
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()
        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            #action = QAction(actionName, self)
            print(type(actionName))
            print(actionName)
            action = QAction(actionName)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        headerPos = self._ui.treeView.mapToGlobal(self.header.pos())
        posY = headerPos.y() + self.header.height()
        posX = headerPos.x() + self.header.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    def on_actionAll_triggered(self):
        print("--- on_actionAll_triggered ---")
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp("",
                                      QtCore.Qt.CaseInsensitive,
                                      QtCore.QRegExp.RegExp
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    def on_signalMapper_mapped(self, i):
        print("--- on_signalMapper_mapped[{}] ---".format(i))
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        self.proxy.setFilter(stringAction, filterColumn)
        font = QFont()
        font.setBold(True)
        self.model.setFont(filterColumn, font)


if __name__ == "__main__":
    from PySide2.QtCore import QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = TreeView()
    widget.show()
    sys.exit(app.exec_())