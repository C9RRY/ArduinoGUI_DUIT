import time
from datetime import datetime
from pathlib import Path
from pyqtgraph import PlotWidget
from threads import MyTimerThread
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QIODevice, QTimer
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 570)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 570))
        font = QtGui.QFont()
        font.setPointSize(16)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("background-color:rgb(51, 53, 52);")

        self.ports = ()
        self.logs_count = 0
        self.current_timer = 0
        self.timer_is_running = False
        self.port_is_connect = False
        self.current_encoder_position = 0
        self.port_wrong_read_count = 0
        self.input_data = ''
        self.input_data_dict = {"1": "0", "2": "0", "3": "0"}
        self.output_data_dict = {"1": "Duit the best!", "2": "0", "3": "0", "4": "0", "5": "0", "6": "0"}
        self.old_output_data_dict = {"1": "0", "2": "0", "3": "0", "4": "0", "5": "0", "6": "0"}
        self.moisture_value = 100
        self.rain_detector_value = 100
        self.relay_is_active = False
        self.ready_to_write = False
        self.pwm_value = 0
        self.current_path = Path(__file__).parent
        self.current_log = ''
        self.weather_status = "Sunny"
        self.lcd1602_cycle_count = 0

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_19 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_19.setObjectName("gridLayout_19")
        self.widget_options_block = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_options_block.sizePolicy().hasHeightForWidth())
        self.widget_options_block.setSizePolicy(sizePolicy)
        self.widget_options_block.setMinimumSize(QtCore.QSize(330, 500))
        self.widget_options_block.setMaximumSize(QtCore.QSize(1222222, 16777215))
        self.widget_options_block.setStyleSheet("")
        self.widget_options_block.setObjectName("widget_options_block")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.widget_options_block)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.toolButton = QtWidgets.QToolButton(self.widget_options_block)
        self.toolButton.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.toolButton.setObjectName("toolButton")
        self.gridLayout_17.addWidget(self.toolButton, 0, 0, 1, 1)
        self.widget_connection_block = QtWidgets.QWidget(self.widget_options_block)
        self.widget_connection_block.setMaximumSize(QtCore.QSize(1808, 88888))
        self.widget_connection_block.setObjectName("widget_connection_block")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.widget_connection_block)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.comboBox_COM_ports = QtWidgets.QComboBox(self.widget_connection_block)
        self.comboBox_COM_ports.activated.connect(self.get_port_info)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_COM_ports.sizePolicy().hasHeightForWidth())
        self.comboBox_COM_ports.setSizePolicy(sizePolicy)
        self.comboBox_COM_ports.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_COM_ports.setMaximumSize(QtCore.QSize(200, 30))
        self.comboBox_COM_ports.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.comboBox_COM_ports.setObjectName("comboBox_COM_ports")
        self.gridLayout_5.addWidget(self.comboBox_COM_ports, 0, 0, 1, 1)
        self.pushButton_com_port_connect = QtWidgets.QPushButton(self.widget_connection_block)
        self.pushButton_com_port_connect.clicked.connect(self.open_port)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_com_port_connect.sizePolicy().hasHeightForWidth())
        self.pushButton_com_port_connect.setSizePolicy(sizePolicy)
        self.pushButton_com_port_connect.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButton_com_port_connect.setMaximumSize(QtCore.QSize(200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_com_port_connect.setFont(font)
        self.pushButton_com_port_connect.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.pushButton_com_port_connect.setObjectName("pushButton_com_port_connect")
        self.gridLayout_5.addWidget(self.pushButton_com_port_connect, 1, 0, 1, 1)
        self.pushButton_com_port_disconnect = QtWidgets.QPushButton(self.widget_connection_block)
        self.pushButton_com_port_disconnect.clicked.connect(self.close_port)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_com_port_disconnect.sizePolicy().hasHeightForWidth())
        self.pushButton_com_port_disconnect.setSizePolicy(sizePolicy)
        self.pushButton_com_port_disconnect.setMinimumSize(QtCore.QSize(0, 35))
        self.pushButton_com_port_disconnect.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_com_port_disconnect.setFont(font)
        self.pushButton_com_port_disconnect.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.pushButton_com_port_disconnect.setObjectName("pushButton_com_port_disconnect")
        self.gridLayout_5.addWidget(self.pushButton_com_port_disconnect, 2, 0, 1, 1)
        self.frame_log_view = QtWidgets.QFrame(self.widget_connection_block)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_log_view.sizePolicy().hasHeightForWidth())
        self.frame_log_view.setSizePolicy(sizePolicy)
        self.frame_log_view.setMinimumSize(QtCore.QSize(300, 320))
        self.frame_log_view.setMaximumSize(QtCore.QSize(300, 700))
        self.frame_log_view.setStyleSheet("background-color:rgb(90, 93, 92);")
        self.frame_log_view.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_log_view.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_log_view.setLineWidth(2)
        self.frame_log_view.setObjectName("frame_log_view")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_log_view)
        self.gridLayout_4.setContentsMargins(3, -1, 3, -1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_com_port_number = QtWidgets.QLabel(self.frame_log_view)
        self.label_com_port_number.setObjectName("label_com_port_number")
        self.gridLayout_4.addWidget(self.label_com_port_number, 4, 0, 1, 1)
        self.label_log = QtWidgets.QLabel(self.frame_log_view)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_log.sizePolicy().hasHeightForWidth())
        self.label_log.setSizePolicy(sizePolicy)
        self.label_log.setMinimumSize(QtCore.QSize(216, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_log.setFont(font)
        self.label_log.setStyleSheet("")
        self.label_log.setObjectName("label_log")
        self.gridLayout_4.addWidget(self.label_log, 1, 0, 1, 1)
        self.label_arduino_connection_status = QtWidgets.QLabel(self.frame_log_view)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_arduino_connection_status.setFont(font)
        self.label_arduino_connection_status.setStyleSheet("color: rgb(170, 199, 197);")
        self.label_arduino_connection_status.setObjectName("label_arduino_connection_status")
        self.gridLayout_4.addWidget(self.label_arduino_connection_status, 1, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(self.frame_log_view)
        self.listWidget.setMaximumSize(QtCore.QSize(400, 16777215))
        self.listWidget.setStyleSheet("background-color:#989590;")
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_4.addWidget(self.listWidget, 3, 0, 1, 2)
        self.gridLayout_5.addWidget(self.frame_log_view, 3, 0, 1, 1)
        self.gridLayout_17.addWidget(self.widget_connection_block, 1, 0, 1, 1)
        self.gridLayout_19.addWidget(self.widget_options_block, 0, 0, 1, 1)
        self.widget_devices_block = QtWidgets.QWidget(self.centralwidget)
        self.widget_devices_block.setStyleSheet("")
        self.widget_devices_block.setObjectName("widget_devices_block")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.widget_devices_block)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.widget_devices_subblock1 = QtWidgets.QWidget(self.widget_devices_block)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_devices_subblock1.sizePolicy().hasHeightForWidth())
        self.widget_devices_subblock1.setSizePolicy(sizePolicy)
        self.widget_devices_subblock1.setMaximumSize(QtCore.QSize(3000, 3000))
        self.widget_devices_subblock1.setObjectName("widget_devices_subblock1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_devices_subblock1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(80, 1, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(369, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(368, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 5, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(369, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 0, 7, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(80, 1, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem4, 0, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(80, 1, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem5, 0, 6, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(120, 1, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem6, 0, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(369, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 0, 1, 1, 1)
        self.widget_i2c1602 = QtWidgets.QWidget(self.widget_devices_subblock1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_i2c1602.sizePolicy().hasHeightForWidth())
        self.widget_i2c1602.setSizePolicy(sizePolicy)
        self.widget_i2c1602.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_i2c1602.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_i2c1602.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_i2c1602.setObjectName("widget_i2c1602")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_i2c1602)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.widget_i2c1602)
        self.widget.setMinimumSize(QtCore.QSize(132, 138))
        self.widget.setObjectName("widget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setMinimumSize(QtCore.QSize(140, 0))
        self.widget_3.setObjectName("widget_3")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.checkBox_i2c1602_show_log = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox_i2c1602_show_log.setObjectName("checkBox_i2c1602_show_log")
        self.gridLayout_9.addWidget(self.checkBox_i2c1602_show_log, 2, 0, 1, 1)
        self.checkBox_i2c1602_show_pwm = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox_i2c1602_show_pwm.setObjectName("checkBox_i2c1602_show_pwm")
        self.gridLayout_9.addWidget(self.checkBox_i2c1602_show_pwm, 2, 1, 1, 1)
        self.checkBox_i2c1602_show_weather = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox_i2c1602_show_weather.setObjectName("checkBox_i2c1602_show_weather")
        self.gridLayout_9.addWidget(self.checkBox_i2c1602_show_weather, 1, 1, 1, 1)
        self.checkBox_i2c1602_show_moisure = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox_i2c1602_show_moisure.setObjectName("checkBox_i2c1602_show_moisure")
        self.gridLayout_9.addWidget(self.checkBox_i2c1602_show_moisure, 1, 0, 1, 1)
        self.checkBox_i2c1602_show_timer = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox_i2c1602_show_timer.setObjectName("checkBox_i2c1602_show_timer")
        self.gridLayout_9.addWidget(self.checkBox_i2c1602_show_timer, 3, 0, 1, 1)
        self.checkBox_i2c1602_show_clock = QtWidgets.QCheckBox(self.widget_3)
        self.checkBox_i2c1602_show_clock.setObjectName("checkBox_i2c1602_show_clock")
        self.gridLayout_9.addWidget(self.checkBox_i2c1602_show_clock, 3, 1, 1, 1)
        self.gridLayout_7.addWidget(self.widget_3, 3, 0, 1, 1)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.textEdit_i2c1602_send_text = QtWidgets.QTextEdit(self.widget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_i2c1602_send_text.sizePolicy().hasHeightForWidth())
        self.textEdit_i2c1602_send_text.setSizePolicy(sizePolicy)
        self.textEdit_i2c1602_send_text.setMinimumSize(QtCore.QSize(0, 35))
        self.textEdit_i2c1602_send_text.setMaximumSize(QtCore.QSize(300, 40))
        self.textEdit_i2c1602_send_text.setStyleSheet("background-color:#fdfef9;")
        self.textEdit_i2c1602_send_text.setMidLineWidth(3)
        self.textEdit_i2c1602_send_text.setObjectName("textEdit_i2c1602_send_text")
        self.gridLayout_8.addWidget(self.textEdit_i2c1602_send_text, 0, 0, 1, 2)
        self.pushButton_i2c1602_send_text = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_i2c1602_send_text.setObjectName("pushButton_i2c1602_send_text")
        self.gridLayout_8.addWidget(self.pushButton_i2c1602_send_text, 1, 0, 1, 2)
        self.gridLayout_7.addWidget(self.widget_2, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.widget)
        self.line = QtWidgets.QFrame(self.widget_i2c1602)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.label = QtWidgets.QLabel(self.widget_i2c1602)
        self.label.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.gridLayout_2.addWidget(self.widget_i2c1602, 2, 1, 1, 1)
        self.widget_mosfet = QtWidgets.QWidget(self.widget_devices_subblock1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_mosfet.sizePolicy().hasHeightForWidth())
        self.widget_mosfet.setSizePolicy(sizePolicy)
        self.widget_mosfet.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_mosfet.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_mosfet.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_mosfet.setObjectName("widget_mosfet")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_mosfet)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_13 = QtWidgets.QWidget(self.widget_mosfet)
        self.widget_13.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_13.setObjectName("widget_13")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.widget_13)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.widget_24 = QtWidgets.QWidget(self.widget_13)
        self.widget_24.setObjectName("widget_24")
        self.gridLayout_14 = QtWidgets.QGridLayout(self.widget_24)
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.horizontalSlider_pwm_duty_cycle = QtWidgets.QSlider(self.widget_24)
        self.horizontalSlider_pwm_duty_cycle.valueChanged.connect(self.change_pwm_value)
        self.horizontalSlider_pwm_duty_cycle.setRange(0, 255)
        self.horizontalSlider_pwm_duty_cycle.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_pwm_duty_cycle.setObjectName("horizontalSlider_pwm_duty_cycle")
        self.gridLayout_14.addWidget(self.horizontalSlider_pwm_duty_cycle, 0, 0, 1, 1)
        self.gridLayout_13.addWidget(self.widget_24, 1, 0, 1, 1)
        self.frame_pwm_oscilloscope = QtWidgets.QFrame(self.widget_13)
        self.frame_pwm_oscilloscope.setMinimumSize(QtCore.QSize(0, 90))
        self.frame_pwm_oscilloscope.setStyleSheet("background-color:rgb(90, 93, 92);\n"
"")
        self.frame_pwm_oscilloscope.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_pwm_oscilloscope.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pwm_oscilloscope.setLineWidth(2)
        self.frame_pwm_oscilloscope.setMidLineWidth(0)
        self.frame_pwm_oscilloscope.setObjectName("frame_pwm_oscilloscope")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_pwm_oscilloscope)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.widget_pwm_oscilloscope = PlotWidget(self.frame_pwm_oscilloscope)
        self.widget_pwm_oscilloscope.setObjectName("widget_pwm_oscilloscope")
        self.verticalLayout_9.addWidget(self.widget_pwm_oscilloscope)
        self.gridLayout_13.addWidget(self.frame_pwm_oscilloscope, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.widget_13)
        self.line_3 = QtWidgets.QFrame(self.widget_mosfet)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.label_3 = QtWidgets.QLabel(self.widget_mosfet)
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.gridLayout_2.addWidget(self.widget_mosfet, 2, 3, 1, 1)
        self.widget_symbolik4x7digit = QtWidgets.QWidget(self.widget_devices_subblock1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_symbolik4x7digit.sizePolicy().hasHeightForWidth())
        self.widget_symbolik4x7digit.setSizePolicy(sizePolicy)
        self.widget_symbolik4x7digit.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_symbolik4x7digit.setMaximumSize(QtCore.QSize(330, 330))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.widget_symbolik4x7digit.setFont(font)
        self.widget_symbolik4x7digit.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_symbolik4x7digit.setObjectName("widget_symbolik4x7digit")
        self.gridLayout_24 = QtWidgets.QGridLayout(self.widget_symbolik4x7digit)
        self.gridLayout_24.setObjectName("gridLayout_24")
        self.label_4 = QtWidgets.QLabel(self.widget_symbolik4x7digit)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_24.addWidget(self.label_4, 4, 0, 1, 1)
        self.line_4 = QtWidgets.QFrame(self.widget_symbolik4x7digit)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.gridLayout_24.addWidget(self.line_4, 3, 0, 1, 1)
        self.widget_28 = QtWidgets.QWidget(self.widget_symbolik4x7digit)
        self.widget_28.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_28.setObjectName("widget_28")
        self.gridLayout_23 = QtWidgets.QGridLayout(self.widget_28)
        self.gridLayout_23.setObjectName("gridLayout_23")
        self.widget_11 = QtWidgets.QWidget(self.widget_28)
        self.widget_11.setStyleSheet("background-color: rgb(213, 209, 202);")
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lcdNumber_symb_disp1 = QtWidgets.QLCDNumber(self.widget_11)
        self.lcdNumber_symb_disp1.setStyleSheet("color: rgb(207, 227, 255);\n"
"background-color:#464847;")
        self.lcdNumber_symb_disp1.setDigitCount(1)
        self.lcdNumber_symb_disp1.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_symb_disp1.setObjectName("lcdNumber_symb_disp1")
        self.horizontalLayout.addWidget(self.lcdNumber_symb_disp1)
        self.lcdNumber_symb_disp2 = QtWidgets.QLCDNumber(self.widget_11)
        self.lcdNumber_symb_disp2.setStyleSheet("color: rgb(207, 227, 255);\n"
"background-color:#464847;")
        self.lcdNumber_symb_disp2.setDigitCount(1)
        self.lcdNumber_symb_disp2.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_symb_disp2.setObjectName("lcdNumber_symb_disp2")
        self.horizontalLayout.addWidget(self.lcdNumber_symb_disp2)
        self.lcdNumber_symb_disp3 = QtWidgets.QLCDNumber(self.widget_11)
        self.lcdNumber_symb_disp3.setStyleSheet("color: rgb(207, 227, 255);\n"
"background-color:#464847;")
        self.lcdNumber_symb_disp3.setDigitCount(1)
        self.lcdNumber_symb_disp3.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_symb_disp3.setObjectName("lcdNumber_symb_disp3")
        self.horizontalLayout.addWidget(self.lcdNumber_symb_disp3)
        self.lcdNumber_symb_disp4 = QtWidgets.QLCDNumber(self.widget_11)
        self.lcdNumber_symb_disp4.setStyleSheet("color: rgb(207, 227, 255);\n"
"background-color:#464847;")
        self.lcdNumber_symb_disp4.setDigitCount(1)
        self.lcdNumber_symb_disp4.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.lcdNumber_symb_disp4.setObjectName("lcdNumber_symb_disp4")
        self.horizontalLayout.addWidget(self.lcdNumber_symb_disp4)
        self.gridLayout_23.addWidget(self.widget_11, 0, 0, 1, 1)
        self.radioButton_symb_disp_show_timer = QtWidgets.QRadioButton(self.widget_28)
        self.radioButton_symb_disp_show_timer.clicked.connect(self.display_4x7digit)               # oновлюємо значення
        self.radioButton_symb_disp_show_timer.setObjectName("radioButton_symb_disp_show_timer")
        self.gridLayout_23.addWidget(self.radioButton_symb_disp_show_timer, 1, 0, 1, 1)
        self.radioButton_symb_disp_show_clock = QtWidgets.QRadioButton(self.widget_28)
        self.radioButton_symb_disp_show_clock.setChecked(True)                             # увімкнено за замовчуванням
        self.radioButton_symb_disp_show_clock.clicked.connect(self.display_4x7digit)               # oновлюємо значення
        self.radioButton_symb_disp_show_clock.setObjectName("radioButton_symb_disp_show_clock")
        self.gridLayout_23.addWidget(self.radioButton_symb_disp_show_clock, 2, 0, 1, 1)
        self.gridLayout_24.addWidget(self.widget_28, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_symbolik4x7digit, 2, 7, 1, 1)
        self.widget_matrix8x8 = QtWidgets.QWidget(self.widget_devices_subblock1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_matrix8x8.sizePolicy().hasHeightForWidth())
        self.widget_matrix8x8.setSizePolicy(sizePolicy)
        self.widget_matrix8x8.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_matrix8x8.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_matrix8x8.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_matrix8x8.setObjectName("widget_matrix8x8")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_matrix8x8)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.widget_23 = QtWidgets.QWidget(self.widget_matrix8x8)
        self.widget_23.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_23.setObjectName("widget_23")
        self.gridLayout_18 = QtWidgets.QGridLayout(self.widget_23)
        self.gridLayout_18.setObjectName("gridLayout_18")
        self.widget_9 = QtWidgets.QWidget(self.widget_23)
        self.widget_9.setObjectName("widget_9")
        self.gridLayout_22 = QtWidgets.QGridLayout(self.widget_9)
        self.gridLayout_22.setObjectName("gridLayout_22")
        self.pushButton_matrix8x8_send = QtWidgets.QPushButton(self.widget_9)
        self.pushButton_matrix8x8_send.clicked.connect(self.matrix_8x8)
        self.pushButton_matrix8x8_send.setObjectName("pushButton_matrix8x8_send")
        self.gridLayout_22.addWidget(self.pushButton_matrix8x8_send, 0, 0, 1, 1)
        self.gridLayout_18.addWidget(self.widget_9, 2, 0, 1, 1)
        self.widget_29 = QtWidgets.QWidget(self.widget_23)
        self.widget_29.setObjectName("widget_29")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_29)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_matrix8x8 = QtWidgets.QTextEdit(self.widget_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_matrix8x8.sizePolicy().hasHeightForWidth())
        self.textEdit_matrix8x8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(50)
        self.textEdit_matrix8x8.setFont(font)
        self.textEdit_matrix8x8.setStyleSheet("background-color: rgb(213, 209, 202);")
        self.textEdit_matrix8x8.setObjectName("textEdit_matrix8x8")
        self.verticalLayout.addWidget(self.textEdit_matrix8x8)
        self.gridLayout_18.addWidget(self.widget_29, 1, 0, 1, 1)
        self.verticalLayout_8.addWidget(self.widget_23)
        self.line_2 = QtWidgets.QFrame(self.widget_matrix8x8)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_8.addWidget(self.line_2)
        self.label_2 = QtWidgets.QLabel(self.widget_matrix8x8)
        self.label_2.setMinimumSize(QtCore.QSize(137, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_8.addWidget(self.label_2)
        self.gridLayout_2.addWidget(self.widget_matrix8x8, 2, 5, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 330, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_2.addItem(spacerItem8, 2, 0, 1, 1)
        self.gridLayout_6.addWidget(self.widget_devices_subblock1, 0, 1, 1, 1)
        self.widget_devices_subblock2 = QtWidgets.QWidget(self.widget_devices_block)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_devices_subblock2.sizePolicy().hasHeightForWidth())
        self.widget_devices_subblock2.setSizePolicy(sizePolicy)
        self.widget_devices_subblock2.setMaximumSize(QtCore.QSize(3000, 3000))
        self.widget_devices_subblock2.setObjectName("widget_devices_subblock2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_devices_subblock2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem9 = QtWidgets.QSpacerItem(369, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem9, 0, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem10, 0, 1, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(369, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem11, 0, 2, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem12, 0, 3, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(368, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem13, 0, 4, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem14, 0, 5, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(369, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem15, 0, 6, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(120, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem16, 0, 7, 1, 1)
        spacerItem17 = QtWidgets.QSpacerItem(20, 330, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout_3.addItem(spacerItem17, 1, 7, 1, 1)
        self.widget_rain_sensor = QtWidgets.QWidget(self.widget_devices_subblock2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_rain_sensor.sizePolicy().hasHeightForWidth())
        self.widget_rain_sensor.setSizePolicy(sizePolicy)
        self.widget_rain_sensor.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_rain_sensor.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_rain_sensor.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_rain_sensor.setObjectName("widget_rain_sensor")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_rain_sensor)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_15 = QtWidgets.QWidget(self.widget_rain_sensor)
        self.widget_15.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_15.setObjectName("widget_15")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.widget_15)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.widget_7 = QtWidgets.QWidget(self.widget_15)
        self.widget_7.setObjectName("widget_7")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.widget_7)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_678 = QtWidgets.QLabel(self.widget_7)
        self.label_678.setObjectName("label_678")
        self.gridLayout_11.addWidget(self.label_678, 0, 0, 1, 1)
        self.progressBar_rain_sens_level = QtWidgets.QProgressBar(self.widget_7)
        font = QtGui.QFont()
        font.setKerning(True)
        self.progressBar_rain_sens_level.setFont(font)
        self.progressBar_rain_sens_level.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.progressBar_rain_sens_level.setStyleSheet("QProgressBar{\n"
"    background-color: #fdfef9;\n"
";\n"
"    border-style: solid;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar::chunk{\n"
"    background-color:rgb(0, 122, 217);\n"
"    border-radius: 10px;\n"
"}")
        self.progressBar_rain_sens_level.setProperty("value", 0)
        self.progressBar_rain_sens_level.setObjectName("progressBar_rain_sens_level")
        self.gridLayout_11.addWidget(self.progressBar_rain_sens_level, 1, 0, 1, 1)
        self.gridLayout_10.addWidget(self.widget_7, 0, 0, 1, 1)
        self.widget_6 = QtWidgets.QWidget(self.widget_15)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_12.addItem(spacerItem18, 1, 1, 1, 1)
        self.label_rain_sens_status_icon = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_rain_sens_status_icon.sizePolicy().hasHeightForWidth())
        self.label_rain_sens_status_icon.setSizePolicy(sizePolicy)
        self.label_rain_sens_status_icon.setMinimumSize(QtCore.QSize(40, 40))
        self.label_rain_sens_status_icon.setMaximumSize(QtCore.QSize(40, 40))
        self.label_rain_sens_status_icon.setText("")
        self.label_rain_sens_status_icon.setScaledContents(True)
        self.label_rain_sens_status_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_rain_sens_status_icon.setObjectName("label_rain_sens_status_icon")
        self.gridLayout_12.addWidget(self.label_rain_sens_status_icon, 1, 2, 1, 1)
        self.checkBox_rain_sens_connect_to_relay = QtWidgets.QCheckBox(self.widget_6)
        self.checkBox_rain_sens_connect_to_relay.setObjectName("checkBox_rain_sens_connect_to_relay")
        self.gridLayout_12.addWidget(self.checkBox_rain_sens_connect_to_relay, 1, 0, 1, 1)
        self.gridLayout_10.addWidget(self.widget_6, 1, 0, 1, 1)
        self.verticalLayout_4.addWidget(self.widget_15)
        self.line_7 = QtWidgets.QFrame(self.widget_rain_sensor)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_4.addWidget(self.line_7)
        self.label_7 = QtWidgets.QLabel(self.widget_rain_sensor)
        self.label_7.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.gridLayout_3.addWidget(self.widget_rain_sensor, 1, 0, 1, 1)
        self.widget_relay = QtWidgets.QWidget(self.widget_devices_subblock2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_relay.sizePolicy().hasHeightForWidth())
        self.widget_relay.setSizePolicy(sizePolicy)
        self.widget_relay.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_relay.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_relay.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_relay.setObjectName("widget_relay")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_relay)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_17 = QtWidgets.QWidget(self.widget_relay)
        self.widget_17.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_17.setObjectName("widget_17")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.widget_17)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.pushButton_relay_timer_stop = QtWidgets.QPushButton(self.widget_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_relay_timer_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_relay_timer_stop.setSizePolicy(sizePolicy)
        self.pushButton_relay_timer_stop.clicked.connect(self.stop_timer)
        self.pushButton_relay_timer_stop.setObjectName("pushButton_relay_timer_stop")
        self.gridLayout_16.addWidget(self.pushButton_relay_timer_stop, 6, 2, 1, 1)
        self.horizontalSlider_relay_timer_value = QtWidgets.QSlider(self.widget_17)
        self.horizontalSlider_relay_timer_value.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_relay_timer_value.valueChanged.connect(self.update_timer_value)
        self.horizontalSlider_relay_timer_value.setObjectName("horizontalSlider_relay_timer_value")
        self.gridLayout_16.addWidget(self.horizontalSlider_relay_timer_value, 4, 0, 1, 3)
        self.lcdNumber_relay_timer = QtWidgets.QLCDNumber(self.widget_17)
        self.lcdNumber_relay_timer.setMinimumSize(QtCore.QSize(0, 25))
        self.lcdNumber_relay_timer.setObjectName("lcdNumber_relay_timer")
        self.gridLayout_16.addWidget(self.lcdNumber_relay_timer, 5, 0, 1, 3)
        self.radioButton_relay_on = QtWidgets.QRadioButton(self.widget_17)
        self.radioButton_relay_on.setObjectName("radioButton_relay_on")
        self.gridLayout_16.addWidget(self.radioButton_relay_on, 0, 0, 1, 1)
        self.radioButton_relay_off = QtWidgets.QRadioButton(self.widget_17)
        self.radioButton_relay_off.setChecked(True)                                          # вибрано за замовчуванням
        self.radioButton_relay_off.setObjectName("radioButton_relay_off")
        self.gridLayout_16.addWidget(self.radioButton_relay_off, 2, 0, 1, 1)
        self.radioButton_relay_timer = QtWidgets.QRadioButton(self.widget_17)
        self.radioButton_relay_timer.setObjectName("radioButton_relay_timer")
        self.gridLayout_16.addWidget(self.radioButton_relay_timer, 0, 2, 1, 1)
        self.pushButton_relay_timer_start = QtWidgets.QPushButton(self.widget_17)
        self.pushButton_relay_timer_start.clicked.connect(self.start_timer)                # пуск/пауза відліку таймера
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_relay_timer_start.sizePolicy().hasHeightForWidth())
        self.pushButton_relay_timer_start.setSizePolicy(sizePolicy)
        self.pushButton_relay_timer_start.setObjectName("pushButton_relay_timer_start")
        self.gridLayout_16.addWidget(self.pushButton_relay_timer_start, 6, 0, 1, 1)
        self.radioButton_relay_side_in = QtWidgets.QRadioButton(self.widget_17)
        self.radioButton_relay_side_in.setObjectName("radioButton_relay_side_in")
        self.gridLayout_16.addWidget(self.radioButton_relay_side_in, 2, 2, 1, 1)
        self.verticalLayout_5.addWidget(self.widget_17)
        self.line_8 = QtWidgets.QFrame(self.widget_relay)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.verticalLayout_5.addWidget(self.line_8)
        self.label_8 = QtWidgets.QLabel(self.widget_relay)
        self.label_8.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.gridLayout_3.addWidget(self.widget_relay, 1, 2, 1, 1)
        self.widget_encoder = QtWidgets.QWidget(self.widget_devices_subblock2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_encoder.sizePolicy().hasHeightForWidth())
        self.widget_encoder.setSizePolicy(sizePolicy)
        self.widget_encoder.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_encoder.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_encoder.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_encoder.setObjectName("widget_encoder")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.widget_encoder)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_19 = QtWidgets.QWidget(self.widget_encoder)
        self.widget_19.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_19.setObjectName("widget_19")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_19)
        self.gridLayout.setObjectName("gridLayout")
        self.radioButton_connect_encoder_to_timer = QtWidgets.QRadioButton(self.widget_19)
        self.radioButton_connect_encoder_to_timer.setChecked(True)                           # вибрано за замовчуванням
        self.radioButton_connect_encoder_to_timer.setObjectName("radioButton_connect_encoder_to_timer")
        self.gridLayout.addWidget(self.radioButton_connect_encoder_to_timer, 2, 0, 1, 1)
        self.radioButton_connect_encoder_to_pwm = QtWidgets.QRadioButton(self.widget_19)
        self.radioButton_connect_encoder_to_pwm.setObjectName("radioButton_connect_encoder_to_pwm")
        self.gridLayout.addWidget(self.radioButton_connect_encoder_to_pwm, 2, 1, 1, 1)
        self.dial_encoder = QtWidgets.QDial(self.widget_19)
        self.dial_encoder.valueChanged.connect(lambda: self.dial_move())                           # під'єднуємо дайлер
        self.dial_encoder.setStyleSheet("background-color:#fdfef9;")
        self.dial_encoder.setObjectName("dial_encoder")
        self.gridLayout.addWidget(self.dial_encoder, 1, 0, 1, 2)
        self.verticalLayout_6.addWidget(self.widget_19)
        self.line_5 = QtWidgets.QFrame(self.widget_encoder)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_6.addWidget(self.line_5)
        self.label_5 = QtWidgets.QLabel(self.widget_encoder)
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.gridLayout_3.addWidget(self.widget_encoder, 1, 4, 1, 1)
        self.widget_moisture_sensor = QtWidgets.QWidget(self.widget_devices_subblock2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_moisture_sensor.sizePolicy().hasHeightForWidth())
        self.widget_moisture_sensor.setSizePolicy(sizePolicy)
        self.widget_moisture_sensor.setMinimumSize(QtCore.QSize(150, 105))
        self.widget_moisture_sensor.setMaximumSize(QtCore.QSize(330, 330))
        self.widget_moisture_sensor.setStyleSheet("background-color:rgb(182, 179, 174);")
        self.widget_moisture_sensor.setObjectName("widget_moisture_sensor")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_moisture_sensor)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_21 = QtWidgets.QWidget(self.widget_moisture_sensor)
        self.widget_21.setMinimumSize(QtCore.QSize(0, 138))
        self.widget_21.setObjectName("widget_21")
        self.gridLayout_21 = QtWidgets.QGridLayout(self.widget_21)
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.label_moisture_relay_en_level = QtWidgets.QLabel(self.widget_21)
        self.label_moisture_relay_en_level.setObjectName("label_moisture_relay_en_level")
        self.gridLayout_21.addWidget(self.label_moisture_relay_en_level, 4, 0, 1, 1)
        self.widget_27 = QtWidgets.QWidget(self.widget_21)
        self.widget_27.setMinimumSize(QtCore.QSize(65, 65))
        self.widget_27.setObjectName("widget_27")
        self.gridLayout_25 = QtWidgets.QGridLayout(self.widget_27)
        self.gridLayout_25.setObjectName("gridLayout_25")
        self.progressBar_moisture_level = QtWidgets.QProgressBar(self.widget_27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_moisture_level.sizePolicy().hasHeightForWidth())
        self.progressBar_moisture_level.setSizePolicy(sizePolicy)
        self.progressBar_moisture_level.setMaximumSize(QtCore.QSize(130, 16777215))
        self.progressBar_moisture_level.setStyleSheet("QProgressBar{\n"
"    background-color:#fdfef9;\n"
"    border-style: solid;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"    background-color:rgb(36, 160, 217);\n"
"}")
        self.progressBar_moisture_level.setProperty("value", 0)
        self.progressBar_moisture_level.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_moisture_level.setObjectName("progressBar_moisture_level")
        self.gridLayout_25.addWidget(self.progressBar_moisture_level, 0, 0, 1, 1)
        self.gridLayout_21.addWidget(self.widget_27, 0, 0, 1, 3)
        self.horizontalSlider_moisture_relay_en_level = QtWidgets.QSlider(self.widget_21)
        self.horizontalSlider_moisture_relay_en_level.valueChanged.connect(self.relay_by_moisture_slider)
        self.horizontalSlider_moisture_relay_en_level.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_moisture_relay_en_level.setObjectName("horizontalSlider_moisture_relay_en_level")
        self.gridLayout_21.addWidget(self.horizontalSlider_moisture_relay_en_level, 3, 0, 1, 3)
        self.checkBox_connect_moisture_to_relay = QtWidgets.QCheckBox(self.widget_21)
        self.checkBox_connect_moisture_to_relay.setText("")
        self.checkBox_connect_moisture_to_relay.setObjectName("checkBox_connect_moisture_to_relay")
        self.gridLayout_21.addWidget(self.checkBox_connect_moisture_to_relay, 4, 2, 1, 1)
        self.verticalLayout_7.addWidget(self.widget_21)
        self.line_6 = QtWidgets.QFrame(self.widget_moisture_sensor)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_7.addWidget(self.line_6)
        self.label_6 = QtWidgets.QLabel(self.widget_moisture_sensor)
        self.label_6.setMinimumSize(QtCore.QSize(137, 0))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.gridLayout_3.addWidget(self.widget_moisture_sensor, 1, 6, 1, 1)
        self.gridLayout_6.addWidget(self.widget_devices_subblock2, 1, 1, 1, 1)
        self.gridLayout_19.addWidget(self.widget_devices_block, 0, 1, 1, 1)
        self.serial = QSerialPort()                                 # створюємо порт об'єкт serial
        self.serial.setBaudRate(9600)                               # задаємо швидкість
        MainWindow.setCentralWidget(self.centralwidget)
        self.update_clock_timer = QTimer()
        self.update_clock_timer.timeout.connect(self.clock_update)
        self.update_clock_timer.start(60000)
        self.update_lcd1602_timer = QTimer()
        self.update_lcd1602_timer.timeout.connect(self.lcd1602_cycle)
        self.update_lcd1602_timer.start(3000)

        self.timer_thread = MyTimerThread(mainwindow=self)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.pushButton_com_port_connect.setText(_translate("MainWindow", "Встановити з\'єднання"))
        self.pushButton_com_port_disconnect.setText(_translate("MainWindow", "Роз\'єднати"))
        self.label_com_port_number.setText(_translate("MainWindow", "COM1"))
        self.label_log.setText(_translate("MainWindow", "  log"))
        self.label_arduino_connection_status.setText(_translate("MainWindow", "connected"))
        self.checkBox_i2c1602_show_log.setText(_translate("MainWindow", "log"))
        self.checkBox_i2c1602_show_pwm.setText(_translate("MainWindow", "ШІМ"))
        self.checkBox_i2c1602_show_weather.setText(_translate("MainWindow", "Погода"))
        self.checkBox_i2c1602_show_moisure.setText(_translate("MainWindow", "Грунт"))
        self.checkBox_i2c1602_show_timer.setText(_translate("MainWindow", "timer"))
        self.checkBox_i2c1602_show_clock.setText(_translate("MainWindow", "Годинник"))
        self.pushButton_i2c1602_send_text.setText(_translate("MainWindow", "Відправити"))
        self.label.setText(_translate("MainWindow", "Дисплей  I2C1602"))
        self.label_3.setText(_translate("MainWindow", "ШІМ  Mosfet module"))
        self.label_4.setText(_translate("MainWindow", "Символьний дисплей 4х7digit"))
        self.radioButton_symb_disp_show_timer.setText(_translate("MainWindow", "Вивести timer"))
        self.radioButton_symb_disp_show_clock.setText(_translate("MainWindow", "Годинник"))
        self.pushButton_matrix8x8_send.setText(_translate("MainWindow", "Відправити"))
        self.label_2.setText(_translate("MainWindow", "Матриця 8х8  MAX7219 "))
        self.label_678.setText(_translate("MainWindow", "Поточна вологість"))
        self.checkBox_rain_sens_connect_to_relay.setText(_translate("MainWindow", "Реле"))
        self.label_7.setText(_translate("MainWindow", "Датчик дощу"))
        self.pushButton_relay_timer_stop.setText(_translate("MainWindow", "Стоп"))
        self.radioButton_relay_on.setText(_translate("MainWindow", "On"))
        self.radioButton_relay_off.setText(_translate("MainWindow", "Off"))
        self.radioButton_relay_timer.setText(_translate("MainWindow", "Timer"))
        self.pushButton_relay_timer_start.setText(_translate("MainWindow", "Старт"))
        self.radioButton_relay_side_in.setText(_translate("MainWindow", "Вхід"))
        self.label_8.setText(_translate("MainWindow", "Реле"))
        self.radioButton_connect_encoder_to_timer.setText(_translate("MainWindow", "Timer"))
        self.radioButton_connect_encoder_to_pwm.setText(_translate("MainWindow", "ШІМ"))
        self.label_5.setText(_translate("MainWindow", "Енкодер"))
        self.label_moisture_relay_en_level.setText(_translate("MainWindow", "Старт поливу при"))
        self.label_6.setText(_translate("MainWindow", "Датчик вологості землі"))
        self.get_port_info()
        self.display_4x7digit()
        self.oscilloscope()

    def open_port(self):
        if self.port_is_connect:                                                       # перевіряємо чи вже не відкрито
            return                                                                             # зачиняємо
        self.serial.setPortName(self.comboBox_COM_ports.currentText())           # вибираєм поточний запис у комбобоксі
        self.serial.open(QIODevice.ReadWrite)                                                               # час на коректне відкриття порта
        self.add_to_log(f"{self.comboBox_COM_ports.currentText()} connected")                              # пишем у лог
        self.label_com_port_number.setText(self.comboBox_COM_ports.currentText())
        self.port_is_connect = True
        self.serial.readyRead.connect(self.read_port)                   # сигнал приєднання при наявності вхідних даних

    def read_port(self):                                                                                # зчитуємо дані
        try:
            self.input_data = str(self.serial.readLine(), 'utf-8').strip()                                 # форматуємо
        except Exception as ex:
            self.add_to_log('Exception ' + str(ex))
            self.close_port()

        if self.input_data:
            input_data = self.input_data.split(',')
            input_data_dict = self.input_data_dict.copy()
            for data in input_data:
                if len(data) > 2:
                    data = data.split(':')
                    if len(data[0]) == 1:
                        input_data_dict[data[0]] = data[1]
            if input_data_dict['1'] != self.input_data_dict['1']:
                self.input_data_dict['1'] = input_data_dict['1']
                self.arduino_encoder()
            if input_data_dict['2'] != self.input_data_dict['2']:
                self.input_data_dict['2'] = input_data_dict['2']
                self.moisture_sensor()
            if input_data_dict['3'] != self.input_data_dict['3']:
                self.input_data_dict['3'] = input_data_dict['3']
                self.rain_detector()

        if self.ready_to_write:
            self.send_to_port()
            self.ready_to_write = False

    def arduino_encoder(self):
        if self.input_data_dict["1"] == "2":
            if self.radioButton_connect_encoder_to_timer.isChecked():
                self.update_timer_value(self.current_timer + 2)
            elif self.radioButton_connect_encoder_to_pwm.isChecked():
                self.horizontalSlider_pwm_duty_cycle.setValue(self.pwm_value + 1)
        elif self.input_data_dict["1"] == "10":
            if self.radioButton_connect_encoder_to_timer.isChecked():
                self.update_timer_value(self.current_timer + 10)
            elif self.radioButton_connect_encoder_to_pwm.isChecked():
                self.horizontalSlider_pwm_duty_cycle.setValue(self.pwm_value + 5)
        elif self.input_data_dict["1"] == "-2":
            if self.radioButton_connect_encoder_to_timer.isChecked():
                self.update_timer_value(self.current_timer - 2)
            elif self.radioButton_connect_encoder_to_pwm.isChecked():
                self.horizontalSlider_pwm_duty_cycle.setValue(self.pwm_value - 1)
        elif self.input_data_dict["1"] == "-10":
            if self.radioButton_connect_encoder_to_timer.isChecked():
                self.update_timer_value(self.current_timer - 10)
            elif self.radioButton_connect_encoder_to_pwm.isChecked():
                self.horizontalSlider_pwm_duty_cycle.setValue(self.pwm_value - 5)
        elif self.input_data_dict["1"] == "99":
            if self.radioButton_connect_encoder_to_timer.isChecked():
                self.start_timer()
        self.input_data_dict["1"] = "0"

    def update_timer_value(self, value):                                               # функція зміни значення таймера
        if value >= 0:
            self.current_timer = value                                                               # оновлюємо таймер
            self.lcdNumber_relay_timer.display(value)
            self.horizontalSlider_relay_timer_value.setValue(value)
            # self.ready_to_write = True
            if self.radioButton_symb_disp_show_timer.isChecked():
                self.display_4x7digit()

    def send_to_port(self):
        send_string = ''
        for key, value in self.output_data_dict.items():
            if self.output_data_dict[key] != self.old_output_data_dict[key]:
                send_string = send_string + str(key) + ':' + str(value) + ','
        print(send_string)
        self.serial.write(send_string.encode())
        self.old_output_data_dict = self.output_data_dict.copy()

    def close_port(self):
        self.serial.close()
        if self.port_is_connect:
            self.add_to_log("disconnected")                                                                 # пишем у лог
            self.port_is_connect = False
            self.label_com_port_number.setText('')

    def get_port_info(self):                                                  # запускається у update_parameters_thread
        self.updated_ports = [port.portName() for port in QSerialPortInfo().availablePorts()]   # генеруємо list портів
        if self.ports != self.updated_ports:                                                  # виявляємо зміни в ports
            self.add_to_log('Device list changed')                                                       # пишем у лог
            self.comboBox_COM_ports.clear()
            self.ports = self.updated_ports
            self.first_port = self.ports[0]
            for port in self.ports:
                self.comboBox_COM_ports.addItem(port)                                # додаємо імена портів у комбобокс

    def add_to_log(self, item):                                                                  # функція запису у лог
        if self.logs_count > 0:                                                    # вирізаємо логи при старті програми
            self.current_log = str(datetime.now())[11: 19] + ' - ' + item
            self.listWidget.insertItem(0, self.current_log)
        self.logs_count += 1

    def display_4x7digit(self):
        if self.radioButton_symb_disp_show_clock.isChecked():
            current_time = str(datetime.now())
            self.lcdNumber_symb_disp1.display(current_time[11])
            self.lcdNumber_symb_disp2.display(current_time[12])
            self.lcdNumber_symb_disp3.display(current_time[14])
            self.lcdNumber_symb_disp4.display(current_time[15])
            self.output_data_dict['3'] = current_time[11:13] + current_time[14:16]
            self.ready_to_write = True
        elif self.radioButton_symb_disp_show_timer.isChecked():
            self.lcdNumber_symb_disp1.display(self.current_timer // 1000 % 10)
            self.lcdNumber_symb_disp2.display(self.current_timer // 100 % 10)
            self.lcdNumber_symb_disp3.display(self.current_timer // 10 % 10)
            self.lcdNumber_symb_disp4.display(self.current_timer % 10)
            self.output_data_dict['3'] = self.current_timer
            self.ready_to_write = True

    def clock_update(self):
        if self.radioButton_symb_disp_show_clock.isChecked():
            self.display_4x7digit()

    def start_timer(self):
        if self.timer_is_running:                                                          # робимо кнопку бістабільною
            self.stop_timer()                                                # повторний виклик "старт" працює як пауза
            self.add_to_log(f' {self.current_timer}s')
        else:
            self.timer_is_running = True                                       # якщо таймер вимкнуто просто запускаємо
            self.timer_thread.start()
            self.add_to_log(f'Timer "Start"  {self.current_timer}s')

    def stop_timer(self):
        if not self.timer_is_running:                                                            # якщо таймер вимкнуто
            self.current_timer = 0                                                 # виклик спрацює на скидання таймера
            self.lcdNumber_relay_timer.display(self.current_timer)
            self.add_to_log('Timer cleared')
            self.horizontalSlider_relay_timer_value.setValue(0)
        else:
            self.timer_is_running = False                                                      # зупиняємо тред таймера
            self.add_to_log('Timer "Stop"')

    def dial_move(self):                                                             # робота дайлера в режимі енкодера
        value = self.dial_encoder.value()
        if self.radioButton_connect_encoder_to_timer.isChecked():
            if self.current_encoder_position > value:
                self.update_timer_value(self.current_timer - 1)
            else:
                self.update_timer_value(self.current_timer + 1)
            self.current_encoder_position = value
        elif self.radioButton_connect_encoder_to_pwm.isChecked():
            if self.current_encoder_position > value:
                self.pwm_value -= 1 if self.pwm_value > 1 else 0
                self.current_encoder_position = value
            else:
                self.pwm_value += 1 if self.pwm_value < 256 else 0
                self.current_encoder_position = value
            self.horizontalSlider_pwm_duty_cycle.setValue(self.pwm_value)

    def relay_by_moisture_slider(self, value):
        self.label_moisture_relay_en_level.setText(f'Полив при {value}%')
        if value < self.moisture_value and self.checkBox_connect_moisture_to_relay.isChecked():
            if self.radioButton_relay_side_in.isChecked():
                self.relay_is_active = True

    def moisture_sensor(self):
        self.moisture_value = int(int(self.input_data_dict['2']) / 1024 * 100)
        self.progressBar_moisture_level.setValue(self.moisture_value)

    def rain_detector(self):
        self.rain_detector_value = 100 - int(int(self.input_data_dict['3']) / 1024 * 100)
        self.progressBar_rain_sens_level.setValue(self.rain_detector_value)
        if self.rain_detector_value >= 60:
            self.label_rain_sens_status_icon.setPixmap(QtGui.QPixmap(f"{self.current_path}/rain.png"))
            self.weather_status = "rainy"
        if self.rain_detector_value <= 20:
            self.label_rain_sens_status_icon.setPixmap(QtGui.QPixmap(f"{self.current_path}/sun.png"))
            self.weather_status = "sunny"
        if self.rain_detector_value > 20 and self.rain_detector_value < 60:
            self.label_rain_sens_status_icon.setPixmap(QtGui.QPixmap(f"{self.current_path}/cloud.png"))
            self.weather_status = "cloudy"

    def matrix_8x8(self):
        self.output_data_dict['4'] = self.textEdit_matrix8x8.toPlainText()
        self.ready_to_write = True

    def change_pwm_value(self, value):
        self.pwm_value = value
        self.output_data_dict["6"] = self.pwm_value
        self.oscilloscope()
        self.ready_to_write = True

    def oscilloscope(self):
        if self.pwm_value < 20:
            self.widget_pwm_oscilloscope.clear()
            self.widget_pwm_oscilloscope.plot([1, 2, 5, 5, 5, 5, 6, 7, 8, 10, 10, 10, 11, 12, 14, 15, 15, 15, 16],
                                              [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0])
        if 20 < self.pwm_value < 80:
            self.widget_pwm_oscilloscope.clear()
            self.widget_pwm_oscilloscope.plot([1, 2, 4, 4, 5, 5, 5, 7, 9, 9, 10, 10, 11, 12, 14, 14, 15, 15, 16],
                                              [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0])
        if 80 < self.pwm_value < 140:
            self.widget_pwm_oscilloscope.clear()
            self.widget_pwm_oscilloscope.plot([1, 3, 3, 4, 5, 5, 6, 8, 8, 9, 10, 10, 11, 13, 13, 14, 15, 15, 16],
                                              [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0])
        if 140 < self.pwm_value < 200:
            self.widget_pwm_oscilloscope.clear()
            self.widget_pwm_oscilloscope.plot([1, 2, 2, 3, 4, 5, 5, 7, 7, 8, 9, 10, 10, 12, 12, 13, 14, 15, 15, 16],
                                              [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0])
        if 200 < self.pwm_value < 256:
            self.widget_pwm_oscilloscope.clear()
            self.widget_pwm_oscilloscope.plot(
                [0.1, 0.5, 0.5, 2, 3, 4, 5, 5, 5.5, 5.5, 7,  8,  9, 10, 10, 10.5, 10.5, 12, 13, 15, 15, 16],
                [0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0])

    def lcd1602_cycle(self):
        message_list = []
        if self.checkBox_i2c1602_show_clock.isChecked():
            time = str(datetime.now())
            message_list.append("Date " + time[0:11] + "Time  " + time[11:16])
        if self.checkBox_i2c1602_show_log.isChecked():
            message_list.append(self.current_log)
        if self.checkBox_i2c1602_show_moisure.isChecked():
            message_list.append("Moisture sensor level " + str(self.moisture_value) + "%")
        if self.checkBox_i2c1602_show_pwm.isChecked():
            message_list.append("Pwm duty cycle        " + str(int(self.pwm_value / 256 * 100 // 1)) + "%")
        if self.checkBox_i2c1602_show_timer.isChecked():
            message_list.append("Timer             " + str(self.current_timer) + "s")
        if self.checkBox_i2c1602_show_weather.isChecked():
            message_list.append("The weather is " + self.weather_status)
        if len(message_list) > self.lcd1602_cycle_count:
            self.output_data_dict['1'] = message_list[self.lcd1602_cycle_count][0:15]
            self.output_data_dict['2'] = message_list[self.lcd1602_cycle_count][15:]
            self.ready_to_write = True
        else:
            self.lcd1602_cycle_count = -1
        if self.lcd1602_cycle_count > 6:
            self.lcd1602_cycle_count = -1
        self.lcd1602_cycle_count += 1
        print(self.output_data_dict)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
