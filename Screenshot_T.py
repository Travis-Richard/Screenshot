#!/usr/bin/python3
'''venv/bin/python3 Screenshot.py &'''
# This application takes a selection of checkboxes and saves the selected screens to /home/AOD/Snapshots
# Travis' File


import os
import subprocess
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QMessageBox, \
    QGridLayout, QTextBrowser


class Screenshot(QWidget):

    def __init__(self, parent=None):
        # initializing widget layout
        super(Screenshot, self).__init__(parent)

        self.path = "/home/richart/AOD/Snapshots/"
        # initial list of checkbox titles
        self.cb_list = ['Trip Information',
                        'Alarm Handler',
                        'First Fault',
                        'First Quadrant',
                        'Storage Ring RF',
                        'B1400',
                        'XRMS_ID1',
                        'XRMS_ID2']

        self.window_title = ['Trip Information Checklist',
                             'Control System Studio',
                             'Storage Ring Amplifier FFM',
                             'First Quadrant',
                             'RF OPI',
                             'B1400-00_monitor',
                             'XRMS_ID1',
                             'XRMS_ID2']

        self.comb_win_title = list(map(list, zip(self.cb_list, self.window_title)))
        self.cb_list_comb = []
        self.cb_list_bool = []
        self.cb_list_text = []
        self.scrn_list = []

        grid = QGridLayout()

        for i, v in enumerate(self.cb_list):
            # iterating over cb_list to add title to checkboxes in a grid layout
            self.cb_list[i] = QCheckBox(v)
            self.cb_list[i].setChecked(False)
            grid.addWidget(self.cb_list[i], i, 0)
        self.error_msg = QTextBrowser(self)
        grid.addWidget(self.error_msg, 0, 1, 9, 1)
        # adding buttons to widget, saving screens and clearing selection
        self.sbtn = QPushButton('Save Selected Screenshots', self)
        self.sbtn.clicked.connect(self.save_screen)
        self.ebtn = QPushButton('Clear Selected Screens', self)
        self.ebtn.clicked.connect(self.clear_screen)
        self.srtbtn = QPushButton('Select Storage Ring Trip Screens', self)
        self.srtbtn.clicked.connect(self.select_storage_ring_trip)
        grid.addWidget(self.sbtn, 10, 0)
        grid.addWidget(self.ebtn, 10, 1)
        grid.addWidget(self.srtbtn, 11, 0)
        self.setLayout(grid)

        # setting window properties
        self.setGeometry(300, 300, 500, 220)  # Window location 1, 2 window size 3, 4
        self.setWindowTitle('Screenshot')
        self.show()

    def save_screen(self):
        # Overall function is to append titles of checkboxes to a list if those boxes are selected
        # Set empty lists

        for i in self.cb_list:
            # add checked state and title to empty lists above
            self.cb_list_bool.append(i.isChecked())
            self.cb_list_text.append(i.text())
            # combine above lists into 1 list
            self.cb_list_comb = [(self.cb_list_bool[i], self.cb_list_text[i]) for i in range(0, len(self.cb_list_bool))]

        for i, v in self.cb_list_comb:
            # check to see if box is checked, if so add title to scrn_list
            if i is True:
                self.scrn_list.append(v)

        # Create an error message if no screens are selected
        if not self.scrn_list:
            self.msg = QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('You did not select any screens to capture')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.setGeometry(300, 450, 100, 100)
            self.msg.exec_()

        now = datetime.now()
        date = now.strftime('%m-%d-%Y_%H-%M-%S')

        cmd = "wmctrl -l | cut -d ' ' -f 5-"
        output = subprocess.check_output(cmd, shell=True).decode("utf-8").split("\n")
        # print(output)
        # iterating over scrn_list to find and capture selected screens based on title
        for i in self.scrn_list:
            for v in range(0, len(self.comb_win_title)):
                if i in self.comb_win_title[v][0]:
                    if any(self.comb_win_title[v][1] in z for z in output):
                        file = self.path + "{}_{}.png".format(date, i.replace(" ", ""))
                        show_window = "wmctrl -a {}".format(self.comb_win_title[v][1].replace("'", ""))
                        screen_shot = "gnome-screenshot -w -f {}".format(file)
                        os.system(show_window)
                        os.system(screen_shot)
                    else:
                        msg = '{} is not open'.format(self.comb_win_title[v][0])
                        self.error_msg.append(msg)

        # return to screenshot GUI
        os.system("wmctrl -a Screenshot")
        self.error_msg.append('Screenshots have been saved, please press Clear Selected Screens and select again')

        # clear lists to not repeat information
        self.cb_list_comb.clear()
        self.cb_list_text.clear()
        self.cb_list_bool.clear()
        self.scrn_list.clear()

    # clears all selections
    def clear_screen(self):
        for i in self.cb_list:
            i.setChecked(False)
        self.error_msg.clear()
        
    # Selects only screens used when storage ring trips
    def select_storage_ring_trip(self):
        for i in self.cb_list[0:5]:
            i.setChecked(True)


# Screen Names
# Trip Information - 0x15000a8 - Desktop 3 - Trip Info, 'Trip Information Checklist'
# First Fault - 0x037000a8 - Desktop 3 - Trip Info, 'Storage Ring Amplifier FFM'
# First Quadrant - 0x0390009a - Desktop 3 - Trip Info,
# '/home/control/opi/Interface/SRInterface/BPMC.edl'
# Alarm Handler - 0x00e002bc - Desktop -1 - Trip Info, 'Control System Studio (CLS)'
# Storage Ring RF - 0x06200007 - Desktop 2 - SR RF, 'RF OPI'
# B1400 - 0x0440000e - Desktop 7 - Orbit Control, 'B1400-00_monitor.stp Graph'
# XRMS1 - 0x0100000e - Desktop 4 - Facility, 'XRMS_ID1.stp Graph'
# XRMS2 - 0x011000e - Desktop 4 - Facility, 'XRMS_ID2.stp Graph'


def main():
    app = QApplication(sys.argv)
    window = Screenshot()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
