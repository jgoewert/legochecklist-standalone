# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QScrollArea, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1760, 1035)
        self.actionWanted = QAction(MainWindow)
        self.actionWanted.setObjectName(u"actionWanted")
        self.actionHave = QAction(MainWindow)
        self.actionHave.setObjectName(u"actionHave")
        self.actionBoth = QAction(MainWindow)
        self.actionBoth.setObjectName(u"actionBoth")
        self.actionPrint = QAction(MainWindow)
        self.actionPrint.setObjectName(u"actionPrint")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.rebrickableKeyLabel = QLabel(self.centralwidget)
        self.rebrickableKeyLabel.setObjectName(u"rebrickableKeyLabel")

        self.gridLayout.addWidget(self.rebrickableKeyLabel, 0, 0, 1, 1)

        self.setLabel = QLabel(self.centralwidget)
        self.setLabel.setObjectName(u"setLabel")
        self.setLabel.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.setLabel, 1, 0, 1, 1)

        self.statusLabel = QLabel(self.centralwidget)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setMaximumSize(QSize(16777215, 20))
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.statusLabel, 2, 0, 1, 2)

        self.partsScrollArea = QScrollArea(self.centralwidget)
        self.partsScrollArea.setObjectName(u"partsScrollArea")
        self.partsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.partsScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.partsScrollArea.setWidgetResizable(True)
        self.partsWidget = QWidget()
        self.partsWidget.setObjectName(u"partsWidget")
        self.partsWidget.setGeometry(QRect(0, 0, 1721, 901))
        self.partsScrollArea.setWidget(self.partsWidget)

        self.gridLayout.addWidget(self.partsScrollArea, 3, 0, 1, 2)

        self.rebrickableKeyText = QLineEdit(self.centralwidget)
        self.rebrickableKeyText.setObjectName(u"rebrickableKeyText")

        self.gridLayout.addWidget(self.rebrickableKeyText, 0, 1, 1, 1)

        self.setText = QLineEdit(self.centralwidget)
        self.setText.setObjectName(u"setText")
        self.setText.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.setText, 1, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1760, 21))
        self.menuNeed = QMenu(self.menubar)
        self.menuNeed.setObjectName(u"menuNeed")
        self.menuHave = QMenu(self.menubar)
        self.menuHave.setObjectName(u"menuHave")
        self.menuSettings = QMenu(self.menubar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuNeed.menuAction())
        self.menubar.addAction(self.menuHave.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menuNeed.addAction(self.actionPrint)
        self.menuNeed.addAction(self.actionSave)
        self.menuNeed.addAction(self.actionExport)
        self.menuHave.addAction(self.actionWanted)
        self.menuHave.addAction(self.actionHave)
        self.menuHave.addAction(self.actionBoth)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Lego Checklist", None))
        self.actionWanted.setText(QCoreApplication.translate("MainWindow", u"Wanted", None))
        self.actionHave.setText(QCoreApplication.translate("MainWindow", u"Have", None))
        self.actionBoth.setText(QCoreApplication.translate("MainWindow", u"Both", None))
        self.actionPrint.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.rebrickableKeyLabel.setText(QCoreApplication.translate("MainWindow", u"Rebrickable API Key:", None))
        self.setLabel.setText(QCoreApplication.translate("MainWindow", u"Set ID:", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.menuNeed.setTitle(QCoreApplication.translate("MainWindow", u"Actions", None))
        self.menuHave.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

