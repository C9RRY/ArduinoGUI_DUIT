import time
from PyQt5 import QtCore


class MyTimerThread(QtCore.QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        while self.mainwindow.current_timer > 0 and self.mainwindow.timer_is_running:
            time.sleep(1)
            if self.mainwindow.timer_is_running:
                self.mainwindow.current_timer -= 1
                self.mainwindow.lcdNumber_relay_timer.display(self.mainwindow.current_timer)
                if self.mainwindow.radioButton_symb_disp_show_timer.isChecked():
                    self.mainwindow.display_4x7digit()
                self.mainwindow.horizontalSlider_relay_timer_value.setValue(self.mainwindow.current_timer)
            elif self.mainwindow.current_timer < 0:
                self.mainwindow.add_to_log('таймер час вичерпано')