import os, time
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtCore
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QApplication, QProgressBar, QDialog, QVBoxLayout
from qgis.PyQt.QtGui import *
from qgis.core import *
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)


class my_dialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=iface.mainWindow()): 
        super(my_dialog, self).__init__(parent)
        self.setupUi(self)

    def progdialog(self):
        progressMessageBar = iface.messageBar().createMessage("Sedang memproses...")
        progress = QProgressBar()
        progress.setMaximum(10)
        progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(33, 37, 43, 180);
                border-radius: 15px;
                text-align: center;
                background-color: rgba(33, 37, 43, 180);
                color: black;
            }
            QProgressBar::chunk {
                background-color: #34ad43;
            }
        """)
        progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        progressMessageBar.layout().addWidget(progress)
        iface.messageBar().pushWidget(progressMessageBar, level = Qgis.Info, duration = 1)
        for i in range(10):
            time.sleep(0.15)
            progress.setValue(i + 1)

        #iface.messageBar().clearWidgets()
        dialog = progress
        label = progressMessageBar
        return dialog, label


    


    



        
      
