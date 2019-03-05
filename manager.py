# Savital https://github.com/Savital
# manager.py Manager control

import sys
from subprocess import check_output
import threading

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication

from models.db import Users, Log
from models.parsers import ProcParser
from models.calcs import Calc
from models.timers import RefreshEventGenerator

from views.forms import MainForm

# Controller, handles signals between view and model
class Manager(QtCore.QObject):
    dbLock = threading.RLock()

    LKM = "monitorkbd"
    FILE_PATH = "monitorkbd/stat"
    PROC_PATH = "/proc/" + FILE_PATH

    doneInitSignal = QtCore.pyqtSignal(list)
    doneChangeUserStateSignal = QtCore.pyqtSignal(list)

    doneMonitoringSignal = QtCore.pyqtSignal(list)
    doneAddUserSignal = QtCore.pyqtSignal(list)
    doneDeleteUserSignal = QtCore.pyqtSignal(list)
    doneClearLogSignal = QtCore.pyqtSignal()

    refreshDataSignal = QtCore.pyqtSignal(list)
    errorSignal = QtCore.pyqtSignal(list)

    def __init__(self):
        super(Manager, self).__init__()
        self.construct()
        self.timer = RefreshEventGenerator(0.01, self.onRefreshEvent)
        self.timer.start()

    def __del__(self):
        self.timer.cancel()

    def construct(self):
        self.mUsers = Users()
        self.mLog = Log()
        self.mProcParser = ProcParser()
        self.mCalc = Calc()

        self.mUsers.createTable()
        self.mLog.createTable()

        self.monitoringFlag = False

    def connects(self):
        self.window.initWindowSignal.connect(self.initWindow)
        self.doneInitSignal.connect(self.window.onInitWindowSignalReverted)

        self.window.changeUserStateSignal.connect(self.changeUserState)
        self.doneChangeUserStateSignal.connect(self.window.onChangeUserStateSignalReverted)
        self.window.comboUser.currentTextChanged.connect(self.window.onComboUserChanged)

        self.window.monitoringSignal.connect(self.monitoring)
        self.window.addUserSignal.connect(self.addUser)
        self.window.deleteUserSignal.connect(self.deleteUser)
        self.window.clearLogSignal.connect(self.clearLog)

        self.doneMonitoringSignal.connect(self.window.onMonitoringSignalReverted)
        self.doneAddUserSignal.connect(self.window.onAddUserSignalReverted)
        self.doneDeleteUserSignal.connect(self.window.onDeleteUserSignalReverted)
        self.doneClearLogSignal.connect(self.window.onClearLogSignalReverted)

        self.window.closeSignal.connect(self.close)
        #Close when the thread terminated (TODO)

        self.refreshDataSignal.connect(self.window.onRefreshSignalReverted)
        self.errorSignal.connect(self.window.displayMessage)


    def runApp(self):
        self.app = QApplication(sys.argv)
        self.window = MainForm()
        self.connects()
        self.window.show()
        sys.exit(self.app.exec_())

    @QtCore.pyqtSlot()
    def initWindow(self):
        self.users = self.mUsers.select()
        self.user = ""
        if len(self.users):
            self.user = self.users[0][0]

        self.doneInitSignal.emit([self.users])

    def refreshData(self):
        self.log = self.mLog.selectByName(self.user)
        self.stats = self.mCalc.formStats(self.log)

    def onRefreshEvent(self):
        self.dbLock.acquire()
        try:
            list = self.mProcParser.read(self.PROC_PATH)
            if list:
                self.mLog.insert(self.user, list)

            self.refreshData()

            self.refreshDataSignal.emit([self.stats, self.log])
        finally:
            self.dbLock.release()

    @QtCore.pyqtSlot(list)
    def changeUserState(self, list):
        self.user = list[0]

        self.refreshData()

        self.doneChangeUserStateSignal.emit([self.stats, self.log])

    @QtCore.pyqtSlot()
    def monitoring(self):
        try:
            existLKM = check_output("lsmod | grep " + self.LKM, shell=True).decode()

            if len(self.mUsers.select()) == 0:
                self.errorSignal.emit(["USER_MISSING"])
                return

            self.monitoringFlag = not self.monitoringFlag
            if self.monitoringFlag:
                self.mProcParser.read(self.PROC_PATH)
                self.timer.runF()
            else:
                self.timer.stopF()

            self.doneMonitoringSignal.emit([self.monitoringFlag])

        except:
            self.errorSignal.emit(["LKM_MISSING"])

    @QtCore.pyqtSlot(list)
    def addUser(self, list):
        if list[0] == "":
            self.errorSignal.emit(["EMPTY_NAME"])
            return

        names = self.mUsers.selectByName(list[0])
        if names == None:
            self.mUsers.insert(list[0])
            self.doneAddUserSignal.emit([list[0]])
        else:
            self.errorSignal.emit(["ALREADY_EXIST"])

    @QtCore.pyqtSlot(list)
    def deleteUser(self, list):
        names = self.mUsers.selectByName(list[0])
        if names != None:
            self.mUsers.delete(list[0])
            self.doneDeleteUserSignal.emit([list[0]])
        else:
            self.errorSignal.emit(["DOESNT_EXIST"])

    @QtCore.pyqtSlot()
    def clearLog(self):
        self.dbLock.acquire()
        try:
            self.mLog.delete(self.user)
            self.doneClearLogSignal.emit()
        finally:
            self.dbLock.release()

    @QtCore.pyqtSlot()
    def close(self):
        self.timer.cancel()