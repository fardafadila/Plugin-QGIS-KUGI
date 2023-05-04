import os
import json
import requests
from urllib import request

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtCore import (QAbstractTableModel, QStringListModel, pyqtSignal)
from qgis.utils import iface
from .dialog import my_dialog
from .unsur import parse_unsur
from .attribute import parse_struktur

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)

class combo_table(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, inputCombo, fieldTable, unsurCombo, kategoriCombo, FORM_CLASS):
        super().__init__()
        self.FORM_CLASS = FORM_CLASS
        self.inputCombo = inputCombo
        self.fieldTable = fieldTable
        self.unsurCombo = unsurCombo
        self.kategoriCombo = kategoriCombo
        self.struktur_instance = parse_struktur(unsurCombo, kategoriCombo, inputCombo, self)
        
    def getSelectedLayer(self):
        layer = self.inputCombo.currentLayer()
        prov = layer.dataProvider()
        #dapatkan list field dari layer yang dipilih
        field_names = [field.name() for field in prov.fields()]
        #buat list nama dan tipe field
        namaField = []
        tipeData = []
        #hitung ada berapa field 
        jumlah_field = int(0)
        #masukin nama dan tipe field ke list
        for count, f in enumerate(field_names):
            namaField.append(f)
            jumlah_field +=1
        return (jumlah_field)
    
    def makeCombo(self):
        jumlah_field = self.getSelectedLayer()
        self.listCombo= []
        for index in range(jumlah_field):
            combo = QtWidgets.QComboBox()
            self.listCombo.append(combo)
            self.fieldTable.setCellWidget(index,2,combo)
        return(self.listCombo)  
    
    def populateCombo(self):
        self.displayDaftarStruktur, _ = self.struktur_instance.getStruktur()
        print ("masuuuuuk")
        jumlah_field = self.getSelectedLayer()
        for index in range(jumlah_field):
            combo = self.makeCombo()            
            cek = self.unsurCombo.currentText()
            if cek == "" :
                skip = []
                for t in skip:
                    for listCombo in combo:
                        print ("ke sinii")
                        listCombo.addItem(t)
            else :
                for t in self.displayDaftarStruktur:
                    listComboCoba =[]
                    for listCombo in combo:
                        listCombo.addItem(t)
                        listComboCoba.append(listCombo)   
        