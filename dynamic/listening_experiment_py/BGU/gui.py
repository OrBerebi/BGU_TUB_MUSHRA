# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtSvg, QtGui
from ..GUI.utils import LabeledSlider, FooterTUB_THK_Chalmers


class gui(QtWidgets.QMainWindow):
    # Signals to control GIF from SSR handler
    playGifSignal   = QtCore.pyqtSignal()
    stopGifSignal   = QtCore.pyqtSignal()
    rewindGifSignal = QtCore.pyqtSignal()

    def __init__(self, num_stimuli_per_page=3, language='english', show_pm_btns=True):
        super().__init__()

    def setupUi(self, ui, num_stimuli_per_page, language='english',gif_path = "/Users/orberebi/Documents/GitHub/TUB-BGU-colab/MUSHRA_2025/SSR_scene/gifs/median_plane_rotation.gif" , show_pm_btns=True):
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

        # ========= START: GIF STUFF=====================
        vlayout = QtWidgets.QVBoxLayout()

        # Create a vertical layout for the GIF
        gif_layout = QtWidgets.QVBoxLayout()

        self.gif_label = QtWidgets.QLabel(self.centralwidget)
        self.gif_label.setAlignment(QtCore.Qt.AlignCenter)
        self.gif_label.setFixedSize(400, 400)  # or leave flexible
        self.movie = QtGui.QMovie(gif_path)
        self.movie.setScaledSize(self.gif_label.size())  # 🔑 scale frames
        #self.movie.setLoops(1)  # play only once
        self.gif_label.setMovie(self.movie)
        self.movie.jumpToFrame(0)   # start at the beginning

        # connect signals to slots
        self.playGifSignal.connect(self.movie.start)
        self.stopGifSignal.connect(self.movie.stop)
        self.rewindGifSignal.connect(self.rewind_gif)
        self.movie.finished.connect(self.rewind_gif)

        
        audio_samples = 236540
        sample_rate = 48000  # Hz
        audio_duration_sec = audio_samples / sample_rate
        print(f"Audio duration: {audio_duration_sec:.3f} seconds")

        gif_frames = 51
        frame_delay_sec = audio_duration_sec / gif_frames
        frame_delay_ms = frame_delay_sec * 1000  # QMovie uses milliseconds
        print(f"Set GIF frame delay to {frame_delay_ms:.2f} ms per frame")

        self.movie.setSpeed(100)  # 100% = normal speed
        # Optional: scale the movie to match audio exactly
        # Calculate relative speed factor
        original_delay_ms = self.movie.nextFrameDelay()  # typical frame delay in GIF
        speed_factor = int(original_delay_ms / frame_delay_ms * 100)
        self.movie.setSpeed(speed_factor)  # percentage


        #self.movie.start()

        gif_layout.addWidget(self.gif_label)
        # ========= END: GIF STUFF=====================



        self.Ref_btn = QtWidgets.QPushButton(self.centralwidget)
        self.Ref_btn.setFixedSize(100, 30)
        self.Ref_btn.setObjectName("Ref_btn")
        self.Ref_btn.setText('Reference (1)')

        self.Mute_all = QtWidgets.QPushButton(self.centralwidget)
        self.Mute_all.setFixedSize(100, 30)
        self.Mute_all.setObjectName("Mute_all")
        self.Mute_all.setText('(M)ute')

        #self.Calibrate = QtWidgets.QPushButton(self.centralwidget)
        #self.Calibrate.setFixedSize(100, 30)
        #self.Calibrate.setObjectName("Calibrate")
        #self.Calibrate.setText('(C)alibrate')

        self.current_playing_label = QtWidgets.QLabel(self.centralwidget)
        self.current_playing_label.setObjectName("current_playing_label")
        self.current_playing_label.setText("Playing Non")
        self.current_playing_label.setAlignment(QtCore.Qt.AlignCenter)
        self.current_playing_label.setStyleSheet("color: yellow; font-size: 14pt; font-weight: bold;")
        
        vlayout.addWidget(self.current_playing_label)  # add it above Calibrate
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
                                       labels=('Large (0)',
                                               '     (25)',
                                               '     (50)',
                                               '     (75)',
                                               'No  (100)')))
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

        slider_layout.addLayout(gif_layout) # Adding the GIF
        
        main_layout.addLayout(slider_layout)

        

        main_layout.addLayout(FooterTUB_THK_Chalmers(experiment_name='MUSHRA Listening Experiment'))

        ui.setCentralWidget(self.centralwidget)
        self.retranslateUi(ui)
        #self.print_task()
        QtCore.QMetaObject.connectSlotsByName(ui)

    def rewind_gif(self):
        self.movie.stop()
        self.movie.jumpToFrame(0)

    def start_gif(self):
        if hasattr(self, '_ui') and hasattr(self._ui, 'movie') and self._ui.movie is not None:
            self._ui.movie.start()

    def retranslateUi(self, ui):
        _translate = QtCore.QCoreApplication.translate
        ui.setWindowTitle(_translate("OLE_gui",
                                     "MUSHRA Listening Experiment"))

    def print_task(self,attribute, finish=False):
        if not finish:
            if self.language == 'english':
                self.task_label.setText("Rate the difference between each signal and the reference in terms of " + attribute)
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