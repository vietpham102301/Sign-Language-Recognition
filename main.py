import sys

from PyQt5.uic.properties import QtWidgets

import run


if __name__ == '__main__':
    output_path, class_name = run.recognize_with_img_import('G:\ForPushGit\Sign-Language-Recognition\Tensorflow\workspace\images\\reduce_train\goodbye.cd1ac334-8221-11ed-9b17-ecf4bb0781e6.jpg')

    # out_path, meaning_list = run.realtime_recognition_for_test()
    # print("out_path: {}".format(out_path))
    # print("meaning: {}".format(' '.join(meaning_list)))
    print('out: {out} \nclass_name: {class_name}'.format(out = output_path, class_name = class_name))


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     my_app = MyApp()
#     # print("out_path: {}".format(out_path))
#     # print("meaning: {}".format(' '.join(meaning_list)))
#     # my_app.ui.outLabel.setText(' '.join(run.m_list))
#     # print('list: ', run.m_list)
#     my_app.show()
#     sys.exit(app.exec_())