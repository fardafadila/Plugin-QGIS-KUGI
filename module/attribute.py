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

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)

class parse_struktur(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, unsurCombo, kategoriCombo, inputCombo, FORM_CLASS):
        super().__init__()
        self.FORM_CLASS = FORM_CLASS
        self.kategoriCombo = kategoriCombo
        self.inputCombo = inputCombo
        self.unsurCombo = unsurCombo
        self.displayDaftarStruktur = []
        self.dictStrukturTipe = []
 
        

    def getSelectedUnsur(self):
        self.selectedUnsur = self.unsurCombo.currentText()
        #print (self.selectedUnsur)
        return (self.selectedUnsur)
        
    def getStruktur(self):
        unsurDipilih = self.getSelectedUnsur()
        #kodeUnsur = unsurDipilih.split("|")[1].split()[0]
        print ("unsur dipilih       " +unsurDipilih)
        tes = ""
        if unsurDipilih != tes:
            partsKode = unsurDipilih.split("|")
            partKode2 = partsKode[1]
            parse_kode = partKode2.split()
            kodeUnsur = parse_kode[0]
            print("HASIL KODENYA            " +kodeUnsur)
            inputKode = str(kodeUnsur)
            urlStruktur = 'https://kugi.ina-sdi.or.id:8080/kugiapi/featuretypegetbycode?code='
            responseStruktur = request.urlopen(urlStruktur+inputKode)
            data = json.loads(responseStruktur.read())
            displayDaftarStrukturRedundan =['-']
            daftarStruktur =[]
            tipeDataStruktur = []
            for listStruktur in data:
                struktur = listStruktur.get('ptMemberName')
                definisi = listStruktur.get('ptDefinition')
                tipeData = listStruktur.get('faValueType')
                fcode = listStruktur.get('code')
                displayStruktur = struktur + ' | '  +definisi + ' (Tipe data: ' + tipeData + ')'
                daftarStruktur.append(struktur)
                tipeDataStruktur.append(tipeData)
                displayDaftarStrukturRedundan.append(displayStruktur)                
            displayDaftarStrukturUnordered = [*set(displayDaftarStrukturRedundan)]
            self.displayDaftarStruktur = sorted(displayDaftarStrukturUnordered)
            self.dictStrukturTipe = dict(zip(daftarStruktur, tipeDataStruktur))
        
        for a in self.displayDaftarStruktur:
            print (a)

        return (self.displayDaftarStruktur, self.dictStrukturTipe)

   