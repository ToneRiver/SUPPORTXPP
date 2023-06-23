'''XPP補助用プログラムです'''
#!/usr/bin/env python3

import sys
import subprocess
import os
from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

###############################################################
# 初期設定
dat_files_location = '.\\'  # 普段XPPのdatファイルを保存しておくフォルダパスを記入してください．
output_location = 'output'  # このアプリからジャンプできるグラフ出力場所を記入してください．
python_code = 'python'  # pythonのプログラムを実行するときの先頭部分
# python_code = 'python3'  # pythonのプログラムを実行するときの先頭部分
apo = "" #windows
# apo = "'" #mac
###############################################################


class GuiWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.build_ui()
        self.set_ui()
        self.setWindowTitle('XPP補助用プログラム')

    def build_ui(self):  # uiを生成します
        # self.title_text = QLabel('修士研究用ポータル', self)
        self.quit_button = QPushButton('アプリ終了', self)
        self.quit_button.clicked.connect(self.close)
        self.jump_datFiles_button = QPushButton('outputに飛ぶ', self)
        self.jump_datFiles_button.clicked.connect(lambda: self.jump_to_url(
            output_location))
        # self.launch_XPP_button = QPushButton('XPPを終了する', self)
        # self.launch_XPP_button.clicked.connect(self.quit_XPP)
        # self.launch_XPPuniv_button = QPushButton('XPPを起動する', self)
        # self.launch_XPPuniv_button.clicked.connect(self.launch_XPP)
        self.file_name = QLineEdit('', self)
        self.launch_XPPtoPDF2_button = QPushButton('右の名前でall info.datをPDF化する', self)
        self.launch_XPPtoPDF2_button.clicked.connect(self.launch_XPPtoPDF2)
        self.uis = [
            [[self.quit_button, 600, 40]],
            [[self.jump_datFiles_button, 160, 40]],
        ]
        self.dat_labels = [QLabel('', self), QLabel('', self), QLabel('', self), QLabel('', self)]
        self.dat_names = [[], [], [], []]
        self.set_dat_file_buttons = [[], [], [], []]
        self.reset_dat_file_buttons = [[], [], [], []]
        self.group_names = ["", "B", "C", "個別"]
        self.uis.append([])
        self.set_dat_file_buttons[0] = QPushButton('dat_fileをセット', self)
        self.set_dat_file_buttons[0].clicked.connect(lambda: self.set_dat_file(0))
        self.uis[-1].append([self.set_dat_file_buttons[0], 140, 40])
        # self.set_dat_file_buttons[1] = QPushButton(self.group_names[1]+':datをセット', self)
        # self.set_dat_file_buttons[1].clicked.connect(lambda: self.set_dat_file(1))
        # self.uis[-1].append([self.set_dat_file_buttons[1], 140, 40])
        # self.set_dat_file_buttons[2] = QPushButton(self.group_names[2]+':datをセット', self)
        # self.set_dat_file_buttons[2].clicked.connect(lambda: self.set_dat_file(2))
        # self.uis[-1].append([self.set_dat_file_buttons[2], 140, 40])
        # self.set_dat_file_buttons[3] = QPushButton(self.group_names[3]+':datをセット', self)
        # self.set_dat_file_buttons[3].clicked.connect(lambda: self.set_dat_file(-1))
        # self.uis[-1].append([self.set_dat_file_buttons[3], 140, 40])
        # self.uis.append([])
        self.reset_dat_file_buttons[0] = QPushButton('dat_fileをリセット', self)
        self.reset_dat_file_buttons[0].clicked.connect(lambda: self.reset_dat_file(0))
        self.uis[-1].append([self.reset_dat_file_buttons[0], 140, 40])
        # self.reset_dat_file_buttons[1] = QPushButton(self.group_names[1]+':datをリセット', self)
        # self.reset_dat_file_buttons[1].clicked.connect(lambda: self.reset_dat_file(1))
        # self.uis[-1].append([self.reset_dat_file_buttons[1], 140, 40])
        # self.reset_dat_file_buttons[2] = QPushButton(self.group_names[2]+':datをリセット', self)
        # self.reset_dat_file_buttons[2].clicked.connect(lambda: self.reset_dat_file(2))
        # self.uis[-1].append([self.reset_dat_file_buttons[2], 140, 40])
        # self.reset_dat_file_buttons[3] = QPushButton(self.group_names[3]+':datをリセット', self)
        # self.reset_dat_file_buttons[3].clicked.connect(lambda: self.reset_dat_file(-1))
        # self.uis[-1].append([self.reset_dat_file_buttons[3], 140, 40])
        self.uis.append([])
        self.uis[-1].append([self.dat_labels[0], 180, 80])
        # self.uis[-1].append([self.dat_labels[1], 180, 80])
        # self.uis[-1].append([self.dat_labels[2], 180, 80])
        # self.uis[-1].append([self.dat_labels[3], 180, 80])
        self.uis.append([])
        # self.uis[-1].append([self.PDF_name, 160, 30])
        self.uis[-1].append([self.launch_XPPtoPDF2_button, 260, 40])
        self.uis[-1].append([self.file_name, 160, 30])
        self.uis.append([])
        self.checkBoxStableEque = QCheckBox("安定平衡点", self)
        self.checkBoxStableEque.setChecked(True)
        self.uis[-1].append([self.checkBoxStableEque, 140, 40])
        self.checkBoxUnStableEque = QCheckBox("不安定平衡点", self)
        self.checkBoxUnStableEque.setChecked(True)
        self.uis[-1].append([self.checkBoxUnStableEque, 140, 40])
        self.checkBoxStablePeri = QCheckBox("安定周期解", self)
        self.checkBoxStablePeri.setChecked(True)
        self.uis[-1].append([self.checkBoxStablePeri, 140, 40])
        self.checkBoxUnStablePeri = QCheckBox("不安定周期解", self)
        self.checkBoxUnStablePeri.setChecked(True)
        self.uis[-1].append([self.checkBoxUnStablePeri, 140, 40])
        self.checkBoxEigenValue = QCheckBox("全変数を出力", self)
        self.checkBoxEigenValue.setChecked(True)
        self.uis[-1].append([self.checkBoxEigenValue, 140, 40])
        self.uis.append([])
        self.variable_text = QLabel('変数', self)
        self.uis[-1].append([self.variable_text, 140, 40])
        self.x_start_label = QLabel('x_start', self)
        self.uis[-1].append([self.x_start_label, 60, 40])
        self.x_end_label = QLabel('x_end', self)
        self.uis[-1].append([self.x_end_label, 60, 40])
        self.y_start_label = QLabel('y_start', self)
        self.uis[-1].append([self.y_start_label, 60, 40])
        self.y_end_label = QLabel('y_end', self)
        self.uis[-1].append([self.y_end_label, 60, 40])
        self.x_label_label = QLabel('x_label', self)
        self.uis[-1].append([self.x_label_label, 60, 40])
        self.y_label_label = QLabel('y_label', self)
        self.uis[-1].append([self.y_label_label, 60, 40])
        # self.eigen_start_label = QLabel('固有値(始)', self)
        # self.uis[-1].append([self.eigen_start_label, 60, 40])
        # self.eigen_end_label = QLabel('固有値(終)', self)
        # self.uis[-1].append([self.eigen_end_label, 60, 40])
        self.uis.append([])
        self.variable_num = QLineEdit('1', self)
        self.uis[-1].append([self.variable_num, 40, 40])
        self.x_start = QLineEdit('0', self)
        self.uis[-1].append([self.x_start, 60, 40])
        self.x_end = QLineEdit('10', self)
        self.uis[-1].append([self.x_end, 60, 40])
        self.y_start = QLineEdit('0', self)
        self.uis[-1].append([self.y_start, 60, 40])
        self.y_end = QLineEdit('5', self)
        self.uis[-1].append([self.y_end, 60, 40])
        self.x_label = QLineEdit('$D$', self)
        self.uis[-1].append([self.x_label, 60, 40])
        self.y_label = QLineEdit('$X_{1}$', self)
        self.uis[-1].append([self.y_label, 60, 40])
        # self.eigen_start = QLineEdit('0', self)
        # self.uis[-1].append([self.eigen_start, 60, 40])
        # self.eigen_end = QLineEdit('10', self)
        # self.uis[-1].append([self.eigen_end, 60, 40])

    def set_ui(self):  # uiを配置します
        I = len(self.uis)
        Jmax = 0
        Hmax = 0
        # print(max([self.uis[1][i][2] for i in range(0,3)]))
        y = 0
        for i, v_stack in enumerate(self.uis):
            J = len(v_stack)
            H = sum(self.uis[i][k][1] for k in range(J))
            if Hmax < H:
                Hmax = H
        self.w = Hmax
        for i, v_stack in enumerate(self.uis):
            J = len(v_stack)
            Vmax = max([self.uis[i][k][2] for k in range(J)])
            # print(y)
            if Jmax < J:
                Jmax = J
            for j, h_stack in enumerate(v_stack):
                # print((2*j+1)/(2*J)*self.w-h_stack[1]/2,(2*i+1)/(2*I)*self.h-h_stack[2]/2,h_stack[1],h_stack[2])
                h_stack[0].setGeometry(int((2*j+1)/(2*J)*self.w-h_stack[1]/2),
                                       int(y+Vmax/2), int(h_stack[1]), int(h_stack[2]))
                try:
                    h_stack[0].setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                except:
                    pass
            y += Vmax
        self.h = y+Vmax
        self.setGeometry(0, 0, self.w, self.h)
        self.setFixedSize(self.w, self.h)

    def jump_to_url(self, url):
        if os.path.exists(url):
            subprocess.call(["open", url])

    def open_vscode_url(self, url):
        if os.path.exists(url):
            subprocess.call("code "+url, shell=True)

    def launch_XPP(self):
        os.chdir("/Users/mebar/xppmac/myode")
        XPPname = "xppmacuniv"
        subprocess.Popen(".././"+XPPname, shell=True)
        XPPname = "xppmac64"
        subprocess.Popen(".././"+XPPname, shell=True)

    def quit_XPP(self):
        os.chdir("/Users/mebar/xppmac")
        XPPname = "xppmacuniv"
        subprocess.Popen("killall "+XPPname, shell=True)
        XPPname = "xppmac64"
        subprocess.Popen("killall "+XPPname, shell=True)

    def launch_XPPtoPDF2(self):
        program_pass = "XPPtoPDF_Re2.py"
        dat_full_name = ""
        draw_eigenValue = " " + str(self.checkBoxEigenValue.isChecked()) + " " + "0" + \
            " " + "10"  # 固有値の表を出力するか またその範囲
        draw_solution = " "  # どの解を描画するか True True False Trueだと安定周期解以外を描画する
        draw_solution += str(self.checkBoxStableEque.isChecked()) + " "
        draw_solution += str(self.checkBoxUnStableEque.isChecked()) + " "
        draw_solution += str(self.checkBoxStablePeri.isChecked()) + " "
        draw_solution += str(self.checkBoxUnStablePeri.isChecked()) + " "
        each_setting = self.variable_num.text() + " " + self.x_start.text() + " " + self.x_end.text() + " " + self.y_start.text() + \
            " " + self.y_end.text() + " "+apo+"" + self.x_label.text() + ""+apo+" "+apo+"" + self.y_label.text() + ""+apo+""
        for i, d in enumerate(self.dat_names):
            if i == len(self.dat_names)-1:  # 最後のセットは個別変換
                for j, dd in enumerate(self.dat_names[i]):
                    mycommand = python_code+" "+program_pass+" " + \
                        os.path.basename(dd)[:-4]+" GROUP "+dd + draw_eigenValue + draw_solution + each_setting
                    # print("mycommand j\n",mycommand)
                    subprocess.Popen(mycommand, shell=True)
            else:  # 最後のセット以外は複数のdatを一つのpdfにする
                for j, dd in enumerate(self.dat_names[i]):
                    if j == 0:
                        dat_full_name += " GROUP"
                    dat_full_name += " " + str(dd)
        if self.file_name.text() != "":
            program_pass += " "
        mycommand = python_code+" "+program_pass+self.file_name.text()+dat_full_name + draw_eigenValue + \
            draw_solution + each_setting
        if dat_full_name != "":
            subprocess.Popen(mycommand, shell=True)
        self.jump_to_url(
            output_location)

    def set_dat_file(self, i):
        base_path = dat_files_location
        filenames, selectedFilters = QFileDialog.getOpenFileNames(self, 'Open file', base_path)
        for j, f in enumerate(filenames):
            # print(selectedFilters[j])
            self.dat_names[i].append(f)
        # print(i)
        text = ""
        for k in range(len(self.dat_names[i])):
            if k != 0:
                text += "\n"
            text += os.path.basename(self.dat_names[i][k])
        self.dat_labels[i].setText(text)
        # print("dat", self.dat_names)

    def reset_dat_file(self, i):
        self.dat_names[i] = []
        self.dat_labels[i].setText("")

    def optimize_layout(self):
        self.w = self.frameGeometry().width()
        self.h = self.frameGeometry().height()
        self.set_ui()

    # ウィンドウのリサイズイベントを拾う
    def resizeEvent(self, event):
        pass
        # self.optimize_layout()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GuiWindow()
    window.show()
    sys.exit(app.exec())
