'''XPPで出力したall info.datファイル1つ以上をコマンドライン引数で指定してグラフとして重ねてXPP_outに出力するプログラムです．'''
'''プログラムの実行はpython3 XPPtoPDF_Re2.py ...でお願いします。'''
'''datファイルの最後は\nであるとします'''
# import pyperclip as pc

################################
# 初期設定
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import shutil
out_path = "output"  # 出力フォルダ
# delimiter = "/" #mac用フォルダ区切り文字
delimiter = '\\'  # windows用フォルダ区切り文字
# myFont = "Hiragino Sans" #mac用フォント
myFont = "MS Gothic"  # windows用フォント

# 設定
subplots_adjust_left=0.19
subplots_adjust_right=0.95
subplots_adjust_bottom=0.15
subplots_adjust_top=0.93
set_xlim = True
set_ylim = True
lang = "EN"  # EN=英語, JP=日本語
if lang == "JP":
    label = ["不安定平衡点", "不安定周期解", "安定平衡点", "安定周期解"]
elif lang == "EN":
    label = ["Unstable Equilibrium", "Unstable Periodic", "Stable Equilibrium", "Stable Periodic"]

################################

same_color = True  # 2つ目のdatを2Pカラーにしないかするか
xlim = [1, 6]
ylim = [0, 3]
eigen_lim = [0, 0]
xlabel = "$D$"
ylabel = "variable"
epoch = 0


def duplicate_rename(file_path):  # ファイル名がかぶっていなかったらそのまま，かぶっていたらナンバリングを付与して返す
    if os.path.exists(file_path):
        name, ext = os.path.splitext(file_path)
        i = 1
        while True:
            # 数値を3桁などにしたい場合は({:0=3})とする
            new_name = "{}【{}】{}".format(name, i, ext)
            if not os.path.exists(new_name):
                return new_name
            i += 1
    else:
        return file_path


def gen_graph(ax, data, colors, labels, n,variable_num):
    global eigenValues_tex, epoch, all_epoch, draw_allVariables
    stableE = []
    unstableE = []
    stableP = []
    unstableP = []
    solution_kinds = ["\\textcolor{red}{安定平衡点}", "\\textbf{不安定平衡点}",
                      "\\textcolor{green}{安定周期解}", "\\textcolor{blue}{不安定周期解}"]
    for d_i, d in enumerate(data):
        print(str(epoch))
        epoch += 1
        # if draw_allVariables is True and eigen_lim[0] <= float(d[3]) and float(d[3]) <= eigen_lim[1]:
        #     eigenValues_tex += f'{xlabel} $ = {d[3]}$のとき，{solution_kinds[int(d[0])-1]}であり，variable$ = $ '
        #     for i in range(n):
        #         if i != 0:
        #             eigenValues_tex += ', '
        #         if d[0] >= 3:
        #             eigenValues_tex += f'${d[6+n+i]} 〜 {d[6+i]}$'+' \\\\'
        #         else:
        #             eigenValues_tex += f'${d[6+i]}$'+' \\\\'
        #     eigenValues_tex += ' \\ \n'
        #     if d_i != 0:
        #         eigenValues_tex += '$(e^{\\lambda}) [(\\lambda)]='
        #         for i in range(n):
        #             re = d[6+2*n+2*i+1-1]
        #             im = d[6+2*n+2*i+2-1]
        #             comp = re + im*1j  # exp(A)の虚数表示
        #             mag = abs(comp)  # 絶対値
        #             phase = cmath.phase(comp)  # 位相
        #             comp2 = math.log(mag) + phase * 1j  # Aの固有値
        #             if i != 0:
        #                 eigenValues_tex += ', '
        #             if mag >= 1:
        #                 eigenValues_tex += '\\bm{ '+str(comp)+' \\quad ['+str(comp2)+']}'+' \\\\'
        #             else:
        #                 eigenValues_tex += f' {comp} \\quad [{comp2}]'+' \\\\'
        #             # if im > 0:
        #             #     eigenValues_tex += f'{re}+{im}i'
        #             # elif im < 0:
        #             #     eigenValues_tex += f'{re}{im}i'
        #             # else:
        #             #     eigenValues_tex += f'{re}'
        #         eigenValues_tex += '$\\\\ \n\n'
        if variable_num != "period":
            if (int(d[0]) == 1 and draw_solutions[0] == "True"):
                stableE = np.append(stableE, [d[3], d[6+variable_num-1]])
                pass
            if (int(d[0]) == 2 and draw_solutions[1] == "True"):
                unstableE = np.append(unstableE, [d[3], d[6+variable_num-1]])
                pass
            if (int(d[0]) == 3 and draw_solutions[2] == "True"):
                stableP = np.append(stableP, [d[3], d[6+variable_num-1]])
                stableP = np.append(stableP, [d[3], d[6+n+variable_num-1]])
                pass
            if (int(d[0]) == 4 and draw_solutions[3] == "True"):
                unstableP = np.append(unstableP, [d[3], d[6+variable_num-1]])
                unstableP = np.append(unstableP, [d[3], d[6+n+variable_num-1]])
                pass
        else:
            if (int(d[0]) == 3):
                stableP = np.append(stableP, [d[3], d[5]])
                stableP = np.append(stableP, [d[3], d[5]])
                pass
            if (int(d[0]) == 4):
                unstableP = np.append(unstableP, [d[3], d[5]])
                unstableP = np.append(unstableP, [d[3], d[5]])
                pass

    if labels != False:
        if len(unstableE) != 0:
            unstableE = unstableE.reshape([int(len(unstableE)/2), 2])
            ax.scatter(unstableE[:, 0], unstableE[:, 1], color=colors[0], label=labels[0], s=8)
        if len(unstableP) != 0:
            unstableP = unstableP.reshape([int(len(unstableP)/2), 2])
            ax.scatter(unstableP[:, 0], unstableP[:, 1], color=colors[1], label=labels[1], s=8)
        if len(stableE) != 0:
            stableE = stableE.reshape([int(len(stableE)/2), 2])
            ax.scatter(stableE[:, 0], stableE[:, 1], color=colors[2], label=labels[2], s=8)
        if len(stableP) != 0:
            stableP = stableP.reshape([int(len(stableP)/2), 2])
            ax.scatter(stableP[:, 0], stableP[:, 1], color=colors[3], label=labels[3], s=8)
    else:
        if len(unstableE) != 0:
            unstableE = unstableE.reshape([int(len(unstableE)/2), 2])
            ax.scatter(unstableE[:, 0], unstableE[:, 1], color=colors[0], s=8)
        if len(unstableP) != 0:
            unstableP = unstableP.reshape([int(len(unstableP)/2), 2])
            ax.scatter(unstableP[:, 0], unstableP[:, 1], color=colors[1], s=8)
        if len(stableE) != 0:
            stableE = stableE.reshape([int(len(stableE)/2), 2])
            ax.scatter(stableE[:, 0], stableE[:, 1], color=colors[2], s=8)
        if len(stableP) != 0:
            stableP = stableP.reshape([int(len(stableP)/2), 2])
            ax.scatter(stableP[:, 0], stableP[:, 1], color=colors[3], s=8)


file_name = ""
files = []
draw_solutions = []  # 安定/不安定 平衡点/周期解　どれを描画するか
variable_num_fact = 0  # どの変数を描画するか
draw_allVariables = False
for i, a in enumerate(sys.argv):
    if i == len(sys.argv) - 14:
        if a == "True":
            draw_allVariables = True
        continue
    if i == len(sys.argv) - 13:
        eigen_lim[0] = float(a)
        continue
    if i == len(sys.argv) - 12:
        eigen_lim[1] = float(a)
        continue
    if len(sys.argv) - 11 <= i and i <= len(sys.argv) - 8:
        draw_solutions.append(a)
        continue
    if i == len(sys.argv) - 7:
        variable_num_fact = int(a)
        continue
    if i == len(sys.argv) - 6:
        xlim[0] = float(a)
        continue
    if i == len(sys.argv) - 5:
        xlim[1] = float(a)
        continue
    if i == len(sys.argv) - 4:
        ylim[0] = float(a)
        continue
    if i == len(sys.argv) - 3:
        ylim[1] = float(a)
        continue
    if i == len(sys.argv) - 2:
        xlabel = str(a)
        continue
    if i == len(sys.argv) - 1:
        ylabel = str(a)
        continue
    if i == 0:
        pass
    elif i == 1 and a != "GROUP":
        file_name = a
    elif a == "GROUP":
        files.append([])
    else:
        files[-1].append(a)

print(files)
print(draw_solutions)
if file_name == "":
    file_name = "noname"
# if file_name != "":
#     file_name += "_"
# dt_now = datetime.datetime.now()
# dt_now_format = dt_now.strftime('%Y%m%d_%H%M%S')
# file_name += dt_now_format
datas = []

last_folder_name = duplicate_rename(out_path + delimiter + str(file_name))
for i in range(len(files)):
    for j, f in enumerate(files[i]):
        # print(f[7:-4])
        data = np.loadtxt(f, dtype='float')  # datファイルひとつ分
        data[0, 0] = data[1, 0] # はじめの一点はなぜか不安定であると判定されてしまうのでこれを修正
        if j == 0:
            cat_data = data  # datファイル二つを同じグラフに結合したもの
        else:
            cat_data = np.vstack([cat_data, data])
        # new_path = shutil.copyfile(f, 'XPP_past/'+file_name+'/'+f[7:-4]+'.dat') #一応コピーして保管する
    # print(cat_data)
    datas.append(cat_data)

n = int((len(datas[0][0])-6)/4)  # モデルの次元
if draw_allVariables is True:
    variable_nums = list(range(0, n+1))
    variable_nums.append("period")
else:
    variable_nums = [0,"period"]

os.makedirs(last_folder_name, exist_ok=True)
for variable_num in variable_nums:
    fig, ax = plt.subplots()
    ax.set_xlabel(xlabel, size=20)
    if variable_num == 0:
        ax.set_ylabel(ylabel, size=20)
    elif variable_num == "period":
        ax.set_ylabel("period", size=20)
    else:
        ax.set_ylabel("ordinate", size=20)
    if set_xlim and variable_num == 0:
        ax.set_xlim(xlim[0], xlim[1])
    if set_ylim and variable_num == 0:
        ax.set_ylim(ylim[0], ylim[1])

    all_epoch = 0
    for i in range(len(datas)):
        all_epoch = len(datas[i])
        colors = [["black", "blue", "red", "green"], ["dimgrey", "royalblue", "orangered", "limegreen"]]
        labels = [label, False]
        if same_color:
            if variable_num == 0:
                gen_graph(ax, datas[i], colors[0], labels[min(i, len(labels)-1)], n,variable_num_fact)
            else:
                gen_graph(ax, datas[i], colors[0], labels[min(i, len(labels)-1)], n,variable_num)
        else:
            if variable_num == 0:
                gen_graph(ax, datas[i], colors[min(i, len(colors)-1)], labels[min(i, len(labels)-1)], n,variable_num_fact)
            else:
                gen_graph(ax, datas[i], colors[min(i, len(colors)-1)], labels[min(i, len(labels)-1)], n,variable_num)

    # 補助目盛を表示
    ax.minorticks_on()
    # 目盛り線の表示
    ax.grid(which="major", color="black", alpha=0.5)
    ax.grid(which="minor", color="gray", linestyle=":")
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    fig.subplots_adjust(left=subplots_adjust_left, right=subplots_adjust_right, bottom=subplots_adjust_bottom, top=subplots_adjust_top)
    plt.rc("legend", fontsize=18)
    if lang == "JP":
        plt.legend(prop={"family": myFont}, markerscale=5)
    else:
        plt.legend(markerscale=5)
    # plt.title("$"+str(file_name[2:])+"$",fontsize=20)

    # グラフを pdf で保存する場合のおまじない
    rcParams['pdf.fonttype'] = 42

    if variable_num == 0:
        last_file_name = "0_main"
    elif variable_num == "period":
        last_file_name = "1_period"
    else:
        last_file_name = "variable"+str(variable_num)
    fig.savefig(last_folder_name+delimiter+last_file_name+".pdf")

for i in range(len(datas)):
    txt_num = i #結合したdatファイルの通し番号
    if len(datas) == 1:
        txt_num = 0 #一つなら通し番号は非表示に
    print(datas[i][0,0])
    np.savetxt(duplicate_rename(last_folder_name+delimiter+"data.txt"), datas[i], fmt='%.5f')

print("XPPtoPDF.py完了")
