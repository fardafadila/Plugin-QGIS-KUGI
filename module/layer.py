import os


from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.utils import iface
from qgis.PyQt.QtCore import (QAbstractTableModel, QVariant, QStringListModel, pyqtSignal,QFileInfo,QUrl)
from qgis.PyQt.QtGui import QDesktopServices
from qgis.core import (QgsVectorLayerCache, QgsFeatureRequest, QgsField, QgsProject, QgsWkbTypes, QgsCoordinateReferenceSystem,
                        QgsVectorLayer, QgsVectorFileWriter)
from qgis.gui import (QgsAttributeTableModel, QgsAttributeTableView, QgsAttributeTableFilterModel)


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)

class layer(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, inputCombo, fieldTable, FORM_CLASS):
        """Constructor."""
        super(layer, self).__init__()
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect 
        self.setupUi(self)
        self.inputLayer = inputCombo
        self.fieldTable = fieldTable
        self.layerEdit = None
    
    def get_selected_layer(self, inputLayer):
        self.inputLayer = self.inputLayer
        selected_layer = self.inputLayer.currentLayer()
        return (selected_layer)
    

    def getLayer(self):
        project = QgsProject.instance()
        layer_list = project.mapLayers()
        num_layers = len(layer_list)
        if num_layers >0:
            self.layerEdit = self.get_selected_layer(self.inputLayer)
            prov = self.layerEdit.dataProvider()
            #dapatkan list field dari layer yang dipilih
            field_names = [field.name() for field in prov.fields()]
            self.fieldTable.clear()
            #buat list nama dan tipe field
            namaField = []
            tipeData = []
            #hitung ada berapa field 
            jumlah_field = 0
            #masukin nama dan tipe field ke list
            for count, f in enumerate(field_names):
                namaField.append(f)
                jumlah_field +=1
            for field in self.layerEdit.fields():
                tipe_data = field.typeName()
                tipeData.append(tipe_data)
            #definisiin ada tiga kolom dan buat header
            self.fieldTable.setColumnCount(3)
            self.fieldTable.setHorizontalHeaderLabels(['Nama Kolom', 'Tipe Data', 'Nama Kolom Baru'])
            #atur ukuran kolom terakhir supaya tabel penuh
            self.fieldTable.horizontalHeader().setStretchLastSection(True)

            #buat baris sebanyak jumlah field
            self.fieldTable.setRowCount(jumlah_field)
            for index in range(jumlah_field):
                #buat list item1 untuk nama field
                item1 = QtWidgets.QTableWidgetItem(namaField[index])
                #masukkan nama field secara berulang tiap baris dengan index
                self.fieldTable.setItem(index,0,item1)
                #buat list item2 untuk tipe field
                item2 = QtWidgets.QTableWidgetItem(tipeData[index])
                #masukkan tipe field secara berulang tiap baris dengan index
                self.fieldTable.setItem(index,1,item2)
            #atur ukuran tabel
            self.fieldTable.setColumnWidth(0,275)
            self.fieldTable.setColumnWidth(1,185)
        else:
            error_dialog = QtWidgets.QMessageBox()
            print ("belum ada layer")
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Tambahkan layer pada project QGIS Anda terlebih dahulu!")
            error_dialog.exec_()

        