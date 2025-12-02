from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
import numpy as np


class Footer(QtWidgets.QVBoxLayout):
    def __init__(self, experiment_name='Listening Experiment'):
        super().__init__()
        Separador = QtWidgets.QFrame()
        Separador.setFrameShape(QtWidgets.QFrame.HLine)
        Separador.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Fixed)
        Separador.setLineWidth(10)

        self.addWidget(Separador)

        hlayout = QtWidgets.QHBoxLayout()
        self.title_label = QtWidgets.QLabel()
        self.title_label.setObjectName("title_label")
        self.title_label.raise_()
        self.title_label.setFixedHeight(80)
        self.title_label.setText(experiment_name)
        self.title_label.setStyleSheet(f"font-family: Helvetica; color: gray; font-size: 25pt")
        hlayout.addWidget(self.title_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            200, 50, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed))

        self.openGLWidget = QtSvg.QSvgWidget(
            'listening_experiment_py/GUI/thk_logo_bw_transparent.svg')
        self.openGLWidget.setObjectName("openGLWidget")
        self.openGLWidget.setFixedSize(120, 90)
        hlayout.addWidget(self.openGLWidget)

        self.addLayout(hlayout)


class FooterTUB_THK_Chalmers(QtWidgets.QVBoxLayout):
    def __init__(self, experiment_name='Listening Experiment'):
        super().__init__()
        Separador = QtWidgets.QFrame()
        Separador.setFrameShape(QtWidgets.QFrame.HLine)
        Separador.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Fixed)
        Separador.setLineWidth(10)

        self.addWidget(Separador)

        hlayout = QtWidgets.QHBoxLayout()
        self.title_label = QtWidgets.QLabel()
        self.title_label.setObjectName("title_label")
        self.title_label.raise_()
        self.title_label.setFixedHeight(80)
        self.title_label.setText(experiment_name)
        self.title_label.setStyleSheet(f"font-family: Helvetica; color: gray; font-size: 25pt")
        hlayout.addWidget(self.title_label)
        hlayout.addItem(QtWidgets.QSpacerItem(
            200, 50, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Fixed))

        #self.openGLWidget = QtSvg.QSvgWidget('listening_experiment_py/GUI/chalmers_logo.svg')
        #self.openGLWidget.setObjectName("openGLWidget")
        #self.openGLWidget.setFixedSize(190, 56)
        #hlayout.addWidget(self.openGLWidget)

        #self.openGLWidget = QtSvg.QSvgWidget('listening_experiment_py/GUI/thk_logo_bw_transparent.svg')
        #self.openGLWidget.setObjectName("openGLWidget")
        #self.openGLWidget.setFixedSize(120, 90)
        #hlayout.addWidget(self.openGLWidget)

        self.openGLWidget = QtSvg.QSvgWidget('listening_experiment_py/GUI/Ben-Logo.svg')
        self.openGLWidget.setObjectName("openGLWidget")
        self.openGLWidget.setFixedSize(120, 90)
        hlayout.addWidget(self.openGLWidget)

        self.openGLWidget = QtSvg.QSvgWidget('listening_experiment_py/GUI/tub_logo.svg')
        self.openGLWidget.setObjectName("openGLWidget")
        self.openGLWidget.setFixedSize(100, 70)
        hlayout.addWidget(self.openGLWidget)

        self.addLayout(hlayout)


class TrackedLabel(QtWidgets.QLabel):
    is_under_mouse = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QtWidgets.QPushButton.__init__(self, parent)
        self.setMouseTracking(True)

    def enterEvent(self, event):
        self.is_under_mouse.emit(True)

    def leaveEvent(self, event):
        self.is_under_mouse.emit(False)


class LabeledSlider(QtWidgets.QWidget):
    def __init__(self, minimum, maximum, interval=1,
                 orientation=QtCore.Qt.Horizontal,
                 labels=None, parent=None, steps_per_interval=1):
        super(LabeledSlider, self).__init__(parent=parent)

        # Create the vertical separator line
        self.separator = QtWidgets.QFrame(self)
        self.separator.setFrameShape(QtWidgets.QFrame.VLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.separator.setLineWidth(2)

        # Create the slider
        self.sl = QtWidgets.QSlider(orientation, self)
        self.steps_per_interval = steps_per_interval
        self.minimum = int(minimum * self.steps_per_interval)
        self.maximum = int(maximum * self.steps_per_interval)
        self.interval = int(interval * self.steps_per_interval)

        # Add current value label
        self.value_label = QtWidgets.QLabel("0", self)
        self.value_label.setAlignment(QtCore.Qt.AlignCenter)
        font = self.value_label.font()
        font.setBold(True)
        font.setPointSize(20)  # Larger font size
        self.value_label.setFont(font)
        
        # Reserve space for 3 digits
        fm = QtGui.QFontMetrics(font)
        label_width = fm.boundingRect("100").width() + 10
        self.value_label.setFixedWidth(label_width)

        self.setTicks(labels=labels)

        # Layout margins and configuration
        self.left_margin = 10
        self.top_margin = 10
        self.right_margin = 10
        self.bottom_margin = 10

        self.sl.setMinimum(minimum)
        self.sl.setMaximum(maximum)
        self.sl.setValue(minimum)
        self.sl.setTickInterval(interval)

        # Create a spacer
        self.spacer = QtWidgets.QSpacerItem(100, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
    
        # --- MODIFIED LAYOUT LOGIC ---
        if orientation == QtCore.Qt.Horizontal:
            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.setContentsMargins(self.left_margin, self.top_margin, 
                                           self.right_margin, self.bottom_margin)
            
            self.sl.setTickPosition(QtWidgets.QSlider.TicksBelow)
            self.sl.setMinimumWidth(300)

            # Horizontal logic
            self.layout.addWidget(self.separator)
            self.layout.addItem(self.spacer)
            self.layout.addWidget(self.sl)
            # Note: For horizontal, the value_label placement logic isn't defined 
            # in your original snippet, but this preserves existing behavior.
        else:
            self.sl.setTickPosition(QtWidgets.QSlider.TicksLeft)
            self.sl.setMinimumHeight(300)

            # 1. Main Vertical Layout (Stack Top to Bottom)
            self.layout = QtWidgets.QVBoxLayout(self)
            self.layout.setContentsMargins(self.left_margin, self.top_margin, 
                                           self.right_margin, self.bottom_margin)

            # 2. Add the Number Label at the very top
            self.layout.addWidget(self.value_label, 0, QtCore.Qt.AlignCenter)

            # 3. Create a sub-layout for the Slider components (Side by Side)
            slider_assembly = QtWidgets.QHBoxLayout()
            slider_assembly.setContentsMargins(0, 0, 0, 0)
            
            # Add separator, spacer and slider to the sub-layout
            slider_assembly.addWidget(self.separator)
            # We removed value_label from here
            slider_assembly.addItem(self.spacer)
            slider_assembly.addWidget(self.sl)

            # Add the sub-layout to the main vertical layout
            self.layout.addLayout(slider_assembly)
        # -----------------------------

        # connect the slider to the label update
        self.sl.valueChanged.connect(self.update_value_label)
        self.update_value_label(self.sl.value())

    def update_value_label(self, val):
        self.value_label.setText(str(int(val / self.steps_per_interval)))

    def value(self):
        return self.sl.value() / self.steps_per_interval

    def setValue(self, value):
        self.sl.setValue(int(value))

    def getMaximum(self):
        return self.maximum

    def getMinimum(self):
        return self.minimum

    def getInterval(self):
        return self.interval

    def setTicks(self, minimum=None, maximum=None, interval=None, labels=None):
        if minimum is not None:
            self.minimum = int(minimum * self.steps_per_interval)
        if maximum is not None:
            self.maximum = int(maximum * self.steps_per_interval)
        if interval is not None:
            self.interval = int(interval * self.steps_per_interval)

        self.sl.setMinimum(self.minimum)
        self.sl.setMaximum(self.maximum)

        levels = range(self.minimum, self.maximum+self.interval, self.interval)
        if labels is not None:
            if not isinstance(labels, (tuple, list)):
                raise Exception("<labels> is a list or tuple.")
            if len(labels) != len(levels):
                raise Exception("Size of <labels> doesn't match levels.")
            self.levels = list(zip(levels, labels))
        else:
            self.levels = list(zip(levels, map(str, levels)))

    def paintEvent(self, e):
        super(LabeledSlider, self).paintEvent(e)

        style = self.sl.style()
        painter = QtGui.QPainter(self)
        st_slider = QtWidgets.QStyleOptionSlider()
        st_slider.initFrom(self.sl)
        st_slider.orientation = self.sl.orientation()

        length = style.pixelMetric(QtWidgets.QStyle.PM_SliderLength, st_slider, self.sl)
        available = style.pixelMetric(QtWidgets.QStyle.PM_SliderSpaceAvailable, st_slider, self.sl)

        for v, v_str in self.levels:
            rect = painter.drawText(QtCore.QRect(), QtCore.Qt.AlignRight, v_str)
            
            if self.sl.orientation() == QtCore.Qt.Horizontal:
                x_loc = QtWidgets.QStyle.sliderPositionFromValue(
                    self.sl.minimum(), self.sl.maximum(), v, available) + length // 2
                
                # UPDATED: Use self.sl.x() instead of self.left_margin to ensure 
                # alignment even if slider moves
                left = x_loc - rect.width() // 2 + self.sl.x()
                bottom = self.rect().bottom()
                
                # (Margin adjustments omitted for brevity, logic remains similar)
                pos = QtCore.QPoint(left, bottom)
                painter.drawText(pos, v_str)

            else:
                y_loc = QtWidgets.QStyle.sliderPositionFromValue(
                    self.sl.minimum(), self.sl.maximum(), v, available, upsideDown=True)

                # UPDATED: Use self.sl.y() instead of self.top_margin
                # This ensures that if the slider is pushed down by the label,
                # the text follows it correctly.
                bottom = y_loc + length // 2 + rect.height() // 2 + self.sl.y() - 3

                left = self.sl.geometry().x() - rect.width() - 4
                
                pos = QtCore.QPoint(left, bottom)
                painter.drawText(pos, v_str)

        return


class SliderTicks2():

    def __init__(self, x, y, centralwidget):
        self._x = x
        self._y = y
        self._width = 10
        self._height = 4  # tick height
        self._centralwidget = centralwidget
        self._ticks = list()
        self._labels = list()

    def draw(self, mode='bipolar', y=None, intervals=7, slider_height=245,
             label_texts=None, label_mode='numbered', fontsize=10):
        if y is None:
            y = self._y

        label_width = 4
        if (label_mode == 'at_ticks' and len(label_texts) == intervals) or (label_mode == 'between' and len(label_texts) == intervals-1):
            label_width = len(max(label_texts, key=len))*4.5

        if mode == 'unipolar':
            spacing = slider_height / (intervals)
            label_cnt = intervals
            for i in range(0, intervals+1):
                tick = QtWidgets.QFrame(self._centralwidget)
                tick.setGeometry(QtCore.QRect(self._x, y, self._width, self._height))
                tick.setFrameShape(QtWidgets.QFrame.HLine)
                tick.setFrameShadow(QtWidgets.QFrame.Sunken)
                tick.show()

                label = QtWidgets.QLabel(self._centralwidget)
                label.setGeometry(QtCore.QRect(self._x - self._width - label_width, y - 4,
                                               self._width, self._height))
                if label_mode == 'numbered' or label_texts is None:
                    label.setText(f"{int(label_cnt)}")
                elif label_mode == 'at_ticks':
                    if len(label_texts) == intervals:
                        label.setText(label_texts[i])
                elif label_mode == 'between' and i < intervals:
                    if len(label_texts) == intervals-1:
                        label.setGeometry(QtCore.QRect(self._x - self._width - label_width, y + spacing/2 - 4, self._width, self._height))
                        label.setText(label_texts[i])

                label.setStyleSheet(f"color: gray; font-size: {fontsize}pt")
                label.adjustSize()
                label.show()

                label_cnt = label_cnt - 1
                self._labels.append(label)
                y = y + spacing
                self._ticks.append(tick)

        elif mode == 'bipolar':
            spacing = slider_height / (intervals-1)
            label_cnt = np.floor(intervals/2)
            for i in range(0, intervals):
                tick = QtWidgets.QFrame(self._centralwidget)
                tick.setGeometry(QtCore.QRect(self._x, y,
                                      self._width, self._height))
                tick.setFrameShape(QtWidgets.QFrame.HLine)
                tick.setFrameShadow(QtWidgets.QFrame.Sunken)

                label = QtWidgets.QLabel(self._centralwidget)
                label.setGeometry(QtCore.QRect(self._x-self._width-label_width, y-4,
                                              self._width, self._height))

                if label_mode == 'numbered' or label_texts is None:
                    label.setText(f"{int(label_cnt)}")
                elif label_mode == 'at_ticks':
                    if len(label_texts) == intervals:
                        label.setText(label_texts[i])
                elif label_mode == 'between' and i < intervals-1:
                    if len(label_texts) == intervals-1:
                        label.setGeometry(QtCore.QRect(self._x - self._width - label_width, y + spacing/2 - 4, self._width, self._height))
                        label.setText(label_texts[i])
                label.setStyleSheet(f"color: gray; font-size: {fontsize}pt")
                label.adjustSize()

                label_cnt = label_cnt - 1
                y = y + spacing
                self._ticks.append(tick)
                self._labels.append(label)

    def hide(self):
        for tick in self._ticks:
            tick.hide()

        for label in self._labels:
            label.hide()

    def show(self):
        for tick in self._ticks:
            tick.show()

        for label in self._labels:
            label.show()


class SliderTicks():

    def __init__(self, x, y, centralwidget):
        self._x = x
        self._y = y
        self._width = 10
        self._height = 4  # tick height
        self._centralwidget = centralwidget
        self._ticks = list()
        self._labels = list()

    def draw(self, mode='bipolar', y=None, intervals=7, slider_height=245,
             label_texts=None, label_mode='numbered', fontsize=10):
        if y is None:
            y = self._y

        label_width = 4
        if (label_mode == 'at_ticks' and len(label_texts) == intervals) or (label_mode == 'between' and len(label_texts) == intervals-1):
            label_width = len(max(label_texts, key=len))*4.5

        if mode == 'unipolar':
            spacing = slider_height / (intervals)
            label_cnt = intervals
            for i in range(0, intervals+1):
                tick = QtWidgets.QFrame(self._centralwidget)
                tick.setGeometry(QtCore.QRect(self._x, y, self._width, self._height))
                tick.setFrameShape(QtWidgets.QFrame.HLine)
                tick.setFrameShadow(QtWidgets.QFrame.Sunken)
                tick.show()

                label = QtWidgets.QLabel(self._centralwidget)
                label.setGeometry(QtCore.QRect(self._x - self._width - label_width, y - 4,
                                               self._width, self._height))
                if label_mode == 'numbered' or label_texts is None:
                    label.setText(f"{int(label_cnt)}")
                elif label_mode == 'at_ticks':
                    if len(label_texts) == intervals:
                        label.setText(label_texts[i])
                elif label_mode == 'between' and i < intervals:
                    if len(label_texts) == intervals-1:
                        label.setGeometry(QtCore.QRect(self._x - self._width - label_width, y + spacing/2 - 4, self._width, self._height))
                        label.setText(label_texts[i])

                label.setStyleSheet(f"color: gray; font-size: {fontsize}pt")
                label.adjustSize()
                label.show()

                label_cnt = label_cnt - 1
                self._labels.append(label)
                y = y + spacing
                self._ticks.append(tick)

        elif mode == 'bipolar':
            spacing = slider_height / (intervals-1)
            label_cnt = np.floor(intervals/2)
            for i in range(0, intervals):
                tick = QtWidgets.QFrame(self._centralwidget)
                tick.setGeometry(QtCore.QRect(self._x, y,
                                      self._width, self._height))
                tick.setFrameShape(QtWidgets.QFrame.HLine)
                tick.setFrameShadow(QtWidgets.QFrame.Sunken)

                label = QtWidgets.QLabel(self._centralwidget)
                label.setGeometry(QtCore.QRect(self._x-self._width-label_width, y-4,
                                              self._width, self._height))

                if label_mode == 'numbered' or label_texts is None:
                    label.setText(f"{int(label_cnt)}")
                elif label_mode == 'at_ticks':
                    if len(label_texts) == intervals:
                        label.setText(label_texts[i])
                elif label_mode == 'between' and i < intervals-1:
                    if len(label_texts) == intervals-1:
                        label.setGeometry(QtCore.QRect(self._x - self._width - label_width, y + spacing/2 - 4, self._width, self._height))
                        label.setText(label_texts[i])
                label.setStyleSheet(f"color: gray; font-size: {fontsize}pt")
                label.adjustSize()

                label_cnt = label_cnt - 1
                y = y + spacing
                self._ticks.append(tick)
                self._labels.append(label)

    def hide(self):
        for tick in self._ticks:
            tick.hide()

        for label in self._labels:
            label.hide()

    def show(self):
        for tick in self._ticks:
            tick.show()

        for label in self._labels:
            label.show()


class ProgressBar(QtWidgets.QProgressBar):

    def __init__(self, *args, **kwargs):
        super(ProgressBar, self).__init__(*args, **kwargs)
        self.setValue(0)
        if self.minimum() != self.maximum():
            self.timer = QtCore.QTimer(self, timeout=self.onTimeout)
            self.timer.start(np.random.randint(1, 3) * 1000)

    def onTimeout(self):
        if self.value() >= 100:
            self.timer.stop()
            self.timer.deleteLater()
            del self.timer
            return
        self.setValue(self.value() + 1)