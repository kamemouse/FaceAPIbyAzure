import os
from google_images_download import dir_check
from pykakasi import kakasi

check = dir_check()

kakasi = kakasi()  # Generate kakasi instance
# 日本語をローマ字にする処理
def exchange_word(text):
    kakasi.setMode("H", "a")  # Hiragana to ascii
    kakasi.setMode("K", "a")  # Katakana to ascii
    kakasi.setMode("J", "a")  # Japanese(kanji) to ascii
    conv = kakasi.getConverter()
    result = conv.do(text)
    return result

# Original下のフォルダ名取得
list_all = os.listdir("Original/")
dirs = [f for f in list_all if os.path.isdir(os.path.join("Original/", f))]

# フォルダ名をローマ字化
for i in range(len(dirs)):
    dirs[i] = "Original/" + dirs[i]
    re_dir = exchange_word(dirs[i]) 
    if re_dir != dirs[i]:
        os.rename(dirs[i] ,re_dir)
    else:
        continue

new_dirs = os.listdir("Original")

# ファイル名を取得して名前を0,1,2,3...と数値のみにする処理
for j in range(len(new_dirs)):
    dir = "Original/" + new_dirs[j] + "/"
    files = os.listdir(dir)
    for k in range(len(files)):
        name = dir + files[k]
        rename = dir + str(k) + '.jpg'
        if not new_dirs[j] in check:
            os.rename(name,rename)
        else:
            continue 