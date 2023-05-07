# -*- coding: utf-8 -*-
"""
/***************************************************************************
 kugiDialog
                                 A QGIS plugin
 Mengubah struktur data atribut sesuai standar KUGI
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-12-26
        git sha              : $Format:%H$
        copyright            : (C) 2022 by UGM
        email                : fardafadila48@gmail.com
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import json
from urllib import request
from time import time, gmtime, strftime
from .module.kategori import parse_kategori
from .module.unsur import parse_unsur
from .module.layer import layer
from .module.attribute import parse_struktur
from .module.mapping_table import combo_table


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
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'kugi_dialog_base.ui'))

class kugiDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(kugiDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect 
        self.setupUi(self)
        masuk = parse_kategori()
        masuk.getKategori()
        self.layer_instance = layer(self.inputCombo, self.fieldTable, self)
        self.layer_instance.getLayer()
        displayKategori = masuk.daftarKategoriSorted
        self.unsur = parse_unsur(self.kategoriCombo, self.inputCombo, self.unsurCombo, self)
        displayUnsur = self.unsur.daftarUnsur
        self.mapping_instance = combo_table(self.inputCombo, self.fieldTable, self.unsurCombo, self.kategoriCombo, self)
        self.atribut_instance = parse_struktur(self.unsurCombo, self.kategoriCombo, self.inputCombo, self)
        
        
        self.kategoriCombo.addItems(displayKategori)
        self.kategoriCombo.currentTextChanged.connect(self.unsur.getUnsur)
        self.kategoriCombo.currentTextChanged.connect(self.unsur.populateUnsur)
        self.inputCombo.currentTextChanged.connect(self.layer_instance.getLayer)
        self.unsurCombo.addItems(displayUnsur)        
        self.unsurCombo.currentTextChanged.connect(self.mapping_instance.populateCombo)
        self.inputCombo.currentTextChanged.connect(self.unsur.populateUnsur)
        self.inputCombo.currentTextChanged.connect(self.mapping_instance.makeCombo)
        self.cancelButton.clicked.connect(self.mapping_instance.get_matched)


      
