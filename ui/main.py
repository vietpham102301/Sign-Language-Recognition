import sys

import cv2
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import QListWidgetItem, QFileDialog
import numpy as np

from menu import *

from PyQt5.QtCore import QSize, pyqtSignal, QThread, Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import os

import playsound

from gtts import gTTS

import run
from time import sleep
import database
from login import *


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

# listhis = [["img/1.jpg", "Hinh daksjdklasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/2.jpg", "Hinh dklasjdaksjdklasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/3.jpg", "Hinh dklasjdaksjdklasjdklsajdklasjlkdjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/4.jpg", "Hinh dklasjdaksjdklasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/5.jpg", "Hinh dklasjdaksjdklasjdklkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/6.jpg", "Hinh dklasjdaksjdklasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1]]
# listsav = [["img/1.jpg", "Hinh dklasjdaksjdklasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/2.jpg", "Hinh dklasjdaksjdklasjdasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/3.jpg", "Hinh dklasjdaksjdklasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/4.jpg", "Hinh dklasjdaksjdklasjdklsajdklasskldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/5.jpg", "Hinh dklasjdaksjdklasjdklsajdklkldjaskldjaskdjaskldjaskldjaskl", 1],
#            ["img/6.jpg", "Hinh dklaasjdklsajdklasjlkdjaskldjaskldjaskdjaskldjaskldjaskl", 1]]




class cap_video(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.index = index
        super(cap_video, self).__init__()

    def run(self):
        self.thread_active = True
        # cap = cv2.VideoCapture(0)
        # while True:
        #     ret, cv_img = cap.read()
        #     if ret:
        # self.signal.emit(cv_img)
        run.realtime_recognition(self)



    def stop(self):
        self.quit()
        self.thread_active = False

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
            ma = MyApp()
            ma.show()
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


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()


        self.ui = Ui_MainWindow()
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
        self.ui.transButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.transPage))
        self.ui.transButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.transPage))
        self.ui.dicButton.clicked.connect(self.control_sav)
        self.ui.hisButton.clicked.connect(self.control_his)

        # Dieu chinh nut luu va xoa
        self.ui.findLine.hide()

        # Dieu chinh thanh tieu de
        self.ui.hideButton.clicked.connect(self.control_hideButton)
        self.ui.minButton.clicked.connect(self.control_minButton)
        self.ui.maxButton.clicked.connect(self.control_maxButton)
        self.ui.quitButtion.clicked.connect(lambda: self.close())
        self.ui.minButton.hide()
        self.ui.cameraButton_2.hide()


        # Phim chuc nang

        self.ui.photoButton.clicked.connect(self.control_photo)
        self.ui.soundButton.clicked.connect(self.control_sound)
        self.ui.delallButton.clicked.connect(self.control_delall_his)
        self.ui.searchButton.clicked.connect(self.seacrch_save)
        self.ui.searchButton_2.clicked.connect(self.seacrch_his)
        self.ui.delallButton_2.clicked.connect(self.control_delall_save)
        #self.ui.save.clicked.connect(self.add_fav)


        self.thread = {}
        self.open_camera()
        self.camera_state = 0
        self.ui.cameraButton.clicked.connect(self.control_camera)
        #self.ui.cameraButton_2.clicked.connect(self.control_camera_2)






    def showhis(self, list, u):
        self.newItem = QListWidgetItem()
        self.newItem.setSizeHint(QSize(0, 200))
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setStyleSheet("QPushButton{\n"
                                         "background-color: rgb(118, 185, 0);\n"
                                         "border: 1px solid rgb(61, 94, 0);\n"
                                         "border-radius:10px;\n"
                                         "color: rgb(56, 95, 0);\n"
                                         "}\n"
                                         "QPushButton:hover{\n"
                                         "background-color: rgb(96, 148, 0);\n"
                                         "\n"
                                         "color: white;\n"
                                         "}\n"
                                         "QPushButton:pressed{\n"
                                         "background-color: red;\n"
                                         "\n"
                                         "}\n"
                                         "QFrame {\n"
                                         "background-color: rgb(150, 150, 150);\n"
                                         "}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.showFrame = QtWidgets.QFrame(self.centralwidget)
        self.showFrame.setMaximumSize(QtCore.QSize(16777215, 200))
        self.showFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.showFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.showFrame.setObjectName("showFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.showFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imgFrame = QtWidgets.QFrame(self.showFrame)
        self.imgFrame.setMinimumSize(QtCore.QSize(200, 200))
        self.imgFrame.setMaximumSize(QtCore.QSize(200, 200))
        self.imgFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.imgFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.imgFrame.setObjectName("imgFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.imgFrame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.imgFrame)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_2.setScaledContents(True)
        self.label_2.setPixmap(QtGui.QPixmap(list[0]))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.imgFrame)
        self.frame_3 = QtWidgets.QFrame(self.showFrame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.meanLabel = QtWidgets.QLabel(self.frame_3)
        self.meanLabel.setMinimumSize(QtCore.QSize(200, 198))
        self.meanLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.meanLabel.setFont(font)
        self.meanLabel.setAutoFillBackground(False)
        self.meanLabel.setLineWidth(9)
        self.meanLabel.setMidLineWidth(0)
        self.meanLabel.setText("")
        self.meanLabel.setTextFormat(QtCore.Qt.RichText)
        self.meanLabel.setScaledContents(False)
        self.meanLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.meanLabel.setWordWrap(True)
        self.meanLabel.setObjectName("meanLabel")
        self.meanLabel.setText(list[1])
        self.verticalLayout_2.addWidget(self.meanLabel)
        self.horizontalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.showFrame)
        self.frame_4.setMinimumSize(QtCore.QSize(75, 200))
        self.frame_4.setMaximumSize(QtCore.QSize(75, 200))
        self.frame_4.setMouseTracking(False)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btnSave = QtWidgets.QPushButton(self.frame_4)
        self.btnSave.setMaximumSize(QtCore.QSize(50, 50))
        self.btnSave.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon)
        self.btnSave.setIconSize(QtCore.QSize(50, 50))
        self.btnSave.setFlat(True)
        self.btnSave.setObjectName("btnSave")
        self.verticalLayout_3.addWidget(self.btnSave)
        self.btnSound = QtWidgets.QPushButton(self.frame_4)
        self.btnSound.setMaximumSize(QtCore.QSize(50, 50))
        self.btnSound.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/high-volume.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSound.setIcon(icon1)
        self.btnSound.setIconSize(QtCore.QSize(45, 45))
        self.btnSound.setFlat(True)
        self.btnSound.setObjectName("btnSound")
        self.verticalLayout_3.addWidget(self.btnSound)
        self.btnDel = QtWidgets.QPushButton(self.frame_4)
        self.btnDel.setMaximumSize(QtCore.QSize(50, 50))
        self.btnDel.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDel.setIcon(icon2)
        self.btnDel.setIconSize(QtCore.QSize(50, 50))
        self.btnDel.setFlat(True)
        self.btnDel.setObjectName("btnDel")
        self.verticalLayout_3.addWidget(self.btnDel)
        self.horizontalLayout.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.showFrame)

        self.btnSound.clicked.connect(lambda: self.control_sound_2(list[1]))
        self.btnSave.clicked.connect(lambda: self.control_save(list))


        if u == 1:
            self.ui.hisListWidget.addItem(self.newItem)
            self.ui.hisListWidget.setItemWidget(self.newItem, self.centralwidget)
            self.btnDel.clicked.connect(lambda: self.control_del(list, 1))
        else:
            self.btnDel.clicked.connect(lambda: self.control_del(list, 0))
            self.ui.saveListWidget.addItem(self.newItem)
            self.btnSave.hide()
            self.ui.saveListWidget.setItemWidget(self.newItem, self.centralwidget)

    # Ham chuc nang can them v
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



    #dieu huong

    def control_his(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.hisPage)
        for list in listhis:
            self.showhis(list, 1)

    def control_sav(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.savedPage)
        for list1 in listsav:
            self.showhis(list1, 0)


    def control_save(self, lt):
        for it in listsav:
            if it == lt:
                return None
        listsav.append(lt)

    def control_sound_2(self, sound):
        speaktext(sound)

    def control_sound(self):
        sound = self.ui.outLabel.text()
        speaktext(sound)

    # camera

    def control_photo(self):
        self.thread[1].stop()
        frame = QFileDialog.getOpenFileName(self, "Open file", "G:/", "JPG files (*.jpg)")
        if frame[0] != '':
            output_path, class_name = run.recognize_with_img_import(frame[0])
            print('path: ', frame)
            print('class_name: ', class_name)
            run.import_img_meaning = class_name
            global load_meaning_state
            load_meaning_state = 1
            self.ui.cameraLabel.setPixmap(QtGui.QPixmap(output_path))


    def open_camera(self):
        self.thread[1] = cap_video(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_camera)
        # self.ui.cameraButton.hide()
        # self.ui.cameraButton_2.show()

    def control_camera(self):
        if self.camera_state == 0:
            self.thread[1].stop()
            self.camera_state = 1
        else:
            self.thread[1].start()
            self.camera_state = 0
            global load_meaning_state
            load_meaning_state = 0
        # self.ui.cameraButton_2.hide()
        # self.ui.cameraButton.show()


    def show_camera(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.ui.cameraLabel.setPixmap(qt_img)
        # self.ui.outLabel.setText(' '.join(meaning_list))

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(n, d, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def control_del(self, list, name):
        if name == 1:
            listhis.remove(list)
            database.delete_translation(list[0])
            self.ui.hisListWidget.clear()
            for lt in listhis:
                self.showhis(lt, 1)
        else:
            listsav.remove(list)
            database.delete_favourite(list[0])
            self.ui.saveListWidget.clear()
            for lt in listsav:
                self.showhis(lt, 0)

    def control_delall_his(self):
            listhis.clear()
            database.delete_all_translation_by_user_id(idx)
            self.ui.hisListWidget.clear()

    def control_delall_save(self):
            listsav.clear()
            database.delete_all_favourite_by_user_id(idx)
            self.ui.saveListWidget.clear()


    def seacrch_his(self):
        f = self.ui.findLine.text()
        self.ui.hisListWidget.clear()
        for list in listhis:
            if list[2].find(f) != -1:
                self.showhis(list, 1)
    def seacrch_save(self):
        f = self.ui.findLine.text()
        self.ui.saveListWidget.clear()
        for list in listsav:
            if list[2].find(f) != -1:
                self.showhis(list, 0)

    # def add_fav(self):
    #     pass
    #     database.insert_favourite(path,meaning,idx)
    #
    # def add_his(self):
    #     pass
    #     database.insert_translation(path,meaning,idx)

    def control_hideButton(self):
        self.showMinimized()

    def control_minButton(self):
        self.showNormal()
        self.ui.minButton.hide()
        self.ui.maxButton.show()

    def control_maxButton(self):
        self.showMaximized()
        self.ui.maxButton.hide()
        self.ui.minButton.show()

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


# ham nay




def speaktext(text):
    tts = gTTS(text=text, lang="vi")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove("voice.mp3")


def open_main_app():
    listhis.extend(database.get_translation_by_user_id(idx))
    listsav.extend(database.get_favourite_by_user_id(idx))
    ma = MyApp()
    print("smt")

    def update_label():
        if load_meaning_state == 0:
            # a_list = run.m_list
            my_app.ui.outLabel.setText(' '.join(run.m_list))
        else:
            my_app.ui.outLabel.setText(run.import_img_meaning)

    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(1000)
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    def update_label():
        if load_meaning_state == 0:
            # a_list = run.m_list
            my_app.ui.outLabel.setText(' '.join(run.m_list))
        else:
            my_app.ui.outLabel.setText(run.import_img_meaning)


    timer = QtCore.QTimer()
    timer.timeout.connect(update_label)
    timer.start(1000)

    sys.exit(app.exec_())



