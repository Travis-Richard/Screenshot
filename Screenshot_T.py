#!/usr/bin/python3
'''venv/bin/python3 Screenshot.py &'''
# This application takes a selection of checkboxes and saves the selected screens to aodsnapshots
# Travis' File


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QMessageBox, \
    QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from datetime import datetime
import os
import time


class Screenshot(QWidget):

    def __init__(self, parent = None):
        # initializing widget layout
        super(Screenshot, self).__init__(parent)
        # initial list of checkbox titles
        self.cb_list = ['Trip Information', 'Alarm Handler', 'First Fault', 'First Quadrant',
                     'Storage Ring RF', 'B1400', 'XRMS_ID1', 'XRMS_ID2']
        self.window_title = ['Trip Information Checklist',
                'Control System Studio',
                'Storage Ring Amplifier FFM',
                'First Quadrant',
                'RF OPI',
                'B1400-00_monitor',
                'XRMS_ID1',
                'XRMS_ID2']

        self.comb_win_title = list(map(list, zip(self.cb_list, self.window_title)))

        grid = QGridLayout()

        for i, v in enumerate (self.cb_list):
            # iterating over cb_list to add title to checkboxes in a grid layout
            self.cb_list[i] = QCheckBox(v)
            self.cb_list[i].setChecked(False)
            grid.addWidget(self.cb_list[i], i, 0)
        # adding buttons to widget, saving screens and clearing selection
        self.sbtn = QPushButton('Save Selected Screenshots', self)
        self.sbtn.clicked.connect(self.saveScreen)
        self.ebtn = QPushButton('Clear Selected Screens', self)
        self.ebtn.clicked.connect(self.clearScreen)
        self.srtbtn = QPushButton('Select Storage Ring Trip Screens', self)
        self.srtbtn.clicked.connect(self.selectStorageRingTrip)
        grid.addWidget(self.sbtn, 10, 0)
        grid.addWidget(self.ebtn, 10, 1)
        grid.addWidget(self.srtbtn, 11, 0)
        self.setLayout(grid)

        # setting window properties
        self.setGeometry(300, 300, 300, 220)  # Window location 1, 2 window size 3, 4
        self.setWindowTitle('Screenshot')
        self.setWindowIcon(QIcon('scrn.png'))
        self.show()



    def saveScreen(self):
        # Overall function is to append titles of checkboxes to a list if those boxes are selected
        # Set empty lists
        self.cb_list_comb = []
        self.cb_list_bool = []
        self.cb_list_text = []
        self.scrn_list = []
        for i in self.cb_list:
            # add checked state and title to empty lists above
            self.cb_list_bool.append(i.isChecked())
            self.cb_list_text.append(i.text())
            # combine above lists into 1 list
            self.cb_list_comb = [(self.cb_list_bool[i], self.cb_list_text[i]) for i in range(0,
                                                        len(self.cb_list_bool))]

        for i, v in self.cb_list_comb:
            # check to see if box is checked, if so add title to scrn_list
            if i is True:
                self.scrn_list.append(v)
        # print(self.scrn_list)

        # Create an error message if no screens are selected
        if self.scrn_list == []:
            self.msg = QMessageBox()
            self.msg.setWindowTitle('Error')
            self.msg.setText('You did not select any screens to capture')
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.setGeometry(300, 450, 100, 100)
            self.msg.exec_()

        path = "/home/richart/AOD/Snapshots/"
        now = datetime.now()
        date = now.strftime('%m-%d-%Y_%H-%M-%S')

        # iterating over scrn_list to find and capture selected screens based on title
        for i in self.scrn_list:
            for v in range(0, len(self.comb_win_title)):
                if i in self.comb_win_title[v][0]:
                    file = path + "{}_{}.png".format(date, i.replace(" ", ""))
                    show_window = "wmctrl -a {}".format(self.comb_win_title[v][1].replace("'", ""))
                    screen_shot = "gnome-screenshot -w -f {}".format(file)
                    os.system(show_window)
                    os.system(screen_shot)
        # return to screenshot GUI
        os.system("wmctrl -a Screenshot")


        # clear lists to not repeat information
        self.cb_list_comb.clear()
        self.cb_list_text.clear()
        self.cb_list_bool.clear()
        self.scrn_list.clear()

    # clears all selections
    def clearScreen(self):
        for i in self.cb_list:
            i.setChecked(False)
    # Selects only screens used when storage ring trips
    def selectStorageRingTrip(self):
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
    scrn = Screenshot()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     scrn = Screenshot()
#     sys.exit(app.exec_())