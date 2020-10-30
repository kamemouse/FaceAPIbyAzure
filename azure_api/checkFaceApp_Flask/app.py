# -*- coding: utf-8 -*- 
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
from PIL import Image, ImageDraw
import os
import io
import sys
import uuid
import time
import pickle
from flask import Flask,render_template,request,redirect
app = Flask(__name__)
DIR = "static/img/"


# 対象の人の名前を取得
# searchNameList = os.listdir("../test/")
# 名前を日本語で表示させたいときはtestフォルダの順番通りに名前をリストで記述する
searchNameList = ["石原さとみ","佐々木のぞみ"]

# Face APIを使用するためにFaceClientをインスタンス化している
face_client = FaceClient(
    "https://face-test-maronn.cognitiveservices.azure.com/",
    CognitiveServicesCredentials("c0cc87482dae4261a0fa6b77ac58cc78")
)

# 学習モデルを参照するのに必要なIDを取得
with open("../person_group_id.pickle",'rb') as id:
    PERSON_GROUP_ID = pickle.load(id) 

# 顔の範囲を座標指定する関数
def getRectangle(faceDictionary):
    rect = faceDictionary.face_rectangle
    left = rect.left
    top = rect.top
    right = left + rect.width
    bottom = top + rect.height
    
    return ((left, top), (right, bottom))


@app.route('/',methods=['GET','POST'])
def check_img():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/check',methods=['GET','POST'])
def check_answer():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # フォームからファイル情報を取得
        img = request.files['img']
        # 画像を保存し、保存した画像の名前を取得
        img.save(os.path.join(DIR,img.filename))
        name = os.path.join(DIR,img.filename)
        # テスト画像を読み込み学習モデルと比較出来るように画像のIDを取得する。face_client.face.detect_with_streamによって顔を識別した上で読み込んでくれる・
        detect_faces = face_client.face.detect_with_stream(
                open(name,mode="rb"),recognition_model='recognition_03'
            )

        print(len(detect_faces))
        # 単一の画像のみ読み込めるようにする
        if len(detect_faces) > 1:
            error = "複数の顔が存在する画像は対応していません。別の画像を用いてください"
            return render_template('check.html',error=error,name=name)
        elif len(detect_faces) == 1:
            face_ids = [detect_faces[0].face_id]
        else:
            error = "顔が検出できませんでした。別の画像を用いてください"
            return render_template('check.html',error=error,name=name)
        
        
        # 学習モデルとテスト画像を比較して顔判別グループ内の各Personグループとの一致度合いを調べる
        result = face_client.face.identify(face_ids=face_ids, person_group_id=PERSON_GROUP_ID,max_num_of_candidates_returned=2,confidence_threshold=0.01)

        # 画像の顔部分に枠線を引くためにImageを使って読み込み、ImageDraw.Drawと関数getRectangleを使って描画する
        img_rect = Image.open(name)
        draw = ImageDraw.Draw(img_rect)
        for face in detect_faces:
            draw.rectangle(getRectangle(face), outline='red')
        img_rect.save(os.path.join(DIR,img.filename))


        # 結果の表示
        if not result:
            error = '一致するグループは存在しませんでした'
            return render_template('check.html',error=error,name=name)

        elif len(result[0].candidates) > 0:
            # 各resultグループの名前を取得するための処理
            check_name_high = face_client.person_group_person.get(PERSON_GROUP_ID,result[0].candidates[0].person_id)
            check_name_low = face_client.person_group_person.get(PERSON_GROUP_ID,result[0].candidates[1].person_id)
            # 結果の表示部分
            high_confi = '読み込んだ画像は' + check_name_high.name + 'に'+ str(result[0].candidates[0].confidence*100) + '% 似ています'
            low_confi ='読み込んだ画像は' + check_name_low.name + 'に'+ str(result[0].candidates[1].confidence*100) + '% 似ています' # Get topmost confidence score

            return render_template('check.html',high_confi=high_confi,low_confi=low_confi,name=name)
            
        else:
            error = '一致したグループとの詳細情報を得ることができませんでした。'
            return render_template('check.html',error=error,name=name)
        



if __name__ == "__main__":
    app.run(debug=True)


