＜概要＞
画像をアップロードして、佐々木のぞみ・石原さとみとどのぐらい一致しているかを示す

＜実行手順＞
①「python -m venv "好きなフォルダ名"」を実行して仮想環境の構築を行う
②「"①で決めたフォルダ名"\Scripts\activate」を実行して仮想環境を活動状態にする
③「pip install -r requirements.txt」を実行してモジュール、パッケージのインストール
④「python google_images_download.py -ri - cd "chromedriver.exe" -l "取得する画像の枚数（最大1000）" -k "人物の名前"」をコマンドで実行する。
⑤Originalフォルダにある画像で顔の画像ではないものを手作業で削除する
⑥azureFaceAPI.pyをコマンドで実行する。
⑦学習後はcheckFaceApp_Flaskフォルダ内のapp.pyをコマンドで実行する。
⑧出てきたブラウザ画面に従い判定させたい画像を指定して、「送信」ボタンを押せば結果が表示される

＜各フォルダ・ファイルの説明＞
azure_api:azureFaceAPIにおけるトレーニングとテスト画像との結果の一致度合いを示す、画像をダウンロードするといった機能を有するファイルがある（メイン部分）
azure_env:仮想環境。このフォルダは削除しても良い。

（azure_apiの中身）
checkFaceApp_Flask:Flaskで動かしているアプリケーションが搭載されている。実行部分はapp.pyである
original:google_images_download.pyによってダウンロードした画像が保存される場所
google_images_download.py：画像をダウンロードするときに実行するファイル
chromedriver.exe：google_images_download.pyを実行する際に取得できる枚数を最大100枚から1000枚に拡大するために使用する。
azureFaceAPI.py:PersonGROUPを作成し、学習モデルを構築するためのファイル初めて実行するときはこのファイルを実行してからFlaskでアプリを起動する
person_group_id.pickle:person_group_idを保存している。これを読み込めばどのファイルでも共通のFaceAPIが使用できる
