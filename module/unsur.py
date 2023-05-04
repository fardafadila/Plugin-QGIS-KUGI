import os
import json
import requests
from urllib import request
import socket

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtCore import (QAbstractTableModel, QStringListModel, pyqtSignal)
from qgis.utils import iface
from .dialog import my_dialog
from .kategori import parse_kategori
from .layer import layer

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)

class parse_unsur(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, kategoriCombo,inputCombo, unsurCombo, FORM_CLASS):
        super().__init__()
        self.kategoriCombo = kategoriCombo
        self.unsurCombo = unsurCombo
        self.inputCombo = inputCombo
        self.FORM_CLASS = FORM_CLASS
        self.kategori_instance = parse_kategori()
        self.daftarUnsur = []        
        self.kategori_instance.getKategori()    
        self.daftar_nama_kategori = self.kategori_instance.daftarNamaKategori    
        self.daftar_id_kategori = self.kategori_instance.daftarIDKategori
        self.zipUnsur = []
        self.listTipe = []
        self.daftarUnsurUnordered = []
        self.dict_kodeUnsur = []
        

    def getSelectedKategori(self):
        self.selectedCategory = self.kategoriCombo.currentText()
        return (self.selectedCategory)
        
    def getKodeURL(self):   
        selectedCategory = self.getSelectedKategori()     
        kode_kategori_dipilih = [k for k, n in zip(self.daftar_id_kategori, self.daftar_nama_kategori) if n == selectedCategory]
        return (kode_kategori_dipilih)
    
    def getUnsur (self, inputCombo):
        a = self.getKodeURL()
        inputID = str(a[0])
        try:
            dialogKategori = my_dialog()
            prog_dialog, label = dialogKategori.progdialog()
            url = "https://kugi.ina-sdi.or.id:8080/kugiapi/featuretype?fcid="
            linkAPI = url+inputID
            response = request.urlopen(linkAPI)
            data = json.loads(response.read())
            #buat daftar unsur dari api unsur (nama dan kode)
            self.daftarUnsurUnordered= []
            self.daftarKode =[]
            self.listNama = []
            self.listTipe =[]
            self.namaUnsurGlobal = []
            for listdata in data:
                #parsing api unsur untuk dapat nama dan kode unsur dan masukin ke daftar kode dan daftar unsur
                unsur = listdata.get('typeName')
                namaUnsur = unsur.strip('@en')
                tipe = namaUnsur[-2:]
                self.listTipe.append(tipe)
                code = listdata.get('code')
                kode1 = code.strip('@en')
                kode = str(kode1[4:6])
                if kode== "01":
                    skala = "1:1.000.000" 
                elif kode== "02":
                    skala  = "1:500.000" 
                elif kode == "03":
                    skala  = "1:250.000"
                elif kode == "04":
                   skala  = "1:100.000"
                elif kode == "05":
                    skala  = "1:50.000"
                elif kode == "06":
                    skala  = "1:25.000"
                elif kode == "07":
                    skala  = "1:10.000"
                elif kode == "08":
                    skala  = "1:5.000"
                elif kode == "09":
                    skala  = "1:2.500"
                elif kode == "10":
                    skala  = "1:1.000"
                else:
                    skala="error"
                definisi1 = listdata.get('definition')
                definisi = definisi1.strip('@en')
                display = namaUnsur  + " | " + kode1 + " \nSkala: " + skala + '\n' + definisi
                self.daftarKode.append(kode1)
                self.daftarUnsurUnordered.append(display) 
                self.listNama.append(namaUnsur)
                self.namaUnsurGlobal.append(namaUnsur)
            self.zipUnsur =zip(self.daftarKode, self.daftarUnsurUnordered)
        
        except socket.timeout:
            error_dialog = QtWidgets.QMessageBox()
            print ("tidak ada sinyal")
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Tidak bisa menghubungi API KUGI. Cek koneksi internet Anda!")
            error_dialog.exec_()
    
    def populateUnsur(self):
        inputlayer = self.inputCombo.currentLayer()
        self.dict_tipe = zip(self.listTipe, self.daftarUnsurUnordered)
        AR_list = []
        LN_list = []
        PT_list = []
        for item in self.dict_tipe:
            if item[0] == 'AR':
                AR_list.append(item[1])
            elif item[0] == 'LN':
                LN_list.append(item[1])
            elif item[0] == 'PT':
                PT_list.append(item[1])      
        listDisplay =None
        tipe_geom = inputlayer.geometryType()
        if tipe_geom == 0:
            listDisplay = PT_list
        elif tipe_geom == 1:
            listDisplay = LN_list
        elif tipe_geom == 2:
            listDisplay = AR_list
            
        self.daftarUnsur = sorted(listDisplay)
        self.unsurCombo.clear()  
        self.unsurCombo.setModel(QStringListModel(self.daftarUnsur))
        self.listView = QtWidgets.QListView()
        self.listView.setWordWrap(True)
        self.unsurCombo.setView(self.listView)
        self.unsurCombo.show()
