import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPen, QLinearGradient, QColor, QGradient
from PySide2.QtCore import QPointF, Qt

app = QApplication([])

upperSeries = QtCharts.QLineSeries()
lowerSeries = QtCharts.QLineSeries()

#x = [x for x in range(1, 20, 2)]
#y1 = [5, 7, 6, 7, 5, 7, 5, 4, 7, 5]
#y2 = [3, 4, 2, 5, 3, 5, 2, 1, 4, 2]
x = [x for x in range(1, 3, 1)]
y1 = [5, 7]
y2 = [3, 4]

for i in range(len(x)):
    upperSeries.append(x[i], y1[i])
    lowerSeries.append(x[i], y2[i])

series = QtCharts.QAreaSeries(upperSeries, lowerSeries)

pen = QPen(Qt.red)
pen.setWidth(3)
series.setPen(pen)

gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
gradient.setColorAt(0.0, QColor(255, 255, 255))
gradient.setColorAt(1.0, QColor(0, 255, 0))
gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
series.setBrush(gradient)

chart = QtCharts.QChart()
chart.addSeries(series)
chart.setTitle('Simple Area Chart')
chart.legend().hide()
chart.createDefaultAxes()
chart.axes(Qt.Horizontal)[0].setRange(0, 3)
chart.axes(Qt.Vertical)[0].setRange(0, 10)

chartView = QtCharts.QChartView(chart)
chartView.setWindowTitle('Area Chart')
chartView.resize(800, 600)
chartView.show()

app.exec_()
