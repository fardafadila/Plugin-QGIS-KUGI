import os
import json
import requests
from urllib import request

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtCore
from qgis.utils import iface
from qgis.utils import iface
from .dialog import my_dialog

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)


class parse_kategori(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=iface.mainWindow()): 
        super(parse_kategori, self).__init__(parent)
        self.setupUi(self)
        self.zipped_kategori = None

    def getKategori(self):
        try:
            dialogKategori = my_dialog()
            prog_dialog, label = dialogKategori.progdialog()
            urlKategori = "https://kugi.ina-sdi.or.id:8080/kugiapi/featurecatalog"
            response = requests.get(urlKategori)
            responseKategori = request.urlopen(urlKategori)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            #definisi variabel dataKategori = response url kategori
            dataKategori = json.loads(responseKategori.read())
            #dapatkan list nama kategori
            self.daftarNamaKategori = []
            self.daftarIDKategori =[]
            for kategoriList in dataKategori:
                namaKategori = kategoriList.get('name')
                trimmedKategori = namaKategori.strip('@en')
                self.daftarNamaKategori.append(trimmedKategori)
                id = kategoriList.get('id')
                idKategori = id.strip('@en')
                self.daftarIDKategori.append(idKategori)
            self.daftarKategoriSorted = sorted(self.daftarNamaKategori)
            self.zipped_kategori = zip(self.daftarIDKategori, self.daftarNamaKategori)   

        except requests.exceptions.RequestException:
            error_dialog = QtWidgets.QMessageBox()
            print ("tidak ada sinyal")
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Tidak bisa menghubungi API KUGI. Cek koneksi internet Anda!")
            error_dialog.exec_()