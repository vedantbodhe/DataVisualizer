import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Visualization Tool')
        self.setGeometry(100, 100, 800, 600)

        # Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')

        openFile = QAction('Open CSV', self)
        openFile.triggered.connect(self.openFileDialog)
        fileMenu.addAction(openFile)

        # Chart Display Area
        self.chartLayout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.chartLayout)
        self.setCentralWidget(self.widget)

    def openFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
        if fileName:
            print(f"Opening file: {fileName}")
            self.loadAndPlotData(fileName)

    def loadAndPlotData(self, fileName):
        # Load data
        data = pd.read_csv(fileName)
        print(f"Data loaded: {data.head()}")  # Debugging: Print first few rows of the data

        # Clear previous plot if any
        self.clearLayout(self.chartLayout)

        # Create a figure and canvas for the plot
        fig, ax = plt.subplots()
        ax.plot(data.iloc[:,0], data.iloc[:,1])  # Assuming two columns of data
        ax.set_title('Data Plot')
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')

        # Display plot
        canvas = FigureCanvas(fig)
        self.chartLayout.addWidget(canvas)
        canvas.draw()

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
