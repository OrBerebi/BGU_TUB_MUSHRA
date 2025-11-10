from PyQt5 import QtCore, QtWidgets
import numpy as np
from .. GUI.welcome_gui import Welcome_gui
from .. GUI.goodbye_gui import goodbye_gui


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, ssr_handler, experiment_handler, jack_handler=None,
                 language='english', monitor_id=1, debug=False):

        """
        Listening Experiment Py: SAQI - A Spatial Audio Inventory

        (C) 2021 by Tim Lübeck
                TH Köln - University of Applied Sciences
                Institute of Communications Engineering
                Department of Acoustics and Audio Signal Processing

        Parameters
        ----------
        ssr_handler
        jack_handler
        experiment_handler
        language
        verbose
        """
        super().__init__()
        self.setWindowTitle('')
        self._ssr_handler = ssr_handler
        self._experiment_handler = experiment_handler
        self._jack_handler = jack_handler
        self._ui = None
        self._language = language
        self.debug = debug

        self._monitor = QtWidgets.QDesktopWidget().screenGeometry(monitor_id)

    def start_welcome_screen(self):
        self._ui = Welcome_gui()
        self._ui.setupUi(self, "TUB_Chalmers_THK", self._language)

        # callbacks
        self._ui.age_combobox.activated.connect(
            lambda: self.set_participant_infos(0))
        self._ui.gender_combobox.activated.connect(
            lambda: self.set_participant_infos(1))
        self._ui.general_exp_combobox.activated.connect(
            lambda: self.set_participant_infos(2))
        self._ui.binaural_exp_combobox.activated.connect(
            lambda: self.set_participant_infos(3))

        self._ui.start_btn.clicked.connect(self.finish_login)
        #self._ui.calibrate_btn.clicked.connect(self._ssr_handler.calibrate_tracker)

        self.checked_participant_infos = list([0, 0, 0, 0])

    def finish_login(self):
        if not self.debug:
            if self._ssr_handler._is_calibrated:
                if np.sum(self.checked_participant_infos) == len(self.checked_participant_infos):
                    self.checked_participant_infos[0] = self._ui.age_combobox.currentText()
                    self.checked_participant_infos[1] = self._ui.gender_combobox.currentText()
                    self.checked_participant_infos[2] = self._ui.general_exp_combobox.currentText()
                    self.checked_participant_infos[3] = self._ui.binaural_exp_combobox.currentText()
                    self._experiment_handler.set_participant_infos(self.checked_participant_infos)

                    message_box = QtWidgets.QMessageBox()
                    message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                    message_box.move(int(self._monitor.left()/1.7),
                                     int(self._monitor.top()*1.5))

                    if self._language == 'english':
                        message = 'Thanks for participating in our listenining experiment.'

                    elif self._language == 'german':
                        message = 'Danke für die Teilnahme an unserm Hörversuch.'
                    else:
                        message = ''
                    message_box = QtWidgets.QMessageBox.information(
                        message_box, 'Error', message,
                        QtWidgets.QMessageBox.Ok)

                    self.start_main_experiment_screen()
                else:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                    message_box.move(int(self._monitor.left() / 1.7), int(self._monitor.top() * 1.5))

                    if self._language == 'english':
                        message = 'Please fill all fields.'
                    elif self._language == 'german':
                        message = 'Bitte fülle alle Felder aus.'
                    else:
                        message = ''
                    message_box = QtWidgets.QMessageBox.warning(message_box, 'Error', message,
                                                                QtWidgets.QMessageBox.Ok)
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                message_box.move(int(self._monitor.left() / 1.7), int(self._monitor.top() * 1.5))


                if self._language == 'english':
                    message = 'Please calibrate tracker before starting the experiment.'
                elif self._language == 'german':
                    message = 'Bitte calibriere den Head tracker bevor du das Experiment startest.'
                else:
                    message = ''
                message_box = QtWidgets.QMessageBox.warning(
                    message_box, 'Error', message, QtWidgets.QMessageBox.Ok)
        else:
            self.start_main_experiment_screen()

    def start_main_experiment_screen(self):
        pass

    def start_goodby_screen(self):
        self._ui = goodbye_gui()
        self._ui.setupUi(self)
        self._ui.finish_btn.clicked.connect(self.close_app)

    def set_participant_infos(self, id):
        self.checked_participant_infos[id] = 1

    def next_trial(self):
        pass

    def close_app(self):
        if self._ssr_handler is not None:
            self._ssr_handler.destroy_handler()
        self.close()