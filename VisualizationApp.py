import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import openpyxl


class VisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.currentData = None
        self.currentFigure = None

    def initUI(self):
        self.setWindowTitle('Data Visualization Tool')
        self.setGeometry(100, 100, 1000, 800)

        # Main Layout
        self.mainLayout = QVBoxLayout()

        # Buttons for actions
        self.openCSVButton = QPushButton('Open CSV File')
        self.openCSVButton.clicked.connect(lambda: self.openFileDialog('CSV Files (*.csv)'))
        self.mainLayout.addWidget(self.openCSVButton)

        self.openExcelButton = QPushButton('Open Excel File')
        self.openExcelButton.clicked.connect(lambda: self.openFileDialog('Excel Files (*.xlsx)'))
        self.mainLayout.addWidget(self.openExcelButton)

        self.linePlotButton = QPushButton('Line Plot')
        self.linePlotButton.clicked.connect(lambda: self.plotData('line'))
        self.mainLayout.addWidget(self.linePlotButton)

        self.barPlotButton = QPushButton('Bar Plot')
        self.barPlotButton.clicked.connect(lambda: self.plotData('bar'))
        self.mainLayout.addWidget(self.barPlotButton)

        self.scatterPlotButton = QPushButton('Scatter Plot')
        self.scatterPlotButton.clicked.connect(lambda: self.plotData('scatter'))
        self.mainLayout.addWidget(self.scatterPlotButton)

        self.histogramButton = QPushButton('Histogram')
        self.histogramButton.clicked.connect(lambda: self.plotData('hist'))
        self.mainLayout.addWidget(self.histogramButton)

        self.savePlotButton = QPushButton('Save Plot')
        self.savePlotButton.clicked.connect(self.savePlot)
        self.mainLayout.addWidget(self.savePlotButton)

        # Chart Display Area
        self.chartLayout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.chartLayout)
        self.mainLayout.addWidget(self.widget)

        # Set the main layout
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def openFileDialog(self, fileType):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", fileType, options=options)
        if fileName:
            self.loadData(fileName)

    def loadData(self, fileName):
        if fileName.endswith('.csv'):
            self.currentData = pd.read_csv(fileName)
        elif fileName.endswith('.xlsx'):
            self.currentData = pd.read_excel(fileName)
        print(f"Data loaded: {self.currentData.head()}")

    def plotData(self, plotType):
        if self.currentData is None:
            print("No data loaded")
            return

        try:
            self.clearLayout(self.chartLayout)
            self.currentFigure = Figure()
            ax = self.currentFigure.add_subplot(111)

            if plotType == 'line':
                ax.plot(self.currentData.iloc[:, 0], self.currentData.iloc[:, 1])
            elif plotType == 'bar':
                ax.bar(self.currentData.iloc[:, 0], self.currentData.iloc[:, 1])
            elif plotType == 'scatter':
                ax.scatter(self.currentData.iloc[:, 0], self.currentData.iloc[:, 1])
            elif plotType == 'hist':
                ax.hist(self.currentData.iloc[:, 0])

            ax.set_title(f'{plotType.capitalize()} Plot')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')

            canvas = FigureCanvas(self.currentFigure)
            self.chartLayout.addWidget(canvas)
            canvas.draw()
        except Exception as e:
            print(f"Error: {e}")

    def savePlot(self):
        if self.currentFigure is not None:
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png)", options=options)
            if filePath:
                self.currentFigure.savefig(filePath)
                print(f"Plot saved: {filePath}")
        else:
            print("No plot to save")

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


def main():
    app = QApplication(sys.argv)
    ex = VisualizationApp()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
