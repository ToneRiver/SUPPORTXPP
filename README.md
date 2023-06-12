# supportXPPの使い方

このプログラムは，XPP AUTOで出力したall info.datをグラフにするためのプログラムです．

## 初期設定
最初にしてほしいことがいくつかあります．
①supportXPP.pyのソースコードを開き，dat_files_locationという変数を自身の環境に合わせて書き換える．
もし使用osがwindowsじゃないなら→②XPPtoPDF_Re2.pyを開き， delimiterとmyFontという変数を自身の環境に合わせて書き換える．

## 起動方法
このフォルダをターミナル or コマンドプロンプトで開き"python3 supportXPP.py"
と入力して実行するだけです．

## ssample.dat
試用のall info.datファイルです．x軸を[-1,1], y軸も[-1,1]にして出力してみてください．