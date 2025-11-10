# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtSvg
from .. GUI.utils import Footer


class Welcome_gui(object):
    def setupUi(self, ui, experiment_name, language='english', footer=None):
        """
        Listening Experiment Py: SAQI - A Spatial Audio Inventory

        (C) 2021 by Tim Lübeck
                TH Köln - University of Applied Sciences
                Institute of Communications Engineering
                Department of Acoustics and Audio Signal Processing

        Parameters
        ----------
        SAQI_welcome_gui
        language
        """
        if footer is None:
            footer = Footer(experiment_name=experiment_name)

        ui.setObjectName(experiment_name)
        ui.resize(1024, 768)  # IPad 1.gen display dimensions 1024 x 768

        self.centralwidget = QtWidgets.QWidget(ui)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        Separador = QtWidgets.QFrame()
        Separador.setFrameShape(QtWidgets.QFrame.HLine)
        Separador.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Fixed)
        Separador.setLineWidth(10)
        main_layout.addWidget(Separador)

        # draw Top layout
        top_layout = QtWidgets.QVBoxLayout()
        top_layout.addItem(QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))

        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.task_label = QtWidgets.QLabel(self.centralwidget)
        self.task_label.setGeometry(QtCore.QRect(50, 80, 521, 91))
        self.task_label.setObjectName("task_label")
        self.task_label.setStyleSheet(f"color: white; font-size: 18pt")
        hlayout.addWidget(self.task_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 30, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)
        Separador = QtWidgets.QFrame()
        Separador.setFrameShape(QtWidgets.QFrame.HLine)
        Separador.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Fixed)
        Separador.setLineWidth(10)
        top_layout.addWidget(Separador)
        
        # age 
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.age_label = QtWidgets.QLabel(self.centralwidget)
        self.age_label.setGeometry(QtCore.QRect(70, 270, 75, 16))
        self.age_label.setObjectName("age_label")
        self.age_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.age_combobox.setMaximumWidth(120)
        self.age_combobox.setObjectName("age_combobox")
        hlayout.addWidget(self.age_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        hlayout.addWidget(self.age_combobox)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)
        
        # gender
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.gender_label = QtWidgets.QLabel(self.centralwidget)
        self.gender_label.setGeometry(QtCore.QRect(70, 230, 75, 16))
        self.gender_label.setObjectName("gender_label")
        self.gender_combobox = QtWidgets.QComboBox(self.centralwidget)
        self.gender_combobox.setMaximumWidth(120)
        self.gender_combobox.setObjectName("gender_combobox")
        self.gender_combobox.addItem("")
        self.gender_combobox.addItem("")
        self.gender_combobox.addItem("")
        hlayout.addWidget(self.gender_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        hlayout.addWidget(self.gender_combobox)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)

        # general experience
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.general_exp_label = QtWidgets.QLabel()
        self.general_exp_label.setGeometry(QtCore.QRect(20, 100, 341, 51))
        self.general_exp_label.setObjectName("LE_exp_label")
        self.general_exp_combobox = QtWidgets.QComboBox()
        self.general_exp_combobox.setMaximumWidth(120)
        self.general_exp_combobox.setObjectName("LE_exp_combobox")
        self.general_exp_combobox.addItem("")
        self.general_exp_combobox.addItem("")
        self.general_exp_combobox.addItem("")
        self.general_exp_combobox.addItem("")
        hlayout.addWidget(self.general_exp_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        hlayout.addWidget(self.general_exp_combobox)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)

        # binaural experience
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.binaural_exp_label = QtWidgets.QLabel()
        self.binaural_exp_label.setGeometry(QtCore.QRect(20, 185, 341, 21))
        self.binaural_exp_label.setObjectName("BinTech_exp_label")
        self.binaural_exp_combobox = QtWidgets.QComboBox()
        self.binaural_exp_combobox.setMaximumWidth(120)
        self.binaural_exp_combobox.setObjectName("BinTech_exp_combobox")
        self.binaural_exp_combobox.addItem("")
        self.binaural_exp_combobox.addItem("")
        hlayout.addWidget(self.binaural_exp_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        hlayout.addWidget(self.binaural_exp_combobox)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)

        # health status
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.health_status_label = QtWidgets.QLabel()
        self.health_status_label.setGeometry(QtCore.QRect(20, 485, 541, 21))
        self.health_status_label.setObjectName("health_status_label")
        self.health_status_combobox = QtWidgets.QComboBox()
        self.health_status_combobox.setMinimumWidth(120)
        self.health_status_combobox.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                                  QtWidgets.QSizePolicy.Fixed)
        self.health_status_combobox.setFixedSize(220, 20)
        self.health_status_combobox.setFixedWidth(200)
        self.health_status_combobox.setObjectName("health_status_combo")
        self.health_status_combobox.addItem("")
        self.health_status_combobox.addItem("")
        self.health_status_combobox.addItem("")
        self.health_status_combobox.addItem("")
        self.health_status_combobox.addItem("")
        self.health_status_combobox.addItem("")
        hlayout.addWidget(self.health_status_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        hlayout.addWidget(self.health_status_combobox)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)

        # hearing problems
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        self.hearing_problems_label = QtWidgets.QLabel()
        self.hearing_problems_label.setGeometry(QtCore.QRect(20, 185, 341, 21))
        self.hearing_problems_label.setObjectName("hearing_problems_label")
        self.hearing_problems_combobox = QtWidgets.QComboBox()
        self.hearing_problems_combobox.setMaximumWidth(120)
        self.hearing_problems_combobox.setObjectName("hearing_problems_combo")
        self.hearing_problems_combobox.addItem("")
        self.hearing_problems_combobox.addItem("")
        self.hearing_problems_combobox.addItem("")
        self.hearing_problems_combobox.addItem("")
        hlayout.addWidget(self.hearing_problems_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Fixed))
        hlayout.addWidget(self.hearing_problems_combobox)
        hlayout.addItem(QtWidgets.QSpacerItem(
            50, 10, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))
        top_layout.addLayout(hlayout)
        
        top_layout.addItem(QtWidgets.QSpacerItem(
            120, 60, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed))

        hlayout = QtWidgets.QHBoxLayout()
        self.calibrate_btn = QtWidgets.QPushButton(self.centralwidget)
        self.calibrate_btn.setFixedSize(QtCore.QSize(110, 30))
        self.calibrate_btn.setObjectName("calibrate_btn")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setFixedSize(QtCore.QSize(110, 30))
        self.start_btn.setObjectName("start_btn")
        hlayout.addWidget(self.calibrate_btn)
        hlayout.addWidget(self.start_btn)
        top_layout.addLayout(hlayout)

        self.task_label.raise_()
        self.start_btn.raise_()
        self.age_combobox.raise_()
        self.age_label.raise_()
        self.gender_label.raise_()
        self.gender_combobox.raise_()
        self.calibrate_btn.raise_()

        main_layout.addLayout(top_layout)
        # add footer
        main_layout.addLayout(footer)

        ui.setCentralWidget(self.centralwidget)
        self.retranslateUi(ui, language)
        QtCore.QMetaObject.connectSlotsByName(ui)

    def retranslateUi(self, ui, language):
        _translate = QtCore.QCoreApplication.translate
        ui.setWindowTitle(_translate("welcome_gui", "Welcome"))
        self.task_label.setText(_translate("SAQI_welcome_gui",
                                           "<html><head/><body><p align=\"justify\">Welcome to our Listening Experiment. </p><p align=\"justify\">Please provide us some information about yourselfe and click start </p><p align=\"justify\">to start the experiment.</p></body></html>"))
        if language == 'english':
            self.start_btn.setText(_translate("SAQI_welcome_gui", "start"))
            self.age_label.setText(_translate("SAQI_welcome_gui", "age"))
            self.gender_label.setText(_translate("SAQI_welcome_gui", "gender"))
            self.gender_combobox.setItemText(0, _translate("SAQI_welcome_gui", "female"))
            self.gender_combobox.setItemText(1, _translate("SAQI_welcome_gui", "male"))
            self.gender_combobox.setItemText(2, _translate("SAQI_welcome_gui", "divers / non-binary"))
            for age in range(1, 99):
                self.age_combobox.addItem(f"{age}")
            self.general_exp_combobox.setItemText(0, _translate("SAQI_welcome_gui", "no"))
            self.general_exp_combobox.setItemText(1, _translate("SAQI_welcome_gui", "<3"))
            self.general_exp_combobox.setItemText(2, _translate("SAQI_welcome_gui", "3-5"))
            self.general_exp_combobox.setItemText(3, _translate("SAQI_welcome_gui", ">5"))
            self.general_exp_combobox.adjustSize()
            self.binaural_exp_label.setText(
                _translate("SAQI_welcome_gui", "Do you have experince with binaural technology?"))
            self.binaural_exp_combobox.setItemText(0, _translate("SAQI_welcome_gui", "yes"))
            self.binaural_exp_combobox.setItemText(1, _translate("SAQI_welcome_gui", "no"))
            self.binaural_exp_combobox.adjustSize()
            self.general_exp_label.setText(_translate("SAQI_welcome_gui",
                                                 "<html><head/><body><p>Did you already participated in a listening experiments </p><p>and if in how many?</p></body></html>"))
            self.health_status_label.setText(_translate("SAQI_welcome_gui", "How do you feel today?"))
            self.health_status_combobox.setItemText(0, _translate("SAQI_welcome_gui", "excellent"))
            self.health_status_combobox.setItemText(1, _translate("SAQI_welcome_gui", "very well"))
            self.health_status_combobox.setItemText(2, _translate("SAQI_welcome_gui", "well"))
            self.health_status_combobox.setItemText(3, _translate("SAQI_welcome_gui", "less well"))
            self.health_status_combobox.setItemText(4, _translate("SAQI_welcome_gui", "bad"))
            #self.health_status_label.adjustSize()
            self.hearing_problems_label.setText(_translate("SAQI_welcome_gui", "Do you have any hearing problems on one or both ears?"))
            self.hearing_problems_combobox.setItemText(0, _translate("SAQI_welcome_gui", "no"))
            self.hearing_problems_combobox.setItemText(1, _translate("SAQI_welcome_gui", "both"))
            self.hearing_problems_combobox.setItemText(2, _translate("SAQI_welcome_gui", "left"))
            self.hearing_problems_combobox.setItemText(3, _translate("SAQI_welcome_gui", "right"))
            self.hearing_problems_combobox.adjustSize()
            self.calibrate_btn.setText(_translate("SAQI_welcome_gui", "calibrate"))

        elif language == 'german':
            self.start_btn.setText(_translate("SAQI_welcome_gui", "Start"))
            self.age_label.setText(_translate("SAQI_welcome_gui", "Alter"))
            self.gender_label.setText(_translate("SAQI_welcome_gui", "Geschlecht"))
            self.gender_combobox.setItemText(0, _translate("SAQI_welcome_gui", "weiblich"))
            self.gender_combobox.setItemText(1, _translate("SAQI_welcome_gui", "männlich"))
            self.gender_combobox.setItemText(1, _translate("SAQI_welcome_gui", "divers / non-binary"))
            for age in range(1, 99):
                self.age_combobox.addItem(f"{age}")
            self.general_exp_combobox.setItemText(0, _translate("SAQI_welcome_gui", "Nein"))
            self.general_exp_combobox.setItemText(1, _translate("SAQI_welcome_gui", "<3"))
            self.general_exp_combobox.setItemText(2, _translate("SAQI_welcome_gui", "3-5"))
            self.general_exp_combobox.setItemText(3, _translate("SAQI_welcome_gui", ">5"))
            self.health_status_label.setText(_translate("SAQI_welcome_gui", "Wie fühlst du dich heute?"))
            self.health_status_combobox.setItemText(0, _translate("SAQI_welcome_gui", "ausgezeichnet"))
            self.health_status_combobox.setItemText(1, _translate("SAQI_welcome_gui", "sehr gut"))
            self.health_status_combobox.setItemText(2, _translate("SAQI_welcome_gui", "gut"))
            self.health_status_combobox.setItemText(3, _translate("SAQI_welcome_gui", "weniger gut"))
            self.health_status_combobox.setItemText(4, _translate("SAQI_welcome_gui", "schlecht"))
            self.hearing_problems_label.setText(_translate("SAQI_welcome_gui", "Haben Sie in einem oder in beiden Ohren Hörschwierigkeiten?"))
            self.hearing_problems_combobox.setItemText(0, _translate("SAQI_welcome_gui", "nein"))
            self.hearing_problems_combobox.setItemText(1, _translate("SAQI_welcome_gui", "beiden"))
            self.hearing_problems_combobox.setItemText(2, _translate("SAQI_welcome_gui", "links"))
            self.hearing_problems_combobox.setItemText(3, _translate("SAQI_welcome_gui", "rechts"))
            self.binaural_exp_label.setText(
                _translate("SAQI_welcome_gui", "Haben Sie Erfahrung mit Binaural Synthese?"))
            self.binaural_exp_combobox.setItemText(0, _translate("SAQI_welcome_gui", "Ja"))
            self.binaural_exp_combobox.setItemText(1, _translate("SAQI_welcome_gui", "Nein"))
            self.general_exp_label.setText(_translate("SAQI_welcome_gui",
                                                 "<html><head/><body><p>Haben Sie bereits an einem Hörversuch teilgenommen </p><p>und wenn ja an wie vielen?</p></body></html>"))
            self.calibrate_btn.setText(_translate("SAQI_welcome_gui", "Kalibrieren"))

