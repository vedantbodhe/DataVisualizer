import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QVBoxLayout, QWidget, QMenuBar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class VisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Visualization Tool')
        self.setGeometry(100, 100, 800, 600)

        # Main Layout
        self.mainLayout = QVBoxLayout()

        # Menu Bar
        self.menuBar = QMenuBar()
        fileMenu = self.menuBar.addMenu('File')
        openFile = QAction('Open CSV', self)
        openFile.triggered.connect(self.openFileDialog)
        fileMenu.addAction(openFile)
        self.mainLayout.addWidget(self.menuBar)

        # Chart Display Area
        self.chartLayout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.chartLayout)
        self.mainLayout.addWidget(self.widget)

        # Set the main layout
        centralWidget = QWidget()
        centralWidget.setLayout(self.mainLayout)
        self.setCentralWidget(centralWidget)

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
        if fileName:
            print(f"Opening file: {fileName}")
            self.loadAndPlotData(fileName)

    def loadAndPlotData(self, fileName):
        try:
            # Load data
            data = pd.read_csv(fileName)
            print(f"Data loaded:\n {data.head()}")

            # Clear previous plot if any
            self.clearLayout(self.chartLayout)

            # Create a figure and canvas for the plot
            fig, ax = plt.subplots()
            ax.plot(data.iloc[:,0], data.iloc[:,1])
            ax.set_title('Data Plot')
            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')

            # Display plot
            canvas = FigureCanvas(fig)
            self.chartLayout.addWidget(canvas)
            canvas.draw()
        except Exception as e:
            print(f"Error: {e}")

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
