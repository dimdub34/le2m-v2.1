# -*- coding: utf-8 -*-

from PyQt4 import QtCore 


class TableModelHistorique(QtCore.QAbstractTableModel):
    """
    Table model qui est utilisé à la fois par l'historique et par le
    récapitulatif.
    """
    def __init__(self, historique):
        super(TableModelHistorique, self).__init__()
        self._header = historique[0]
        self._data = historique[1:]
        
    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._header)

    def data(self, index, role=QtCore.Qt.DisplayRole): 
        if not index.isValid():
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self._data[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        else:
            return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self._header[col])
        return QtCore.QVariant()

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemFlags(
            QtCore.QAbstractTableModel.flags(self, index)
        )

