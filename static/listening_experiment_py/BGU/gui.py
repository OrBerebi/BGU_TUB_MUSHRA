# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtSvg, QtGui
from ..GUI.utils import LabeledSlider, FooterTUB_THK_Chalmers


class gui(QtWidgets.QMainWindow):

    def __init__(self, num_stimuli_per_page=3, language='english', show_pm_btns=True):
        super().__init__()

    def setupUi(self, ui, num_stimuli_per_page, language='english' , show_pm_btns=True):
        """
        Listening Experiment Py: SAQI - A Spatial Audio Inventory

        (C) 2021 by Tim Lübeck
                TH Köln - University of Applied Sciences
                Institute of Communications Engineering
                Department of Acoustics and Audio Signal Processing

        Parameters
        ----------
        SAQI_main_gui
        categories
        language
        """
        ui.setObjectName("OLE")
        ui.resize(1024, 768)

        self.language = language
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
        top_layout = QtWidgets.QHBoxLayout()

        self.trial_cnt = QtWidgets.QLabel(self.centralwidget)
        self.trial_cnt.setGeometry(QtCore.QRect(900, 18, 80, 25))
        self.trial_cnt.setObjectName("trial count")
        self.trial_cnt.setWordWrap(True)

        self.task_label = QtWidgets.QLabel(self.centralwidget)
        self.task_label.setObjectName("task_label")
        self.task_label.setStyleSheet("color: white; font-size: 18pt")
        self.task_label.setWordWrap(True)
        top_layout.addWidget(self.task_label)

        main_layout.addLayout(top_layout, stretch=2)

        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.addItem(QtWidgets.QSpacerItem(
                              60, 40, QtWidgets.QSizePolicy.Minimum,
                              QtWidgets.QSizePolicy.Expanding))

        self.play_pause_btns = list()
        self.rating_sliders = list()
        self.slider_ticks = list()
        self.plus_btns = list()
        self.minus_btns = list()

        self.Ref_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Ref_btn.setFixedSize(100, 30)
        self.Ref_btn.setObjectName("Ref_btn")
        self.Ref_btn.setText('Reference (1)')

        self.Mute_all = QtWidgets.QPushButton(self.centralwidget)
        self.Mute_all.setFixedSize(100, 30)
        self.Mute_all.setObjectName("Mute_all")
        self.Mute_all.setText('(M)ute')

        """
        self.Calibrate = QtWidgets.QPushButton(self.centralwidget)
        self.Calibrate.setFixedSize(100, 30)
        self.Calibrate.setObjectName("Calibrate")
        self.Calibrate.setText('(C)alibrate')
        """
        vlayout = QtWidgets.QVBoxLayout()

        #vlayout.addWidget(self.current_playing_label)  # add it above Calibrate
        #vlayout.addWidget(self.Calibrate)
        vlayout.addWidget(self.Mute_all)
        vlayout.addWidget(self.Ref_btn)
        #vlayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        slider_layout.addLayout(vlayout)
        #main_layout.addLayout(slider_layout)


        for stimuli_idx in range(0, num_stimuli_per_page-1):
            vlayout = QtWidgets.QVBoxLayout()
            #vlayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
            
            # plus and minus buttons
            hlayout = QtWidgets.QHBoxLayout()


            self.plus_btns.append(QtWidgets.QPushButton(self.centralwidget))
            self.plus_btns[stimuli_idx].setVisible(False)
            self.plus_btns[stimuli_idx].setFixedHeight(17)
            self.plus_btns[stimuli_idx].setMaximumWidth(17)
            self.plus_btns[stimuli_idx].setText('+')

            self.minus_btns.append(QtWidgets.QPushButton(self.centralwidget))
            self.minus_btns[stimuli_idx].setVisible(False)
            self.minus_btns[stimuli_idx].setFixedHeight(17)
            self.minus_btns[stimuli_idx].setMaximumWidth(17)
            self.minus_btns[stimuli_idx].setText('-')

            hlayout.addWidget(self.plus_btns[stimuli_idx])
            hlayout.addWidget(self.minus_btns[stimuli_idx])

            self.rating_sliders.append(LabeledSlider(
                                       0, 100, steps_per_interval=1, interval=25,
                                       orientation=QtCore.Qt.Vertical,
                                       labels=('None       (0)',
                                               '           (25)',
                                               '           (50)',
                                               '           (75)',
                                               'Very Large (100)')))
            self.rating_sliders[stimuli_idx].setVisible(False)

            self.play_pause_btns.append(QtWidgets.QPushButton(self.centralwidget))
            self.play_pause_btns[stimuli_idx].setObjectName("play_pause_btn")
            self.play_pause_btns[stimuli_idx].setVisible(False)
            self.play_pause_btns[stimuli_idx].setFixedHeight(30)
            self.play_pause_btns[stimuli_idx].setMaximumWidth(110)
            #self.play_pause_btns[stimuli_idx].setText(chr(ord('@')+stimuli_idx+1))
            self.play_pause_btns[stimuli_idx].setText(f"{chr(ord('@') + stimuli_idx + 1)} ({stimuli_idx + 2})")
            vlayout.addWidget(self.rating_sliders[stimuli_idx])
            vlayout.addLayout(hlayout)
            vlayout.addWidget(self.play_pause_btns[stimuli_idx])
            slider_layout.addLayout(vlayout)
            #slider_layout.addItem(QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))




        vlayout = QtWidgets.QVBoxLayout()
        vlayout.addItem(QtWidgets.QSpacerItem(40, 250,
                                              QtWidgets.QSizePolicy.Minimum,
                                              QtWidgets.QSizePolicy.Expanding))
        self.next_trial_btn = QtWidgets.QPushButton(self.centralwidget)
        self.next_trial_btn.setFixedSize(100, 30)
        self.next_trial_btn.setObjectName("next_trial_btn")
        self.next_trial_btn.setText('next')
        vlayout.addWidget(self.next_trial_btn)
        slider_layout.addLayout(vlayout)
        main_layout.addLayout(slider_layout)

        

        main_layout.addLayout(FooterTUB_THK_Chalmers(experiment_name='MUSHRA Listening Experiment'))

        ui.setCentralWidget(self.centralwidget)
        self.retranslateUi(ui)
        QtCore.QMetaObject.connectSlotsByName(ui)

    def retranslateUi(self, ui):
        _translate = QtCore.QCoreApplication.translate
        ui.setWindowTitle(_translate("OLE_gui",
                                     "MUSHRA Listening Experiment"))

    def print_task(self,attribute, finish=False):
        style = "background-color: #FFD700; color: black; font-size: 24pt; font-weight: bold;"
        if not finish:
            if self.language == 'english':
                #self.task_label.setText("Rate the difference between each signal and the reference in terms of " + attribute)
                self.task_label.setText(
                    f"Rate the difference between each signal and the reference in terms of "
                    f"<span style='{style}'>&nbsp;{attribute}&nbsp;</span>"
                )
            elif self.language == 'german':
                self.task_label.setText('How much do you enjoy listening to '
                                        'the following music items?')
        else:
            if self.language == 'english':
                self.task_label.setText('First part of the experiment '
                                        'completed, continue by clicking the '
                                        'next button.')
            elif self.language == 'german':
                self.task_label.setText('First part of the experiment '
                                        'completed, continue by clicking the '
                                        'next button.')