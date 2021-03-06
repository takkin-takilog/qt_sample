import sys
import os
import pandas as pd
from PySide2 import QtCore
from PySide2.QtCore import Qt, QDateTime, QDate, QTime, QPointF, QLineF
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow, QHeaderView
from PySide2.QtWidgets import QTableWidgetItem, QAction, QMenu
from PySide2.QtCore import QFile, QDate, Qt, QRegExp, QPoint
from PySide2.QtCore import QAbstractTableModel, QSortFilterProxyModel, QSignalMapper
from PySide2.QtCore import QItemSelectionModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QColor
from PySide2.QtGui import QStandardItemModel, QStandardItem

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

df = pd.DataFrame({'site_codes': ['01', '02', '03', '04'],
                   'status': ['open', 'open', 'open', 'closed'],
                   'Location': ['east', 'north', 'south', 'east'],
                   'data_quality': ['poor', 'moderate', 'high', 'high']})


class PandasModel(QAbstractTableModel):

    def __init__(self, df=pd.DataFrame(), parent=None):
        super().__init__(parent)
        self._df_index_names = df.index.names
        print("----- index_names -----")
        print(" {}".format(self._df_index_names))
        self._df = df.reset_index()
        self._bolds = dict()
        self._colors = dict()

    def toDataFrame(self):
        print("--- toDataFrame ---")
        return self._df.set_index(self._df_index_names)

    def getColumnUnique(self, column_index):
        print("--- getColumnUnique ---")
        return self._df.iloc[:, column_index].unique()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # print("--- headerData ---")
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                try:
                    return self._df.columns.tolist()[section]
                except (IndexError,):
                    return None
            elif role == Qt.FontRole:
                return self._bolds.get(section, None)

            elif role == Qt.ForegroundRole:
                return self._colors.get(section, None)

        elif orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                try:
                    return self._df.index.tolist()[section]
                except (IndexError,):
                    return None
        return None

    def setFiltered(self, section, isFiltered):
        print("--- setIsFiltered ---")
        font = QFont()
        color = QColor()
        if isFiltered:
            font.setBold(True)
            color.setBlue(255)
        self._bolds[section] = font
        self._colors[section] = color
        self.headerDataChanged.emit(Qt.Horizontal, 0, self.columnCount())

    def data(self, index, role=Qt.DisplayRole):
        # print("--- data:{} ---".format(index))
        if role == Qt.DisplayRole:
            if not index.isValid():
                return None
            return str(self._df.iloc[index.row(), index.column()])

        elif role == Qt.UserRole:
            if not index.isValid():
                return None
            return self._df.iloc[index.row(), index.column()]
        else:
            return None

    """
    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            print("AAAAAAAAAAAAAAAAAAAAAAA")
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            print("BBBBBBBBBBBBBBBBBBBBBBB")
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True
    """

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    """
    def sort(self, column, order):
        print("--- sort ---")
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()
    """

    def sortColumn(self, column, ascending):
        print("--- sortColumn ---")
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=ascending, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        print(self._df)
        self.layoutChanged.emit()


class CustomProxyModel(QSortFilterProxyModel):

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
            regex = QRegExp(
                expresion, Qt.CaseInsensitive, QRegExp.RegExp
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

        df = pd.DataFrame({'site_codes': ['01', '02', '03', '04'],
                           'status': ['open', 'open', 'open', 'closed'],
                           'Location': ['east', 'north', 'south', 'east'],
                           'data_quality': ['poor', 'moderate', 'high', 'high']})

        """
        qstd_itm_mdl = QStandardItemModel()
        sel_mdl = QItemSelectionModel(qstd_itm_mdl)
        callback = self._on_selection_ttm_changed
        sel_mdl.selectionChanged.connect(callback)
        ui.treeView.setSelectionModel(sel_mdl)
        """

        model = PandasModel(df)
        proxy = CustomProxyModel()
        proxy.setSourceModel(model)
        ui.treeView.setModel(proxy)

        selmdl = ui.treeView.selectionModel()
        callback = self._on_selection_changed
        selmdl.selectionChanged.connect(callback)

        header = ui.treeView.header()
        header.setSectionsClickable(True)
        callback = self.on_view_header_sectionClicked
        header.sectionClicked.connect(callback)

        callback = self._on_pushButton_setData_clicked
        ui.pushButton_setData.clicked.connect(callback)

        callback = self._on_pushButton_clicked
        ui.pushButton.clicked.connect(callback)

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

    def _on_selection_changed(self, selected, _):
        print("--- _on_selection_changed ---")
        print(" selected:{}".format(selected))

    def _on_pushButton_clicked(self):
        model = self._ui.treeView.model().sourceModel()
        print(model.toDataFrame())
        tv = self._ui.treeView
        proxy = self._ui.treeView.model()
        model_index_list = tv.selectionModel().selectedRows()

        mat = []
        for model_index in model_index_list:
            r = model_index.row()
            row_ = []
            for j in range(model.columnCount()):
                txt = proxy.index(r, j, model_index).data(role=Qt.UserRole)
                row_.append(txt)
            mat.append(row_)
        df = pd.DataFrame(mat,
                          columns=["Date", "Time", "Goto", "o", "h", "l", "c"])
        print("-----")
        df.set_index("Date", inplace=True)
        print(df)

        """
        for ix in tv.selectedIndexes():
            print("AAAAAAAAAAAAAAAAA")
            text = ix.data(Qt.DisplayRole) # or ix.data()
            print(text)
        """
    def _on_pushButton_setData_clicked(self):
        print("--- on_pushButton_setData_clicked ---")
        model = PandasModel(df_org)
        proxy = CustomProxyModel()
        proxy.setSourceModel(model)
        self._ui.treeView.setModel(proxy)

        selmdl = self._ui.treeView.selectionModel()
        callback = self._on_selection_changed
        selmdl.selectionChanged.connect(callback)

    def on_view_header_sectionClicked(self, logicalIndex):
        print("--- on_view_header_sectionClicked ---")

        self.logicalIndex = logicalIndex
        self.menuValues = QMenu()
        self.signalMapper = QSignalMapper()

        model = self._ui.treeView.model().sourceModel()
        # valuesUnique = model._df.iloc[:, self.logicalIndex].unique()
        valuesUnique = model.getColumnUnique(self.logicalIndex)

        # actAll = QAction("All", self)
        actAll = QAction("All")
        actAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actAll)
        self.menuValues.addSeparator()

        actOrderAsc = QAction("Order Asc")
        actOrderAsc.triggered.connect(self.on_actionOrderAsc_triggered)
        self.menuValues.addAction(actOrderAsc)
        actOrderDes = QAction("Order Des")
        actOrderDes.triggered.connect(self.on_actionOrderDes_triggered)
        self.menuValues.addAction(actOrderDes)
        self.menuValues.addSeparator()

        for actNumber, actName in enumerate(sorted(list(set(valuesUnique)))):
            action = QAction(str(actName), self)
            self.signalMapper.setMapping(action, actNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)

        header = self._ui.treeView.header()

        headerPos = self._ui.treeView.mapToGlobal(header.pos())
        posY = headerPos.y() + header.height()
        posX = headerPos.x() + header.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QPoint(posX, posY))

    def on_actionAll_triggered(self):
        print("--- on_actionAll_triggered ---")
        """
        filterColumn = self.logicalIndex
        filterString = QRegExp("",
                               Qt.CaseInsensitive,
                               QRegExp.RegExp
                               )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)
        """
        filterColumn = self.logicalIndex
        proxy = self._ui.treeView.model()
        proxy.setFilter("", filterColumn)

        model = self._ui.treeView.model().sourceModel()
        model.setFiltered(filterColumn, False)

    def on_actionOrderAsc_triggered(self):
        print("--- on_actionOrderAsc_triggered ---")
        orderColumn = self.logicalIndex
        model = self._ui.treeView.model().sourceModel()
        model.sortColumn(orderColumn, True)

    def on_actionOrderDes_triggered(self):
        print("--- on_actionOrderDes_triggered ---")
        orderColumn = self.logicalIndex
        model = self._ui.treeView.model().sourceModel()
        model.sortColumn(orderColumn, False)

    def on_signalMapper_mapped(self, i):
        print("--- on_signalMapper_mapped[{}] ---".format(i))
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        proxy = self._ui.treeView.model()
        proxy.setFilter(stringAction, filterColumn)
        model = proxy.sourceModel()
        model.setFiltered(filterColumn, True)


if __name__ == "__main__":
    from PySide2.QtCore import QCoreApplication
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = TreeView()
    widget.show()
    sys.exit(app.exec_())
