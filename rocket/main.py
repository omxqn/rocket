import random
import sys
import time
import threading
from ui import Ui_MainWindow
from PyQt5.Qt import *
from password_manager import PasswordDialog
# pip install PyQtChart


# pip install PyQtChart
data = {"speed": 0, "altitude": 0, "pressure": 0, "location": {"log": "0", "lat": "0"}}
launch_password = "alkalbani99"

def refresh():
    print("Updating")
    data["speed"] = random.randint(10, 2000)
    data["altitude"] = random.randint(10, 2000)
    data["pressure"] = random.randint(10, 2000)
    data["location"]["long"] = str(random.randint(10, 2000))
    data["location"]["lat"] = str(random.randint(10, 2000))


class MyForm(QMainWindow):
    def __init__(self):
        super(MyForm, self).__init__()

        self.timer = QTimer()  # Create a QTimer
        self.timer.timeout.connect(self.refresh)  # Connect timeout signal to update_speed slot
        self.timer.start(1000)  # Start the timer with an interval of 1000 milliseconds (1 second)

        self.main_wind()

        self.default_settings()
        print("started")

    def main_wind(self):
        QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.buttons()
        self.menu_bar()

    def menu_bar(self):
        self.menubar = self.menuBar()  # Update this line to get the menu bar from self
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 798, 21))
        self.menuchange_password = QMenu(self.menubar)
        self.menuchange_password.setObjectName(u"menuchange_password")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)
        self.menuchange_password.setTitle(QCoreApplication.translate("MainWindow", u"change password", None))
        self.menubar.addAction(self.menuchange_password.menuAction())
        self.change_pass = QAction("m", self)
        self.change_pass.setText(QCoreApplication.translate("MainWindow", u"change fire password", None))
        self.change_pass.setObjectName(u"actionchange_fire_password")
        self.change_pass.triggered.connect(self.change_fire_password)  # Connect triggered signal to slot
        self.menuchange_password.addAction(self.change_pass)

    def default_settings(self):
        global launch_password
        self.autherized = False
        self.speed = data["speed"]
        self.altitude = data["altitude"]
        self.pressure = data["pressure"]
        self.location = data["location"]
        self.long = data["location"].get("long") or "0"
        self.lat = data["location"]["lat"] or "0"
        self.ui.checkButton.hide()
        self.ui.initiate_Button.hide()
        self.ui.fireButton.hide()


    def buttons(self):
        self.ui.checkButton.clicked.connect(self.check_sensors)
        self.ui.unlock_Button.clicked.connect(self.get_authorization)



    def get_authorization(self):
        # Create an instance of PasswordDialog
        password_dialog = PasswordDialog()

        # Show the dialog and get the result
        result = password_dialog.exec_()

        # If OK button is clicked, retrieve the password and print it
        if result == QDialog.Accepted:
            password = password_dialog.getPassword()
            if password == launch_password:
                print("Password: ", password)
                print("USER HAS BEEN APROVED")
                self.autherized = True
                self.ui.checkButton.show()
                self.ui.initiate_Button.show()
                self.ui.fireButton.show()
                self.ui.unlock_Button.hide()
            else:
                QMessageBox.warning(self,"Authentecation Error","Entered password is not correct with stored password in database")
    def change_fire_password(self):
        if self.autherized:
            # Create an instance of PasswordDialog
            password_dialog = PasswordDialog()

            # Show the dialog and get the result
            result = password_dialog.exec_()

            # If OK button is clicked, retrieve the password and print it
            if result == QDialog.Accepted:
                password = password_dialog.getPassword()
                print("New Password: ", password)
                print("USER HAS BEEN APPROVED")
                global launch_password
                launch_password = password
                QMessageBox.information(self,"Change Password","The password has been changed")

    def refresh(self):
        print("refreshing UI")
        refresh()
        self.speed = data["speed"]  # Update the self.speed with the latest data value
        self.altitude = data["altitude"]
        self.pressure = data["pressure"]
        self.location = data["location"]
        self.long = data["location"]["long"]
        self.lat = data["location"]["lat"]

        self.ui.speed.setText(f"Speed: {self.speed}")  # Update the speed label with the latest value
        self.ui.pressure.setText(f"Pressure: {self.pressure}")
        self.ui.altitude.setText(f"Altitude: {self.altitude}")
        self.ui.location.setText(f"Location {self.long} || {self.lat}")
        print("Updated in UI")


    def charts(self):
        from PyQt5.Qt import Char
        from PyQt5.QtChart import QChart, QChartView, QLineSeries
        from PyQt5.QtCore import Qt
        from PyQt5.QtWidgets import QApplication, QMainWindow

        app = QApplication([])

        window = QMainWindow()

        chart = QChart()

        series = QLineSeries()
        series.append(0, 6)
        series.append(2, 4)
        series.append(3, 8)
        series.append(7, 4)
        series.append(10, 5)

        chart.addSeries(series)

        chart_view = QChartView(chart)
        window.setCentralWidget(chart_view)

        window.show()



    def check_sensors(self):
        QMessageBox.information(self,"Warning","كل الحساسات تعمل بكفائة")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    thred1 = threading.Thread(target=refresh)
    thred1.setDaemon(True)
    thred1.start()
    mainwin = MyForm()
    mainwin.show()

    sys.exit(app.exec_())
