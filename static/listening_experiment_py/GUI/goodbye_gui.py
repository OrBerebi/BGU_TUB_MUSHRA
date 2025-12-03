from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from .. GUI.utils import Footer


class goodbye_gui(object):
    def setupUi(self, ui, language='english', footer=None):
        if footer is None:
            footer = Footer(experiment_name="")

        ui.setObjectName("goodbye_gui")
        
        # --- FIX 1: Comment out or remove this line ---
        # ui.resize(1024, 768) 
        # ----------------------------------------------

        self.centralwidget = QtWidgets.QWidget(ui)
        self.centralwidget.setObjectName("centralwidget")

        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                 QtWidgets.QSizePolicy.Fixed)
        self.frame.setLineWidth(10)
        self.frame.setObjectName("frame")
        self.frame.raise_()

        self.task_label = QtWidgets.QLabel(self.centralwidget)
        self.task_label.setObjectName("task_label")
        self.task_label.setStyleSheet("color: white; font-size: 18pt")
        self.finish_btn = QtWidgets.QPushButton(self.centralwidget)
        self.finish_btn.setFixedSize(100, 30)
        self.finish_btn.setObjectName("start_btn")

        main_layout.addWidget(self.frame)
        
        # --- FIX 2: Add spacers to center content vertically ---
        main_layout.addStretch() 
        main_layout.addWidget(self.task_label, alignment=QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.finish_btn, alignment=QtCore.Qt.AlignCenter)
        main_layout.addStretch()
        # -------------------------------------------------------

        # add footer
        main_layout.addLayout(footer)

        ui.setCentralWidget(self.centralwidget)
        self.retranslateUi(ui, language)
        QtCore.QMetaObject.connectSlotsByName(ui)

    def retranslateUi(self, ui, language):
        _translate = QtCore.QCoreApplication.translate
        ui.setWindowTitle(_translate("goodbye_gui", "Goodby"))

        if language == 'english':
            self.task_label.setText(_translate("SAQUI_goodbye_gui", "<html><head/><body><p align=\"justify\">Thank you for participating. Please close the app.</p></body></html>"))
            self.finish_btn.setText(_translate("SAQUI_goodbye_gui", "finish"))
        elif language == 'german':
            self.task_label.setText(_translate("SAQUI_goodbye_gui",
                                               "<html><head/><body><p align=\"justify\">Danke für die Teilnahme. Bitte schließe die App.</p></body></html>"))
            self.finish_btn.setText(_translate("SAQUI_goodbye_gui", "ende"))