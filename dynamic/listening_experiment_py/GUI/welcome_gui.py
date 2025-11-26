# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from .. GUI.utils import Footer

class Welcome_gui(object):
    def setupUi(self, ui, experiment_name, language='english', footer=None):
        """
        Modified Welcome GUI based on 'AK_Soziodemographie_englisch.pdf'
        """
        if footer is None:
            footer = Footer(experiment_name=experiment_name)

        ui.setObjectName(experiment_name)
        ui.resize(1024, 768)

        self.centralwidget = QtWidgets.QWidget(ui)
        self.centralwidget.setObjectName("centralwidget")

        # --- Main Layout ---
        # We use a main layout for the central widget
        main_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Header Separator
        Separador = QtWidgets.QFrame()
        Separador.setFrameShape(QtWidgets.QFrame.HLine)
        Separador.setLineWidth(10)
        main_layout.addWidget(Separador)

        # Title / Task Label
        self.task_label = QtWidgets.QLabel(self.centralwidget)
        self.task_label.setStyleSheet(f"color: white; font-size: 18pt")
        self.task_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(self.task_label)

        Separador2 = QtWidgets.QFrame()
        Separador2.setFrameShape(QtWidgets.QFrame.HLine)
        Separador2.setLineWidth(10)
        main_layout.addWidget(Separador2)

        # --- SCROLL AREA SETUP ---
        # Because the new PDF has many questions, we need a scroll area
        self.scroll_area = QtWidgets.QScrollArea(self.centralwidget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        self.scroll_content = QtWidgets.QWidget()
        self.form_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.form_layout.setSpacing(20) # Add space between questions

        # =========================================================
        # SECTION 1: General Information [cite: 4]
        # =========================================================

        # 1.0 Subject ID Code
        self.subject_code_label = QtWidgets.QLabel()
        self.subject_code_edit = QtWidgets.QLineEdit()
        self.subject_code_edit.setMaximumWidth(120)
        self.add_row(self.subject_code_label, self.subject_code_edit)
        
        # 1.1 Gender [cite: 5]
        self.gender_label = QtWidgets.QLabel()
        self.gender_combobox = QtWidgets.QComboBox()
        self.add_row(self.gender_label, self.gender_combobox)

        # 1.2 Year Born [cite: 10]
        self.year_born_label = QtWidgets.QLabel()
        self.year_born_edit = QtWidgets.QLineEdit()
        self.year_born_edit.setMaximumWidth(120)
        self.add_row(self.year_born_label, self.year_born_edit)

        # 1.3 Native Language [cite: 11]
        self.language_label = QtWidgets.QLabel()
        self.language_combobox = QtWidgets.QComboBox()
        self.add_row(self.language_label, self.language_combobox)

        # 1.4 German Proficiency [cite: 16]
        self.german_level_label = QtWidgets.QLabel()
        self.german_level_combobox = QtWidgets.QComboBox()
        self.add_row(self.german_level_label, self.german_level_combobox)

        # 1.5 Education [cite: 31]
        self.education_label = QtWidgets.QLabel()
        self.education_combobox = QtWidgets.QComboBox()
        self.add_row(self.education_label, self.education_combobox)

        # 1.6 Hearing Impairment [cite: 35]
        self.hearing_label = QtWidgets.QLabel()
        self.hearing_combobox = QtWidgets.QComboBox()
        self.add_row(self.hearing_label, self.hearing_combobox)

        # Divider
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        self.form_layout.addWidget(line)

        # =========================================================
        # SECTION 2: Acoustic and Musical Experience [cite: 44]
        # =========================================================

        # 2.1 Acoustics Profession [cite: 45]
        self.acoustics_prof_label = QtWidgets.QLabel()
        self.acoustics_prof_combobox = QtWidgets.QComboBox()
        self.add_row(self.acoustics_prof_label, self.acoustics_prof_combobox)

        # 2.2 Acoustics Years [cite: 49]
        self.acoustics_years_label = QtWidgets.QLabel()
        self.acoustics_years_edit = QtWidgets.QLineEdit()
        self.acoustics_years_edit.setMaximumWidth(120)
        self.add_row(self.acoustics_years_label, self.acoustics_years_edit)

        # 2.3 Music Profession [cite: 51]
        self.music_prof_label = QtWidgets.QLabel()
        self.music_prof_combobox = QtWidgets.QComboBox()
        self.add_row(self.music_prof_label, self.music_prof_combobox)

        # 2.4 Music Years [cite: 55]
        self.music_years_label = QtWidgets.QLabel()
        self.music_years_edit = QtWidgets.QLineEdit()
        self.music_years_edit.setMaximumWidth(120)
        self.add_row(self.music_years_label, self.music_years_edit)

        # 2.5 Instrument/Vocals [cite: 57]
        self.instrument_label = QtWidgets.QLabel()
        self.instrument_combobox = QtWidgets.QComboBox()
        self.add_row(self.instrument_label, self.instrument_combobox)

        # 2.6 Instrument Years [cite: 61]
        self.instrument_years_label = QtWidgets.QLabel()
        self.instrument_years_edit = QtWidgets.QLineEdit()
        self.instrument_years_edit.setMaximumWidth(120)
        self.add_row(self.instrument_years_label, self.instrument_years_edit)

        # Divider
        line2 = QtWidgets.QFrame()
        line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.form_layout.addWidget(line2)

        # =========================================================
        # SECTION 3: Studies and Listening Habits [cite: 63]
        # =========================================================

        # 3.1 Prior Experiment Participation [cite: 64]
        self.prior_exp_label = QtWidgets.QLabel()
        self.prior_exp_combobox = QtWidgets.QComboBox()
        self.add_row(self.prior_exp_label, self.prior_exp_combobox)

        # 3.2 How many studies [cite: 68]
        self.num_studies_label = QtWidgets.QLabel()
        self.num_studies_edit = QtWidgets.QLineEdit()
        self.num_studies_edit.setMaximumWidth(120)
        self.add_row(self.num_studies_label, self.num_studies_edit)

        # 3.3 Daily listening hours [cite: 71]
        self.listening_hours_label = QtWidgets.QLabel()
        self.listening_hours_edit = QtWidgets.QLineEdit()
        self.listening_hours_edit.setMaximumWidth(120)
        self.add_row(self.listening_hours_label, self.listening_hours_edit)

        # Divider
        line3 = QtWidgets.QFrame()
        line3.setFrameShape(QtWidgets.QFrame.HLine)
        self.form_layout.addWidget(line3)

        # =========================================================
        # SECTION 4: Student Info [cite: 74]
        # =========================================================
        
        # Matriculation Number [cite: 77]
        self.matriculation_label = QtWidgets.QLabel()
        self.matriculation_edit = QtWidgets.QLineEdit()
        self.matriculation_edit.setMaximumWidth(200)
        self.add_row(self.matriculation_label, self.matriculation_edit)

        # Add scroll content to scroll area
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # --- Footer Area (Start Button) ---
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setFixedSize(QtCore.QSize(150, 40))
        self.start_btn.setObjectName("start_btn")
        button_layout.addWidget(self.start_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        main_layout.addLayout(footer)

        ui.setCentralWidget(self.centralwidget)
        self.retranslateUi(ui, language)
        QtCore.QMetaObject.connectSlotsByName(ui)

    def add_row(self, label, widget):
        """Helper to add a label/widget row to the form layout"""
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.setContentsMargins(20, 0, 20, 0)
        
        label.setWordWrap(True)
        # label.setMinimumWidth(400)
        
        hlayout.addWidget(label, 3) # Label takes 3 parts space
        hlayout.addWidget(widget, 1) # Widget takes 1 part space
        self.form_layout.addLayout(hlayout)

    def retranslateUi(self, ui, language):
        _translate = QtCore.QCoreApplication.translate
        ui.setWindowTitle(_translate("welcome_gui", "Welcome"))
        
        # Intro Text [cite: 1]
        self.task_label.setText(_translate("SAQI_welcome_gui",
            "<html><head/><body><p align=\"center\"><b>Socio-demographic questionnaire</b></p>"
            "<p align=\"center\">Please fill out the questionnaire. Tick or fill in the appropriate information.</p></body></html>"))

        if language == 'english':
            self.start_btn.setText(_translate("SAQI_welcome_gui", "Start"))
            
            self.subject_code_label.setText(_translate("SAQI_welcome_gui", 
                "1.0 Personal Code:\n"
                "First letter of your first name + First letter of mother's first name + "
                "First letter of father's first name + last digit of your birth year.\n"
                "(e.g., OMG3 for Oscar, Maggy, Gerald, 2003)"))
            self.subject_code_edit.setPlaceholderText("e.g. OMG3")

            # 1.1 Gender [cite: 9]
            self.gender_label.setText(_translate("SAQI_welcome_gui", "1.1 What gender do you identify with most?"))
            self.gender_combobox.clear()
            self.gender_combobox.addItems(["Female", "Male", "Diverse"])
            
            # 1.2 Year Born [cite: 10]
            self.year_born_label.setText(_translate("SAQI_welcome_gui", "1.2 What year were you born?"))
            self.year_born_edit.setPlaceholderText("YYYY")

            # 1.3 Native Language [cite: 11]
            self.language_label.setText(_translate("SAQI_welcome_gui", "1.3 What is your native language?"))
            self.language_combobox.clear()
            self.language_combobox.addItems(["English", "German", "Hebrew", "French", "Spanish", "Other"])

            # 1.4 German Proficiency [cite: 16]
            self.german_level_label.setText(_translate("SAQI_welcome_gui", "1.4 Please rate your current level of proficiency in the English language:"))
            self.german_level_combobox.clear()
            self.german_level_combobox.addItems([
                "Native speaker",
                "A1 - Breakthrough Basic User",
                "A2 - Waystage Basic User",
                "B1 - Threshold Independent User",
                "B2 - Vantage Independent User",
                "C1 - Advanced Proficient User",
                "C2 - Mastery Proficient User",
                "Other"
            ])

            # 1.5 Education [cite: 31]
            self.education_label.setText(_translate("SAQI_welcome_gui", "1.5 What is your highest educational qualification?"))
            self.education_combobox.clear()
            self.education_combobox.addItems(["Secondary Education or less", "Graduate or higher academic degree"])

            # 1.6 Hearing [cite: 35]
            self.hearing_label.setText(_translate("SAQI_welcome_gui", "1.6 Do you have a medically diagnosed hearing impairment?"))
            self.hearing_combobox.clear()
            self.hearing_combobox.addItems([
                "No", 
                "Yes, pertains to the right ear", 
                "Yes, pertains to the left ear", 
                "Yes, pertains to both ears"
            ])

            # 2.1 Acoustics Profession [cite: 45]
            self.acoustics_prof_label.setText(_translate("SAQI_welcome_gui", "2.1 Do you have an acoustics-related profession or training?"))
            self.acoustics_prof_combobox.clear()
            self.acoustics_prof_combobox.addItems(["No", "Yes"])

            # 2.2 Acoustics Years [cite: 49]
            self.acoustics_years_label.setText(_translate("SAQI_welcome_gui", "2.2 Experience in years (approximate):"))
            
            # 2.3 Music Profession [cite: 51]
            self.music_prof_label.setText(_translate("SAQI_welcome_gui", "2.3 Do you have a music-related profession or training?"))
            self.music_prof_combobox.clear()
            self.music_prof_combobox.addItems(["No", "Yes"])

            # 2.4 Music Years [cite: 55]
            self.music_years_label.setText(_translate("SAQI_welcome_gui", "2.4 Experience in years (approximate):"))

            # 2.5 Instrument [cite: 57]
            self.instrument_label.setText(_translate("SAQI_welcome_gui", "2.5 Have you learned at least one instrument/vocals under guidance?"))
            self.instrument_combobox.clear()
            self.instrument_combobox.addItems(["No", "Yes"])

            # 2.6 Instrument Years [cite: 61]
            self.instrument_years_label.setText(_translate("SAQI_welcome_gui", "2.6 Experience in years (approximate):"))

            # 3.1 Prior Experiment [cite: 64]
            self.prior_exp_label.setText(_translate("SAQI_welcome_gui", "3.1 Have you ever participated in a scientific hearing experiment before?"))
            self.prior_exp_combobox.clear()
            self.prior_exp_combobox.addItems(["No", "Yes"])

            # 3.2 Num Studies [cite: 68]
            self.num_studies_label.setText(_translate("SAQI_welcome_gui", "3.2 How many such studies have you participated in?"))

            # 3.3 Listening Hours [cite: 71]
            self.listening_hours_label.setText(_translate("SAQI_welcome_gui", "3.3 Active listening hours per day (0-24):"))

            # 4. Matriculation [cite: 75]
            self.matriculation_label.setText(_translate("SAQI_welcome_gui", "4. (TU Berlin Students) Matriculation number:"))
            self.matriculation_edit.setPlaceholderText("Optional")