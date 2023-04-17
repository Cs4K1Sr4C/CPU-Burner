import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor
import psutil


class Worker(QThread):
    cpuUsageSignal = pyqtSignal(float)
    cpuTempSignal = pyqtSignal(float)
    overheatSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        while True:
            cpuUsage = psutil.cpu_percent(interval=1)
            self.cpuUsageSignal.emit(cpuUsage)
            cpuTemp = psutil.sensors_temperatures()['coretemp'][0].current
            self.cpuTempSignal.emit(cpuTemp)
            if cpuTemp >= 80:  # Check if CPU temperature is above 80°C
                self.overheatSignal.emit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ultra-Fast Processor Burner Application')
        self.setGeometry(150, 150, 500, 500)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        font = QFont()
        font.setPointSize(16)
        font.setBold(True)

        self.cpu_usage_label = QLabel(self.central_widget)
        self.cpu_usage_label.setText('CPU Usage: 0.0%')
        self.cpu_usage_label.setFont(font)
        self.cpu_usage_label.setAlignment(Qt.AlignCenter)
        self.cpu_usage_label.setGeometry(50, 50, 400, 100)

        self.cpu_temp_label = QLabel(self.central_widget)
        self.cpu_temp_label.setText('CPU Temperature: 0.0°C')
        self.cpu_temp_label.setFont(font)
        self.cpu_temp_label.setAlignment(Qt.AlignCenter)
        self.cpu_temp_label.setGeometry(50, 150, 400, 100)

        self.slider = QSlider(Qt.Horizontal, self.central_widget)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setGeometry(50, 300, 400, 30)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.valueChanged[int].connect(self.changeValue)

        self.workerThread = Worker(self)
        self.workerThread.cpuUsageSignal.connect(self.updateCpuUsage)
        self.workerThread.cpuTempSignal.connect(self.updateCpuTemp)
        self.workerThread.overheatSignal.connect(self.handleOverheat)
        self.workerThread.start()

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        self.show()

    def changeValue(self, value):
        # Calculate the CPU stress levels based on the slider value
        stressLevels = (value / 100) ** 2
        for i in range(int(1000000 * stressLevels)):
            for j in range(100):
                for k in range(100):
                    pass  # Add a loop that burns CPU cycles based on the calculated stress levels


    def updateCpuUsage(self, cpuUsage):
        self.cpu_usage_label.setText(f'CPU Usage: {cpuUsage:.1f}%')

    def updateCpuTemp(self, cpuTemp):
        self.cpu_temp_label.setText(f'CPU Temperature: {cpuTemp:.1f}°C')

    def handleOverheat(self):
        # Display a warning message box when CPU temperature exceeds 80°C
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Warning)
        messageBox.setWindowTitle('Overheating Warning')
        messageBox.setText('The CPU temperature is getting too high. Do you want to continue using the application?')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        messageBox.setDefaultButton(QMessageBox.No)
        response = messageBox.exec_()
        if response == QMessageBox.No:
            os._exit(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
