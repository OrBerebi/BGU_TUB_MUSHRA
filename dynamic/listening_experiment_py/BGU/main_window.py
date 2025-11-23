from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox
import numpy as np
from functools import partial
from .. GUI.welcome_gui import Welcome_gui
from .. GUI.goodbye_gui import goodbye_gui
from .. GUI.utils import FooterTUB_THK_Chalmers
from .gui import gui
from .. classes.main_window import MainWindow
import os
import sys

# 1. Get the absolute path to this script
script_path = os.path.abspath(__file__)
# 2. Get the directory containing this script
current_dir = os.path.dirname(script_path)
# 3. Go up two levels to find the project's root directory
project_root = os.path.dirname(os.path.dirname(current_dir))

# 4. Add this project root to the system's import path
if project_root not in sys.path:
    sys.path.append(project_root)

from results_analysis.aggregate_results import aggregate_mat_results


class MushraMainWindow(MainWindow):

    def __init__(self, ssr_handler, experiment_handler, language='english',
                 monitor_id=1, debug=False):

        """
        Listening Experiment Py: SAQI - A Spatial Audio Inventory
        (C) 2021 by Tim Lübeck
        Modified 2025 for BGU/TUB MUSHRA
        """
        super().__init__(ssr_handler=ssr_handler,
                         experiment_handler=experiment_handler,
                         language=language,
                         monitor_id=monitor_id, debug=debug)

        self.setWindowTitle('')

        self._ui = None
        self._language = language
        self.debug = debug
        self.last_button = None
        
        # Start the welcome screen
        self.start_welcome_screen()
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key_M:
            print("Mute all triggered via keyboard")
            self._ui.Mute_all.clicked.emit()
            self.animate_button(self._ui.Mute_all)
        elif key == Qt.Key_1:
            print("Ref button triggered via keyboard")
            self._ui.Ref_btn.clicked.emit()
            self.animate_button(self._ui.Ref_btn)
        elif Qt.Key_2 <= key <= Qt.Key_9:
            btn_idx = key - Qt.Key_2  # Convert key to index (2 -> 0, 3 -> 1, ..., 9 -> 7)
            if 0 <= btn_idx < len(self.ssr_ids):
                print(f"Play/Pause button {btn_idx} triggered via keyboard")
                self._ui.play_pause_btns[btn_idx].clicked.emit()
                self.animate_button(self._ui.play_pause_btns[btn_idx])
        
        super().keyPressEvent(event)
    
    def animate_button(self, button):
        if self.last_button and self.last_button != button:
            self.last_button.setStyleSheet("")
        
        button.setStyleSheet("background-color: #D3D3D3; border-radius: 5px;")
        self.last_button = button
    
    def start_welcome_screen(self):
        """
        Initialize the new Welcome GUI with the updated PDF questions.
        """
        self._ui = Welcome_gui()
        self._ui.setupUi(self, "TUB_Chalmers_THK", self._language,
                         footer=FooterTUB_THK_Chalmers(
                            experiment_name=""))

        # Connect the start button to the login finisher
        self._ui.start_btn.clicked.connect(self.finish_login)
        
        # Note: Removed old 'activated' connections (age, health, etc.) 
        # because the widgets have changed and we now collect data 
        # in bulk when 'Start' is clicked.

    def finish_login(self):
        """
        Collects data from the new GUI fields and starts the experiment.
        """
        if not self.debug:
            # 1. Collect all data from the new widgets in Welcome_gui
            participant_data = {
                'gender': self._ui.gender_combobox.currentText(),
                'year_born': self._ui.year_born_edit.text(),
                'native_language': self._ui.language_combobox.currentText(),
                'german_proficiency': self._ui.german_level_combobox.currentText(),
                'education': self._ui.education_combobox.currentText(),
                'hearing_impairment': self._ui.hearing_combobox.currentText(),
                
                'acoustics_profession': self._ui.acoustics_prof_combobox.currentText(),
                'acoustics_years': self._ui.acoustics_years_edit.text(),
                'music_profession': self._ui.music_prof_combobox.currentText(),
                'music_years': self._ui.music_years_edit.text(),
                'musical_instrument': self._ui.instrument_combobox.currentText(),
                'instrument_years': self._ui.instrument_years_edit.text(),
                
                'prior_experiment': self._ui.prior_exp_combobox.currentText(),
                'num_studies': self._ui.num_studies_edit.text(),
                'listening_hours_daily': self._ui.listening_hours_edit.text(),
                'matriculation_number': self._ui.matriculation_edit.text()
            }

            # 2. Pass this dictionary to the experiment handler
            # Ensure your experiment_handler can accept a dict, 
            # otherwise, convert this to a list if strictly required.
            self._experiment_handler.set_participant_infos(participant_data)

            # 3. Show Instructions
            message_box = QtWidgets.QMessageBox()
            message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
            # Safe move logic
            if self._monitor:
                message_box.move(
                    int(self._monitor.left() / 1.7), int(self._monitor.top() * 1.5))
            
            if self._language == 'english':
                message = 'Thank you for participating in our listening experiment.\nThe experiment starts now.\n\nIn this experiment, you will be asked to rate the Overall Quality difference between a Reference and a Test signal.\n\nYou will first listen to the Reference signal, followed by a short pause, and then the Test signal.\n\nThis is a global evaluation. You should consider all audible differences—such as coloration, spatial distortions, source postion dynamics, or added noise—and rate the general fidelity of the test signal relative to the reference.'
            elif self._language == 'german':
                message = 'Danke für die Teilnahme an unserem Hörversuch\nDer Versuch startet nun.'
            else:
                message = ''
            
            QtWidgets.QMessageBox.information(
                message_box, 'Info', message,
                QtWidgets.QMessageBox.Ok)

            self.start_main_experiment_screen()

        else:
            # Debug mode skips validation
            self.start_main_experiment_screen()

    def start_main_experiment_screen(self):
        self._ui = gui()
        print("num_stimuli_per_page: ", self._experiment_handler.num_stimuli_per_page)
        self._ui.setupUi(self,
                         num_stimuli_per_page=self._experiment_handler.num_stimuli_per_page,
                         language=self._language)
        for idx in range(0, len(self._ui.rating_sliders)):
            self._ui.plus_btns[idx].clicked.connect(
                partial(self.increase_slider_with_btn, idx))
            self._ui.minus_btns[idx].clicked.connect(
                partial(self.decrease_slider_with_btn, idx))

        self._ui.next_trial_btn.clicked.connect(self.next_trial)
        self._experiment_handler.reset_ssr_ids()
        self.update_gui()

    def start_goodby_screen(self):
        self._ui = goodbye_gui()
        self._ui.setupUi(self, self._language,
                         footer=FooterTUB_THK_Chalmers(
                            experiment_name=""))
        self._ui.finish_btn.clicked.connect(self.close_app)

    def next_trial(self):
        # mute ssr sources
        self._ssr_handler.mute_all(stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal)

        # check if we are still in a trial (i.e., sliders exist and are visible/enabled)
        active_sliders = [
            slider for slider in self._ui.rating_sliders 
            if slider.isVisible() and slider.isEnabled()
        ]

        if active_sliders:  # Only enforce rule if we're in a trial
            results = [slider.value() for slider in active_sliders]

            if 100 not in results:
                QMessageBox.warning(
                    self, 
                    "Incomplete Rating", 
                    "You need to rate at least one signal 100 before proceeding."
                )
                return  # Stop and do not continue
            
            if not all(self._stimulus_played_flags):
                QMessageBox.warning(
                    self,
                    "Incomplete Listening",
                    "You should listen to all of the signals before proceeding to the next trial."
                )
                print(self._stimulus_played_flags)
                return  # Stop here

            # write results
            if not self.debug and not self._experiment_handler.switch_phase:
                self._experiment_handler.write_results(
                    values=results,
                    current_ssr_ids=self.ssr_ids,
                    ref_id=self.ref_ssr_id
                )
                
        if self._experiment_handler.switch_phase:
            self.start_goodby_screen()  # End experiment instead of starting Phase 2
        else:
            # trigger next trial
            self._experiment_handler.next_trial()
            self.update_gui()

    def update_gui(self):
        # update gui and register callbacks
        self.ssr_ids, curr_atr, self.ref_ssr_id, self.curr_gif_path, self.curr_sample_lengths = self._experiment_handler.get_current_ssr_ids()
        
        if len(self.ssr_ids) == 0:
            self._ui.print_task("poo", finish=True)
        else:
            self._ui.print_task(curr_atr, finish=False)

        print("current attribute ids: ", curr_atr)
        print(self.ssr_ids)
        print("curr ref id: ", self.ref_ssr_id)

        if len(self.ssr_ids) != 0:
            # Reference button
            self._ui.Ref_btn.setVisible(False)
            try:
                self._ui.Ref_btn.clicked.disconnect()
            except TypeError:
                pass
            
            self._ui.Ref_btn.clicked.connect(partial(self._ssr_handler.play_source_once, [self.ref_ssr_id, self.ref_ssr_id], playing_label=self._ui.current_playing_label, playGifSignal=self._ui.playGifSignal, stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal))
            self._ui.Ref_btn.setVisible(True)

            # Mute button
            try:
                self._ui.Mute_all.clicked.disconnect()
            except TypeError:
                pass
            self._ui.Mute_all.clicked.connect(partial(self._ssr_handler.mute_all, stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal))
            self._ui.Mute_all.setVisible(True)

        else:
            self._ui.Ref_btn.setVisible(False)
            self._ui.Mute_all.setVisible(False)

        for btn, slider in zip(self._ui.play_pause_btns,
                               self._ui.rating_sliders):
            btn.setVisible(False)
            slider.setVisible(False)
            slider.setValue(50)

        for p_btn, m_btn in zip(self._ui.plus_btns,
                                self._ui.minus_btns):
            p_btn.setVisible(False)
            m_btn.setVisible(False)

        self._stimulus_played_flags = [False] * len(self.ssr_ids)

        for btn_idx in range(0, self.ssr_ids.shape[0]):
            try:
                self._ui.play_pause_btns[btn_idx].clicked.disconnect()
            except TypeError:
                pass 
            self._ui.play_pause_btns[btn_idx].clicked.connect(partial(self.mark_stimulus_played, btn_idx))
            self._ui.play_pause_btns[btn_idx].clicked.connect(partial(self._ssr_handler.play_source_once, [self.ref_ssr_id, self.ssr_ids[btn_idx]], playing_label=self._ui.current_playing_label, playGifSignal=self._ui.playGifSignal, stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal))
            
            self._ui.play_pause_btns[btn_idx].setVisible(True)
            self._ui.rating_sliders[btn_idx].setVisible(True)
            self._ui.plus_btns[btn_idx].setVisible(True)
            self._ui.minus_btns[btn_idx].setVisible(True)
        
        # update the gif path 
        if isinstance(self.curr_gif_path, str) and self.curr_gif_path:
            self._ui.gif_label.setVisible(True)
            self._ui.movie.setFileName(self.curr_gif_path)
            self._ui.movie.setScaledSize(self._ui.gif_label.size())
            self._ui.movie.jumpToFrame(0)
            self._ui.update_gif_speed(self.curr_sample_lengths)
        else:
            self._ui.gif_label.setVisible(False)
            self._ui.current_playing_label.setVisible(False)

        if self.debug:
            print(self.ssr_ids)

    def mark_stimulus_played(self, idx):
        self._stimulus_played_flags[idx] = True

    def increase_slider_with_btn(self, id):
        new_value = self._ui.rating_sliders[id].value() + self._ui.rating_sliders[id].getInterval()
        if new_value <= self._ui.rating_sliders[id].getMaximum():
            self._ui.rating_sliders[id].setValue(new_value)

    def decrease_slider_with_btn(self, id):
        new_value = self._ui.rating_sliders[id].value() - self._ui.rating_sliders[id].getInterval()
        if new_value >= self._ui.rating_sliders[id].getMinimum():
            self._ui.rating_sliders[id].setValue(new_value)

    def close_app(self):
        print("Starting data aggregation...")
        
        results_dir = os.path.join(project_root, 'bgu_results', 'results')
        output_csv = os.path.join(project_root, 'bgu_results', 'aggregated_results.csv')

        try:
            aggregate_mat_results(results_dir, output_csv)
            print(f"Aggregation complete. Data saved to {output_csv}")
        except FileNotFoundError:
            print(f"ERROR: Could not find results directory at {results_dir}")
        except Exception as e:
            print(f"ERROR: Data aggregation failed: {e}")

        if self._ssr_handler is not None:
            self._ssr_handler.destroy_handler()
        self.close()