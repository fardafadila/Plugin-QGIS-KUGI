import os
import json
from urllib import request

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets, QtCore
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import (QVariant, QFileInfo)
from qgis.utils import iface
from qgis.core import (QgsFeatureRequest, QgsField, QgsProject, 
                       QgsCoordinateReferenceSystem, QgsVectorLayer, QgsVectorFileWriter)
from .dialog import my_dialog
from .attribute import parse_struktur
from .mapping_table import combo_table

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
ui_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..', 'kugi', 'kugi_dialog_base.ui'))

# Load the UI file
FORM_CLASS, _ = uic.loadUiType(ui_path)

class output_c(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, inputCombo, fieldTable, unsurCombo, kategoriCombo, FORM_CLASS):
        super().__init__()
        self.FORM_CLASS = FORM_CLASS
        self.inputCombo = inputCombo
        self.fieldTable = fieldTable
        self.unsurCombo = unsurCombo
        self.kategoriCombo = kategoriCombo
        self.struktur_instance = parse_struktur(unsurCombo, kategoriCombo, inputCombo, self)
        self.get_matched = combo_table.get_matched()

    def coba_rename(self):
            layer = self.inputCombo.currentLayer()
            prov = layer.dataProvider()
            field_names = [field.name() for field in prov.fields()]
            fields = layer.dataProvider().fields()
            print (fields)
            target_field = "new"
            idx = field_names.index(target_field)
            layer.startEditing()
            layer.deleteAttribute(idx)
            layer.commitChanges()
            print ("masuk fungsi coba_rename")

    def adding_attributes(self):
        #run = self.get_matched()
        #FUNGSI PASTIKAN TIPE DATA MAPPING FIELD SUDAH SAMA
        
        attDict,_, _ = self.struktur_instance.getStruktur()
        layerAwal = self.inputCombo.currentLayer()
        layer = layerAwal.materialize(QgsFeatureRequest().setFilterFids(layerAwal.allFeatureIds()))
        num = 0
        kolomBaru = self.get_matched()
        listDihapus = []
        notMatched = "-"
        for satu, dua in kolomBaru.items():
            if dua != notMatched:
                listDihapus.append(satu)
        #print (listDihapus)
        listAtribut = self.matchedList
        #print (listAtribut)
        listRename = []
        for item in listAtribut:
            if item != "-":
                listRename.append(item)
        print(listRename)
        listAdd = attDict.copy()
        for key in listRename:
            if key in attDict:
                del listAdd[key]
        print (listAdd) 
        ####FUNGSI ADD ATRIBUT
        for x, y in attDict.items():
            print ("masuk fungsi penambahan field")
            #print (x)
            num += 1
            if y == "Integer":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.Int)])
            elif y == "Int64":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.Int64)])
            elif y == "Double":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.Double)])
            elif y == "String":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.String)])
            elif y == "OID":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.Int)])
                """
                oid_idx = layer.fields().indexFromName("OBJECTID")
                for feat in layer.getFeatures():
                    layer.changeAttributeValue(feat.id(), oid_idx, feat.id())
                """
            elif y == "Date":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.Date)])
            elif y == "Geometry":
                layer.dataProvider().addAttributes([QgsField(x, QVariant.String)])
            else:
                self.QtWidgets.QMessageBox.warning("Tipe data tidak sesuai")
        layer.commitChanges()
        ####END FUNGSI ADD ATRIBUT

        #FUNGSI BUAT COPY VALUE DARI FIELD AWAL KE AKHIR
        prov = layer.dataProvider()
        field_names = [field.name() for field in prov.fields()]
        fields = layer.dataProvider().fields()
        for awal, akhir in kolomBaru.items():
            print ("masuk fungsi copy value")
            #KALAU PADANANNYA BUKAN -
            if akhir != notMatched:            
                #print ("masuk fungsi copy value")
                
                origin_field = awal
                target_field = akhir
                idx = layer.fields().indexFromName(target_field)
                idy = layer.fields().indexFromName(origin_field)
                #print (fields)
                for field in fields:
                    layer.startEditing()
                    for feat in layer.getFeatures():
                        #print (feat[origin_field])
                        layer.changeAttributeValue(feat.id(), idx, feat[origin_field])
                #layer.deleteAttribute(idy)
                layer.commitChanges()

        self.listFieldKugi = []
        
        prov = layer.dataProvider()
        field_namesUpdated = [field.name() for field in prov.fields()] 
        jumlah_fieldUpdated = 0
        self.namaFieldLayerUpdated= []
        for count, f in enumerate(field_namesUpdated):
            self.namaFieldLayerUpdated.append(f)
            jumlah_fieldUpdated +=1
        print (self.namaFieldLayerUpdated)
        layer.startEditing()
        for namaKolom in self.namaFieldLayerUpdated:
            for harusDihapus in listDihapus:
                if namaKolom == harusDihapus:
                    print ("masuk hapus")
                    idx = layer.fields().indexFromName(namaKolom)
                    print(idx)
                    layer.deleteAttribute(idx)
            layer.updateFields()
        layer.commitChanges()
        return (layer, self.namaFieldLayerUpdated)

    def set_att_value (self):
        self.layerHasil, _ = self.adding_attributes()
        _, mauDiisi = self.adding_attributes()
        attDict,_, _ = self.struktur_instance.getStruktur()
        _, inputKode, _ = self.struktur_instance.getStruktur()
        fcode = str(inputKode)
        self.layerHasil.startEditing()
        prov = self.layerHasil.dataProvider()
        crsLayer1 = self.layerHasil.crs()
        crsLayer = str(crsLayer1).strip('<QgsCoordinateReferenceSystem: EPSG:>')
        field_names = [field.name() for field in prov.fields()]
        for count, f in enumerate(field_names):
            self.namaField.append(f)
        for x in mauDiisi:
            if  x== "FCODE":
                self.layerHasil.dataProvider().addAttributes([QgsField(x, QVariant.Int)])
                field_idx = self.layerHasil.fields().indexOf('FCODE')
                fcode_value = fcode
                for feat in self.layerHasil.getFeatures():
                    self.layerHasil.changeAttributeValue(feat.id(), field_idx, fcode_value)
            elif x == "SRS_ID":
                self.layerHasil.dataProvider().addAttributes([QgsField(x, QVariant.Int)])
                field_idx = self.layerHasil.fields().indexOf('SRS_ID')
                srs_value = crsLayer
                for feat in self.layerHasil.getFeatures():
                    self.layerHasil.changeAttributeValue(feat.id(), field_idx, srs_value)
                
        self.layerHasil.commitChanges()        
        shapefileName = self.getOutFolder()
        if shapefileName == "":
            QgsProject.instance().addMapLayer(self.layerHasil) 
        else:
            crs = QgsCoordinateReferenceSystem()
            crs.createFromId(QgsProject.instance().crs().postgisSrid())
            writer = QgsVectorFileWriter.writeAsVectorFormat(self.layerHasil, shapefileName, "utf-8", crs, "ESRI Shapefile")
            fileInfo = QFileInfo(shapefileName)
            baseName = fileInfo.baseName()
            self.layer = QgsVectorLayer(shapefileName, baseName, "ogr")
            QgsProject.instance().addMapLayer(self.layer) 

    def outFolder(self):
        outFolder = QgsProject.instance().homePath()
        # Get the text from the QLineEdit and use it as the shapefile name
        shapefileName, _ = QFileDialog.getSaveFileName(self, "Save Shapefile", outFolder, "ESRI Shapefile (*.shp)")
        self.saveEdit.insert(shapefileName)
      
    def getOutFolder(self):
        return(self.saveEdit.text())
