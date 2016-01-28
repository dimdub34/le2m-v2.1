# -*- coding: utf-8 -*-

from PyQt4 import QtCore

from util.utili18n import le2mtrans
from configuration.configconst import HOMME, FEMME


class TableModelJoueurs(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        super(TableModelJoueurs, self).__init__(parent)
        self._headers = ['uid', le2mtrans('Hostname'), 'IP',
                         le2mtrans('Automatic'), le2mtrans('Simulation'),
                         le2mtrans(u'Disconnect')]
        self._joueurs = []

    def ajouter_joueur(self, joueur):
        """
        add the player to the table
        """
        self.insertRow(len(self._joueurs), joueur)

    def enlever_joueur(self, joueur):
        """
        Remove the player from the table
        """
        self.removeRow(self._joueurs.index(joueur), joueur)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._joueurs)

    def columnCount(self, parent=QtCore.QModelIndex()):
        """
        return the length of the header
        :param parent:
        :return: int
        """
        return len(self._headers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._joueurs): 
            return QtCore.QVariant()

        ligne = index.row()
        colonne = index.column()

        # display
        if role == QtCore.Qt.DisplayRole:
            if colonne == 0:
                return QtCore.QVariant(self._joueurs[ligne].uid)
            elif colonne == 1: 
                return QtCore.QVariant(self._joueurs[ligne].hostname)
            elif colonne == 2:
                return QtCore.QVariant(self._joueurs[ligne].ip)
            return QtCore.QVariant()

        # checkbox for automatic, simulation and disconnect
        elif role == QtCore.Qt.CheckStateRole:
            part_base = self._joueurs[ligne].get_part('base')
            if colonne == 3:
                if part_base.automatique:
                    return QtCore.QVariant(QtCore.Qt.Checked)
                else:
                    return QtCore.QVariant(QtCore.Qt.Unchecked)
            elif colonne == 4:
                if part_base.simulation:
                    return QtCore.QVariant(QtCore.Qt.Checked)
                else:
                    return QtCore.QVariant(QtCore.Qt.Unchecked)
            elif colonne == 5:
                return QtCore.QVariant(QtCore.Qt.Unchecked)
            return QtCore.QVariant()

        # alignment in the cells
        elif role == QtCore.Qt.TextAlignmentRole: 
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        else:
            return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        """
        return the header
        """
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole: 
                return QtCore.QVariant(self._headers[col])
            elif role == QtCore.Qt.ToolTipRole:
                if col == 3 or col == 4 or col == 5: 
                    return QtCore.QVariant(
                        le2mtrans(u"Click to inverse selection"))
        return QtCore.QVariant()

    def flags(self, index):
        """
        Only the columns automatic, simulation and disconnect are editables
        """
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        if index.column() == 3 or index.column() == 4 or index.column() == 5:
            return QtCore.Qt.ItemFlags(
                QtCore.QAbstractTableModel.flags(self, index) |
                QtCore.Qt.ItemIsUserCheckable)
        return QtCore.Qt.ItemFlags(
            QtCore.QAbstractTableModel.flags(self, index))

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Only for the editables columns
        """
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            if value == QtCore.Qt.Unchecked:
                etat = 0
            else:
                etat = 1
            part_base = self._joueurs[index.row()].get_part('base')
            if index.column() == 3:
                part_base.set_automatique(etat)
                return True
            elif index.column() == 4:
                part_base.set_simulation(etat)
                return True
            elif index.column() == 5:
                if etat == 1:
                    self._joueurs[index.row()].disconnect()
            return True
        return False

    def insertRow(self, row, joueur, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self._joueurs.append(joueur)
        self.endInsertRows()
        return
  
    def removeRow(self, row, joueur, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, row, row)
        self._joueurs.remove(joueur)
        self.endRemoveRows()

    def inverse(self, colonne):
        """
        inverse selection on columns auto, simul or disconnect
        """
        if colonne == 3:
            for r in range(0, self.rowCount()):
                index = self.createIndex(r, 3)
                if not self._joueurs[r].get_part('base').automatique:
                    self.setData(index, QtCore.Qt.Checked,
                                 QtCore.Qt.CheckStateRole)
                else:
                    self.setData(index, QtCore.Qt.Unchecked,
                                 QtCore.Qt.CheckStateRole)
                self.dataChanged[QtCore.QModelIndex, QtCore.QModelIndex].emit(
                    index, index)

        elif colonne == 4:
            for r in range(0, self.rowCount()):
                index = self.createIndex(r, 4)
                if not self._joueurs[r].get_part('base').simulation:
                    self.setData(index, QtCore.Qt.Checked,
                                 QtCore.Qt.CheckStateRole)
                else:
                    self.setData(index, QtCore.Qt.Unchecked,
                                 QtCore.Qt.CheckStateRole)
                self.dataChanged[QtCore.QModelIndex, QtCore.QModelIndex].emit(
                    index, index)

        elif colonne == 5:
            for r in range(0, self.rowCount()):
                index = self.createIndex(r, 5)
                self.setData(index, QtCore.Qt.Checked, QtCore.Qt.CheckStateRole)
                self.dataChanged[QtCore.QModelIndex, QtCore.QModelIndex].emit(
                    index, index)





class TableModelGenres(QtCore.QAbstractTableModel):
    def __init__(self, joueurs,  parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._headers = ['Hostname', 'Femmes']
        self._joueurs = joueurs

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._joueurs)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._headers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._joueurs): 
            return QtCore.QVariant()
        ligne = index.row()
        colonne = index.column()
        # affichage
        if role == QtCore.Qt.DisplayRole:
            if colonne == 0: 
                return QtCore.QVariant(self._joueurs[ligne].hostname)
            return QtCore.QVariant()
        # pour le genre
        elif role == QtCore.Qt.CheckStateRole:
            if colonne == 1:
                try: 
                    if self._joueurs[ligne].genre == FEMME: 
                        return QtCore.QVariant(QtCore.Qt.Checked)
                    else:
                        return QtCore.QVariant(QtCore.Qt.Unchecked)
                except AttributeError:
                    setattr(self._joueurs[ligne], 'genre', HOMME)
                    return QtCore.QVariant(QtCore.Qt.Unchecked)
        # alignement du texte dans les cellules
        elif role == QtCore.Qt.TextAlignmentRole: 
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        else:
            return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        """
        Return le header de la colonne
        """
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole: 
                return QtCore.QVariant(self._headers[col])
        return QtCore.QVariant()

    def flags(self, index):
        """
        Seule la colonne genre est éditable
        """
        if not index.isValid(): return QtCore.Qt.ItemIsEnabled
        # genre
        if index.column() == 1: 
            return QtCore.Qt.ItemFlags(
                QtCore.QAbstractTableModel.flags(self, index) |
                QtCore.Qt.ItemIsUserCheckable
            )
        return QtCore.Qt.ItemFlags(
            QtCore.QAbstractTableModel.flags(self, index)
        )

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Uniquement pour la seule colonne éditable
        """
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            if value == QtCore.Qt.Unchecked:
                genre = HOMME
            elif value == QtCore.Qt.Checked:
                genre = FEMME
            if index.column() == 1:
                self._joueurs[index.row()].genre = genre
                return True
        return False


class TableModelQuestionnaireFinal(QtCore.QAbstractTableModel):
    def __init__(self, blocs, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = ['Blocs', u'Affiché']
        self.blocs = blocs

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.blocs)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)

    def data(self, index, role = QtCore.Qt.DisplayRole): 
        if not index.isValid() or index.row() >= len(self.blocs): 
            return QtCore.QVariant()
        ligne = index.row()
        colonne = index.column()
        if role == QtCore.Qt.DisplayRole:
            if colonne == 0:
                return QtCore.QVariant(self.blocs[ligne][0])
            return QtCore.QVariant()
        # pour l'état
        elif role == QtCore.Qt.CheckStateRole:
            if colonne == 1:
                if self.blocs[ligne][1]: 
                    return QtCore.QVariant(QtCore.Qt.Checked)
                else:
                    return QtCore.QVariant(QtCore.Qt.Unchecked)
        # alignement du texte dans les cellules
        elif role == QtCore.Qt.TextAlignmentRole: 
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        else:
            return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        """
        Return le header de la colonne
        """
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole:
                return QtCore.QVariant(self.headers[col])
        return QtCore.QVariant()

    def flags(self, index):
        """
        Seule la colonne 1 est éditable
        """
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        # genre
        if index.column() == 1: 
            return QtCore.Qt.ItemFlags(
                QtCore.QAbstractTableModel.flags(self, index) |
                QtCore.Qt.ItemIsUserCheckable
            )
        return QtCore.Qt.ItemFlags(
            QtCore.QAbstractTableModel.flags(self, index)
        )

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        """
        Uniquement pour la seule colonne éditable
        """
        if index.isValid() and role == QtCore.Qt.CheckStateRole:
            if value == QtCore.Qt.Unchecked:
                etat = 0
            elif value == QtCore.Qt.Checked:
                etat = 1
            if index.column() == 1:
                self.blocs[index.row()][1] = etat
                return True
        return False
        

class TableModelPaiements(QtCore.QAbstractTableModel):
    def __init__(self, lignes,  parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.headers = [u'Poste',  u'Gain (euros)']
        self.lignes = lignes

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.lignes)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.headers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self.lignes): 
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole: 
            return QtCore.QVariant(self.lignes[index.row()][index.column()])
        elif role == QtCore.Qt.TextAlignmentRole: 
            return QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter
        else:
            return QtCore.QVariant()

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal:
            if role == QtCore.Qt.DisplayRole: 
                return QtCore.QVariant(self.headers[col])
        return QtCore.QVariant()

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemFlags(
            QtCore.QAbstractTableModel.flags(self, index)
        )

    def insertRow(self, row, ligne, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.lignes.append(ligne)
        self.endInsertRows()
        return
