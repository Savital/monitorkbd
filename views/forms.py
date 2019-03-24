# Savital https://github.com/Savital
# views.py MainForm view

from PyQt5 import uic, QtWidgets, QtGui, QtSql, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *

import string

class BaseForm(QWidget):
    messages = {"EXIT" : ["Сообщение", "Вы точно хотите выйти?"],
                "EMPTY_NAME" : ["Ошибка", "Остались незаполненные поля."],
                "ALREADY_EXIST" : ["Ошибка", "Данное имя уже присутствует в базе данных."],
                "DOESNT_EXIST" : ["Ошибка", "Данного имени нет в базе данных."],
                "WRONG_FORMAT" : ["Ошибка", "Неправильный формат имени."],
                "LKM_MISSING" : ["Ошибка", "Отсутсвует модуль сбора статистики."],
                "USER_MISSING" : ["Ошибка", "Отсутствуют пользователи в базе данных."]}

    initWindowSignal = QtCore.pyqtSignal()
    changeUserStateSignal = QtCore.pyqtSignal(list)

    monitoringSignal = QtCore.pyqtSignal()
    addUserSignal = QtCore.pyqtSignal(list)
    deleteUserSignal = QtCore.pyqtSignal(list)
    clearLogSignal = QtCore.pyqtSignal()

    closeSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(BaseForm, self).__init__()
        pass

    def __del__(self):
        pass

    def construct(self):
        pass

    @QtCore.pyqtSlot(list)
    def onInitWindowSignalReverted(self, list):
        pass

    @QtCore.pyqtSlot()
    def onComboUserChanged(self):
        pass

    @QtCore.pyqtSlot(list)
    def onChangeUserStateSignalReverted(self, list):
        pass

    @QtCore.pyqtSlot(list)
    def onMonitoringSignalReverted(self, list):
        pass

    @QtCore.pyqtSlot(list)
    def onAddUserSignalReverted(self, list):
        pass

    @QtCore.pyqtSlot(list)
    def onDeleteUserSignalReverted(self, list):
        pass

    @QtCore.pyqtSlot()
    def onClearLogSignalReverted(self):
        pass

    @QtCore.pyqtSlot(list)
    def onRefreshSignalReverted(self, list):
        pass

    def onButtonMonitoringClick(window):
        pass

    def onButtonAddUserClick(window):
        pass

    def onButtonDeleteUserClick(window):
        pass

    def onButtonClearLogClick(window):
        pass

    def displayMessage(self, list):
        try:
            message = self.messages[list[0]]
        except:
            message = ["Ошибка", "Неизвестная ошибка."]
        return QMessageBox.critical(self, message[0], message[1], QMessageBox.Ok)

    def askMessage(self, list):
        return QMessageBox.question(self, list[0], list[1], QMessageBox.Yes, QMessageBox.No)

# MainForm is view
class MainForm(BaseForm):
    txtEmptyLog = "Журнал пуст"
    txtEmptyShortcuts = "Сочетаний клавиш нет"
    txtEmptyCmbs = "Сочетаний букв нет"
    keyDelayZero = "0.0"
    keySearchZero = "0.0"
    keyNumberZero = "0.0"
    keyCmbsZero = "0"
    keyFuncsZero = "0"

    def __init__(self):
        super(MainForm, self).__init__()
        self.UI = uic.loadUi("static/MainForm.ui", self)
        self.setWindowIcon(QtGui.QIcon('static/icon.png'))

        self.construct()

    def __del__(self):
        pass

    def construct(self):
        self.buttonMonitoring.clicked.connect(lambda: self.onButtonMonitoringClick())
        self.buttonAdd.clicked.connect(lambda: self.onButtonAddUserClick())
        self.buttonDelete.clicked.connect(lambda: self.onButtonDeleteUserClick())
        self.buttonClear.clicked.connect(lambda: self.onButtonClearLogClick())

        self.buttonMonitoring.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(0, 255, 0, 255), stop:0.840909 rgba(0, 136, 0, 255));\n")

    def closeEvent(self, event):
        reply = self.askMessage(self.messages["EXIT"])

        if reply == QMessageBox.Yes:
            event.accept()
            self.closeSignal.emit()
        else:
            event.ignore()

    def showEvent(self, QShowEvent):
        self.initWindowSignal.emit()

    def refreshMethod(self, list):
        self.keyDelay.setText(str(list[0][0]))
        self.keySearch.setText(str(list[0][1]))
        self.keyNumber.setText(str(list[0][2]))
        self.keyCmbs.setText(str(list[0][3]))
        self.keyFuncs.setText(str(list[0][4]))

        if len(list[1]):
            txtLogging = ""
            for item in list[1]:
                txtLogging += str(item) + "\n"
            self.textLogging.setText(txtLogging)
        else:
            self.textLogging.setText(self.txtEmptyLog)


        txtShortcuts = ""
        if len(list[0][5]):
            for item in list[0][5]:
                txtShortcuts += str(item) + "\n"
            self.textShortcuts.setText(txtShortcuts)
        else:
            self.textShortcuts.setText(self.txtEmptyShortcuts)
        txtCmbs = ""
        if len(list[0][6]):
            for item in list[0][6]:
                txtCmbs += str(item) + "\n"
            self.textCmbs.setText(txtCmbs)
        else:
            self.textCmbs.setText(self.txtEmptyCmbs)

    @QtCore.pyqtSlot(list)
    def onInitWindowSignalReverted(self, list):
        for item in list[0]:
            for name in item:
                self.comboUser.addItem(name)

    @QtCore.pyqtSlot()
    def onComboUserChanged(self):
        self.changeUserStateSignal.emit([self.comboUser.currentText()])

    @QtCore.pyqtSlot(list)
    def onChangeUserStateSignalReverted(self, list):
        self.refreshMethod(list)

    @QtCore.pyqtSlot(list)
    def onMonitoringSignalReverted(self, list):
        if (list[0]):
            self.buttonMonitoring.setStyleSheet("background-color: rgb(255, 85, 0)")
            self.buttonMonitoring.setText("Выключить мониторинг действий")
            self.comboUser.setEnabled(False)
        else:
            self.buttonMonitoring.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.0568182, y1:0.126, x2:0.75, y2:0.227, stop:0.0738636 rgba(0, 255, 0, 255), stop:0.840909 rgba(0, 136, 0, 255));\n")
            self.buttonMonitoring.setText("Включить мониторинг действий")
            self.comboUser.setEnabled(True)

    @QtCore.pyqtSlot(list)
    def onAddUserSignalReverted(self, list):
        self.comboUser.addItem(list[0])

    @QtCore.pyqtSlot(list)
    def onDeleteUserSignalReverted(self, list):
        self.comboUser.removeItem(self.comboUser.findText(list[0]))

    @QtCore.pyqtSlot()
    def onClearLogSignalReverted(self):
        self.keyDelay.setText("0.0")
        self.keySearch.setText("0.0")
        self.keyNumber.setText("0.0")
        self.keyCmbs.setText("0")
        self.keyFuncs.setText("0")
        self.textLogging.setText(self.txtEmptyLog)
        self.textShortcuts.setText(self.txtEmptyShortcuts)
        self.textCmbs.setText(self.txtEmptyCmbs)

    @QtCore.pyqtSlot(list)
    def onRefreshSignalReverted(self, list):
        self.refreshMethod(list)

    def onButtonMonitoringClick(self):
        self.monitoringSignal.emit()

    def onButtonAddUserClick(self):
        name = self.editUserName.text().strip()
        self.addUserSignal.emit([name])

    def onButtonDeleteUserClick(self):
        name = self.editUserName.text().strip()
        self.deleteUserSignal.emit([name])

    def onButtonClearLogClick(self):
        self.clearLogSignal.emit()