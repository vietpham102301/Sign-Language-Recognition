

from menu import *

import sys

from time import sleep
import database
from login import *
from subprocess import call


load_meaning_state = 0

# chinh size cam
n = 400
d = 400

idx = 0
# nap database
his = database.get_all_favourites()
sav = database.get_all_translations()
listhis = []
listsav = []




class MiApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Login()
        self.ui.setupUi(self)

        # Xoa thanh tieu de
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        # SizeGrip
        self.gripSize = 10
        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(self.gripSize, self.gripSize)

        # Move window
        self.ui.Head.mouseMoveEvent = self.move_window

        # Truy cap cac trang
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.signQwidget))
        self.ui.btnBack.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.loginQwidget))

        # Dieu chinh thanh tieu de
        self.ui.hideButton.clicked.connect(self.control_hideButton)
        self.ui.quitButtion.clicked.connect(lambda: self.close())

        # Phim chuc nang
        self.ui.btnLogin.clicked.connect(self.control_login)
        self.ui.btnRegister.clicked.connect(self.control_register)


        # tat thong bao
        self.ui.fail_login.hide()
        self.ui.mess_sign.setCurrentWidget(self.ui.page_4)




    def control_hideButton(self):
        self.showMinimized()

    def control_login(self):
        user = self.ui.txtUsername.text()
        pwd = self.ui.txtPassword.text()
        idx = database.login(user, pwd)
        if idx == -1:
            self.ui.txtUsername.setText("")
            self.ui.txtPassword.setText("")
            self.ui.fail_login.show()
            self.control_login()
        else:
            # listhis.extend(database.get_translation_by_user_id(idx))
            # listsav.extend(database.get_favourite_by_user_id(idx))
            # ma = MyApp()
            # ma.show()
            # def update_label():
            #     if load_meaning_state == 0:
            #         # a_list = run.m_list
            #         ma.ui.outLabel.setText(' '.join(run.m_list))
            #     else:
            #         ma.ui.outLabel.setText(run.import_img_meaning)
            #
            # timer = QtCore.QTimer()
            # timer.timeout.connect(update_label)
            # timer.start(1000)
            #
            #
            # #sys.exit(app.exec_())
            self.close()
            call(["python", "main.py"])






    def control_register(self):
        user = self.ui.txtEmail.text()
        pwd = self.ui.txtPassword_regi.text()
        pwd1 = self.ui.txtPassword_regi2.text()
        print(self.check(user, pwd))
        if self.check(user, pwd) == 0:
            if pwd1 == pwd:
                if database.insert_user(user, pwd) == 1:
                    self.ui.mess_sign.setCurrentWidget(self.ui.ok)
                    sleep(1)
                    self.ui.mess_sign.setCurrentWidget(self.ui.loginQwidget)
                else:
                    self.ui.mess_sign.setCurrentWidget(self.ui.notg)
            else:
                self.ui.txtEmail.setText("")
                self.ui.txtPassword_regi.setText("")
                self.ui.txtPassword_regi2.setText("")
                self.ui.mess_sign.setCurrentWidget(self.ui.pr)
        else:
            self.ui.txtEmail.setText("")
            self.ui.txtPassword_regi.setText("")
            self.ui.txtPassword_regi2.setText("")

    def check(self, user, pwd):
        if user == '' or pwd == '':
            return -1
        return 0

    # SizeGrip
    def resizeEvent(self, event):
        rect = self.rect()
        self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

    # move window
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def move_window(self, event):
        if self.isMaximized() == False:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

        if event.globalPos().y() <= 20:
            self.showMaximized()
        else:
            self.showNormal()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_app = MiApp()
    my_app.show()


    sys.exit(app.exec_())