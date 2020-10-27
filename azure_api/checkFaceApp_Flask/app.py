# -*- coding: utf-8 -*- 
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
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
                open(name,mode="rb"),
            )
        face_ids = [detect_faces[0].face_id]
        # 学習モデルとテスト画像を比較して顔判別グループ内の各Personグループとの一致度合いを調べる
        result = face_client.face.identify(face_ids=face_ids, person_group_id=PERSON_GROUP_ID,max_num_of_candidates_returned=2,confidence_threshold=0.01)

        # 結果の表示
        if not result:
            print('一致するグループは存在しませんでした')
            return render_template('check.html',error=error)

        elif len(result[0].candidates) > 0:
            # 各resultグループの名前を取得するための処理
            check_name_high = face_client.person_group_person.get(PERSON_GROUP_ID,result[0].candidates[0].person_id)
            check_name_low = face_client.person_group_person.get(PERSON_GROUP_ID,result[0].candidates[1].person_id)
            # 結果の表示部分
            high_confi = '読み込んだ画像は' + check_name_high.name + 'に'+ str(result[0].candidates[0].confidence*100) + '% 似ています'
            low_confi ='読み込んだ画像は' + check_name_low.name + 'に'+ str(result[0].candidates[1].confidence*100) + '% 似ています' # Get topmost confidence score

            return render_template('check.html',high_confi=high_confi,low_confi=low_confi)
            
        else:
            error = '一致したグループとの詳細情報を得ることができませんでした。'
            return render_template('check.html',error=error)
        



if __name__ == "__main__":
    app.run(debug=True)


