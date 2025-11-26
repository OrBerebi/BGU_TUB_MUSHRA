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
# 1. Get the absolute path to this script (main_window.py)
#    e.g., /path/to/project/listening_experiment_py/classes/main_window.py
script_path = os.path.abspath(__file__)

# 2. Get the directory containing this script
#    e.g., /path/to/project/listening_experiment_py/classes
current_dir = os.path.dirname(script_path)

# 3. Go up two levels to find the project's root directory
#    Level 1 up: .../listening_experiment_py
#    Level 2 up: /path/to/project/
project_root = os.path.dirname(os.path.dirname(current_dir))

# 4. Add this project root to the system's import path
if project_root not in sys.path:
    sys.path.append(project_root)

# 5. Now you can import from 'results_analysis' as if you were at the root
from results_analysis.aggregate_results import aggregate_mat_results




class MushraMainWindow(MainWindow):

    def __init__(self, ssr_handler, experiment_handler, language='english',
                 monitor_id=1, debug=False):

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
        super().__init__(ssr_handler=ssr_handler,
                         experiment_handler=experiment_handler,
                         language=language,
                         monitor_id=monitor_id, debug=debug)

        self.setWindowTitle('')

        self._ui = None
        self._language = language
        self.debug = debug
        self.last_button = None
        self.current_attribute_context = None

        self.start_welcome_screen()
    
    def get_attribute_message(self, attribute):
        """Returns the specific instruction text based on the attribute."""
        
        # You can customize these texts based on your specific experiment attributes
        descriptions = {
            "Coloration": (
                "Task: Rate the Coloration differences.\n\n"
                "Coloration refers to the timbral quality and spectral balance of the sound. "
                "You should detect if the test signal sounds 'brighter,' 'duller,' "
                "or has unnatural resonances compared to the reference."
            ),
            "Source Position": (
                "Task: Rate the Source Position differences.\n\n"
                "Source Position refers to the perceived location of the sound event. "
                "You should detect if the direction (azimuth/elevation) or the distance "
                "of the sound source has shifted compared to the reference."
            ),
            "Overall Quality": (
                "Task: Rate the Overall Quality.\n\n"
                "This is a global evaluation. You should consider all audible differences—"
                "such as coloration, spatial distortions, source position dynamics, or added noise—"
                "and rate the general fidelity of the test signal relative to the reference."
            )
        }
        
        # Return the specific description, or a default message if the attribute isn't in the dict
        return descriptions.get(attribute, f"The rating attribute has changed.\n\nPlease now rate the signals in terms of: {attribute}")


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
        # Store the last pressed button
        if self.last_button and self.last_button != button:
            # Optionally reset previous button if you don't want it to stay highlighted
            self.last_button.setStyleSheet("")
        
        # Set the new button's animated "clicked" style (temporary highlight effect)
        button.setStyleSheet("background-color: #D3D3D3; border-radius: 5px;")  # Customize as needed

        # Update last_button to the currently pressed button
        self.last_button = button
    
    def start_welcome_screen(self):
        self._ui = Welcome_gui()
        self._ui.setupUi(self, "TUB_Chalmers_THK", self._language,
                         footer=FooterTUB_THK_Chalmers(
                            experiment_name=""))

        # callbacks
        self._ui.age_combobox.activated.connect(lambda:
                                                self.set_participant_infos(0))
        self._ui.gender_combobox.activated.connect(
            lambda: self.set_participant_infos(1))
        self._ui.general_exp_combobox.activated.connect(
            lambda: self.set_participant_infos(2))
        self._ui.binaural_exp_combobox.activated.connect(
                                                lambda:
                                                self.set_participant_infos(3))
        self._ui.health_status_combobox.activated.connect(
                                                lambda:
                                                self.set_participant_infos(4))
        self._ui.hearing_problems_combobox.activated.connect(
                                                lambda:
                                                self.set_participant_infos(5))

        self._ui.start_btn.clicked.connect(self.finish_login)
        #self._ui.calibrate_btn.clicked.connect(self._ssr_handler.calibrate_tracker)

        self.checked_participant_infos = list([0, 0, 0, 0, 0, 0])

    def finish_login(self):
        if not self.debug:
            
            # ✅ Always collect values from comboboxes, no click-checking
            self.checked_participant_infos[0] = self._ui.age_combobox.currentText()
            self.checked_participant_infos[1] = self._ui.gender_combobox.currentText()
            self.checked_participant_infos[2] = self._ui.general_exp_combobox.currentText()
            self.checked_participant_infos[3] = self._ui.binaural_exp_combobox.currentText()
            self.checked_participant_infos[4] = self._ui.health_status_combobox.currentText()
            self.checked_participant_infos[5] = self._ui.hearing_problems_combobox.currentText()

            self._experiment_handler.set_participant_infos(self.checked_participant_infos)

            message_box = QtWidgets.QMessageBox()
            message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
            message_box.move(
                int(self._monitor.left() / 1.7), int(self._monitor.top() * 1.5))

            if self._language == 'english':
                # Description for Coloration
                #message = 'Thank you for participating in our listening experiment\nThe experiment starts now.\nIn this experimnt you will be asked to rate the signals in terms of coloration or source position difference.\n\nColoration refers to the timbral quality and spectral balance of the sound. You should detect if the test signal sounds "brighter," "duller," or has unnatural resonances compared to the reference.\n\nSource Position refers to the perceived location of the sound event. You should detect if the direction (azimuth/elevation) or the distance of the sound source has shifted compared to the reference.'
                message = 'Thank you for participating in our listening experiment\nThe experiment starts now.'
            elif self._language == 'german':
                message = 'Danke für die Teilnahme an unserem Hörversuch\nDer Versuch startet nun.'
            else:
                message = ''
            QtWidgets.QMessageBox.information(
                message_box, 'Info', message,
                QtWidgets.QMessageBox.Ok)

            self.start_main_experiment_screen()

        else:
            self.start_main_experiment_screen()

    """
    def finish_login(self):
        if not self.debug:

            if self._ssr_handler._is_calibrated:
                if np.sum(self.checked_participant_infos) == \
                        len(self.checked_participant_infos):
                    self.checked_participant_infos[0] = \
                        self._ui.age_combobox.currentText()
                    self.checked_participant_infos[1] = \
                        self._ui.gender_combobox.currentText()
                    self.checked_participant_infos[2] = \
                        self._ui.general_exp_combobox.currentText()
                    self.checked_participant_infos[3] = \
                        self._ui.binaural_exp_combobox.currentText()
                    self.checked_participant_infos[4] = \
                        self._ui.health_status_combobox.currentText()
                    self.checked_participant_infos[3] = \
                        self._ui.hearing_problems_combobox.currentText()
                    self._experiment_handler.set_participant_infos(
                        self.checked_participant_infos)

                    message_box = QtWidgets.QMessageBox()
                    message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                    message_box.move(
                        int(self._monitor.left()/1.7), int(self._monitor.top()*1.5))

                    if self._language == 'english':
                        message = 'Thanks for participating in our listenining experiment\n The experiment starts now. '

                    elif self._language == 'german':
                        message = 'Danke für die Teilnahme an unserm Hörversuch\n Der Versuch startet nun.'
                    else:
                        message = ''
                    message_box = QtWidgets.QMessageBox.information(
                        message_box, 'Error', message,
                        QtWidgets.QMessageBox.Ok)

                    self.start_main_experiment_screen()
                else:
                    message_box = QtWidgets.QMessageBox()
                    message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                    message_box.move(int(self._monitor.left()/1.7),
                                     int(self._monitor.top()*1.5))

                    if self._language == 'english':
                        message = 'Please fill all fields.'
                    elif self._language == 'german':
                        message = 'Bitte fülle alle Felder aus.'
                    else:
                        message = ''
                    message_box = QtWidgets.QMessageBox.warning(
                        message_box, 'Error', message,
                        QtWidgets.QMessageBox.Ok)
            else:
                message_box = QtWidgets.QMessageBox()
                message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                message_box.move(int(self._monitor.left() / 1.7),
                                 int(self._monitor.top()*1.5))

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
    """

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

    def set_participant_infos(self, id):
        self.checked_participant_infos[id] = 1

    def next_trial(self):
        # mute ssr sources
        #self._ssr_handler.mute_all(stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal)
        self._ssr_handler.mute_all()

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
        self.ssr_ids, curr_atr,self.ref_ssr_id  = self._experiment_handler.get_current_ssr_ids()
        #self._ssr_handler.def_ssr_handler_gui_link(self._ui)
        
        

        if len(self.ssr_ids) == 0:
            #curr_atr = "finish"
            #self.ref_ssr_id = 0
            self._ui.print_task("poo",finish=True)
        else:
            #curr_atr = self._experiment_handler.get_current_attributes()
            #self.ref_ssr_id = self._experiment_handler.get_current_reference_ssr_id()
            self._ui.print_task(curr_atr,finish=False)
            # --- NEW LOGIC STARTS HERE ---
            # Check if the attribute has changed from the last trial
            if curr_atr != self.current_attribute_context:
                
                # Update the tracker so it doesn't pop up again for the same attribute
                self.current_attribute_context = curr_atr
                
                # Create the Popup
                message_box = QtWidgets.QMessageBox()
                
                # Use the geometry you requested
                message_box.setGeometry(QtCore.QRect(700, 500, 151, 32))
                
                # Center it roughly on your monitor setup (from your existing code logic)
                if hasattr(self, '_monitor'):
                     message_box.move(int(self._monitor.left() / 1.7), int(self._monitor.top() * 1.5))

                # Get the text for the specific attribute
                msg_text = self.get_attribute_message(curr_atr)
                
                # Show the message
                QtWidgets.QMessageBox.information(
                    message_box, 
                    'New Rating Task', 
                    msg_text,
                    QtWidgets.QMessageBox.Ok
                )
            # --- NEW LOGIC ENDS HERE ---


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
            self._ui.Ref_btn.clicked.connect(partial(self._ssr_handler.select_source, self.ref_ssr_id))
            #self._ui.Ref_btn.clicked.connect(partial(self._ssr_handler.play_source_once, [self.ref_ssr_id, self.ref_ssr_id], playing_label=self._ui.current_playing_label, playGifSignal=self._ui.playGifSignal, stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal))
            self._ui.Ref_btn.setVisible(True)

            # Mute button
            try:
                self._ui.Mute_all.clicked.disconnect()
            except TypeError:
                pass
            #self._ui.Mute_all.clicked.connect(partial(self._ssr_handler.mute_all, stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal))
            self._ui.Mute_all.clicked.connect(partial(self._ssr_handler.mute_all))
            self._ui.Mute_all.setVisible(True)

            # Calibrate button
            #try:
            #    self._ui.Calibrate.clicked.disconnect()
            #except TypeError:
            #    pass
            #self._ui.Calibrate.clicked.connect(self._ssr_handler.calibrate_tracker)
            #self._ui.Calibrate.setVisible(True)
        else:
            self._ui.Ref_btn.setVisible(False)
            self._ui.Mute_all.setVisible(False)
            #self._ui.Calibrate.setVisible(False)


        for btn, slider in zip(self._ui.play_pause_btns,
                               self._ui.rating_sliders):
            btn.setVisible(False)
            slider.setVisible(False)
            slider.setValue(50)

        for p_btn, m_btn in zip(self._ui.plus_btns,
                                self._ui.minus_btns):
            p_btn.setVisible(False)
            m_btn.setVisible(False)


        #self._stimulus_played_flags = [False] * len(self._ui.play_pause_btns)
        self._stimulus_played_flags = [False] * len(self.ssr_ids)

        for btn_idx in range(0, self.ssr_ids.shape[0]):
            try:
                self._ui.play_pause_btns[btn_idx].clicked.disconnect()
            except TypeError:
                pass  # Ignore the error if there were no previous connections
            self._ui.play_pause_btns[btn_idx].clicked.connect(partial(self.mark_stimulus_played, btn_idx))
            #self._ui.play_pause_btns[btn_idx].clicked.connect(partial(self._ssr_handler.play_source_once,[self.ref_ssr_id, self.ssr_ids[btn_idx]],playing_label=self._ui.current_playing_label, playGifSignal=self._ui.playGifSignal, stopGifSignal=self._ui.stopGifSignal, rewindGifSignal=self._ui.rewindGifSignal))
            self._ui.play_pause_btns[btn_idx].clicked.connect(partial(self._ssr_handler.select_source, self.ssr_ids[btn_idx]))
            self._ui.play_pause_btns[btn_idx].setVisible(True)
            self._ui.rating_sliders[btn_idx].setVisible(True)
            self._ui.plus_btns[btn_idx].setVisible(True)
            self._ui.minus_btns[btn_idx].setVisible(True)
        
        """
        # update the gif path 
        if isinstance(self.curr_gif_path, str) and self.curr_gif_path:
            self._ui.gif_label.setVisible(True)
            self._ui.movie.setFileName(self.curr_gif_path)
            self._ui.movie.setScaledSize(self._ui.gif_label.size())
            self._ui.movie.jumpToFrame(0)
        else:
            self._ui.gif_label.setVisible(False)
            self._ui.current_playing_label.setVisible(False)
        """



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
            # Call the function directly with the full, absolute paths
            aggregate_mat_results(results_dir, output_csv)
            print(f"Aggregation complete. Data saved to {output_csv}")
            
        except FileNotFoundError:
            print(f"ERROR: Could not find results directory at {results_dir}")
        except Exception as e:
            print(f"ERROR: Data aggregation failed: {e}")
            # You could show this error in a GUI pop-up


        print("Shutting down OSC server...")
        if hasattr(self._ssr_handler, 'server') and self._ssr_handler.server:
            self._ssr_handler.server.shutdown()  # Shuts down the server thread
            self._ssr_handler.server.server_close() # Closes the server socket
            print("✅ OSC server shut down.")

        # ... other cleanup ...

        self.close() # This presumably closes your main GUI window