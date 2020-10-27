from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import os
import io
import sys
import uuid
import time



# Face APIを使用するためにFaceClientをインスタンス化している
face_client = FaceClient(
    "https://face-test-maronn.cognitiveservices.azure.com/",
    CognitiveServicesCredentials("c0cc87482dae4261a0fa6b77ac58cc78")
)



# 顔判別のグループ全体の名前を決めるためにほぼ重複しない文字列を指定する
PERSON_GROUP_ID = str(uuid.uuid4())

# 顔判別のグループを作成する
face_client.person_group.create(person_group_id=PERSON_GROUP_ID,name=PERSON_GROUP_ID)

# 顔判別のグループ内の1グループをそれぞれ「石原さとみ」、「佐々木のぞみ」という名前で作成した
ishiharasatomi = face_client.person_group_person.create(person_group_id=PERSON_GROUP_ID,name="石原さとみ")
sasakinozomi = face_client.person_group_person.create(person_group_id=PERSON_GROUP_ID,name="佐々木のぞみ")


# 保存してあるトレーニング用の画像ファイルを取得
ishiharasatomi_images = os.listdir("Original/ishiharasatomi")
sasakinozomi_images = os.listdir("Original/sasakinozomi")

# "Original/ishiharasatomiの下に保存してある画像を「石原さとみ」グループに追加する
for image in ishiharasatomi_images:
    try:
        image = "Original/ishiharasatomi/" + image
        i = open(image,"r+b")
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, ishiharasatomi.person_id, i,)
        # FaceAPIの利用制限による処理の中止を回避するために間隔を空ける
        time.sleep(4)
    # 顔の読み込みが不可能などといったエラーによって処理が止まることを防ぐために例外処理を行う
    except Exception as e:
        print(e)
        time.sleep(4)

    

# 上部のfor文と処理内容は同じ。パスのみ異なる
for image in sasakinozomi_images:
    try:
        image = "Original/sasakinozomi/" + image
        s = open(image,"r+b")
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, sasakinozomi.person_id, s,name="nozomi")
        time.sleep(4)
    except Exception  as e:
        print(e)
        time.sleep(4)

# 顔判別グループをトレーニングして学習モデルを作成する
face_client.person_group.train(PERSON_GROUP_ID)

# 現在のトレーニング状態を表示
while(True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status.{}".format(training_status.status))
    if(training_status.status is TrainingStatusType.succeeded):
        break
    elif(training_status.status is TrainingStatusType.failed):
        sys.exit("Trainig the person group has failed")
    time.sleep(5)

# テスト画像を読み込み学習モデルと比較出来るように画像のIDを取得する。face_client.face.detect_with_streamによって顔を識別した上で読み込んでくれる・
file_path = "test/1.jpg"
detect_faces = face_client.face.detect_with_stream(
        open(file_path,mode="rb"),
    )
face_ids = [detect_face.face_id]

# 学習モデルとテスト画像を比較して顔判別グループ内の各Personグループとの一致度合いを調べる
result = face_client.face.identify(face_ids=face_ids, person_group_id=PERSON_GROUP_ID,max_num_of_candidates_returned=2,confidence_threshold=0.01)


# 結果の表示
if not result:
    print('一致するグループは存在しませんでした')
for person in result:
    if len(person.candidates) > 0:
        # 各Personグループの名前を取得するための処理
        check_name_high = face_client.person_group_person.get(PERSON_GROUP_ID,person.candidates[0].person_id)
        check_name_low = face_client.person_group_person.get(PERSON_GROUP_ID,person.candidates[1].person_id)
        # 結果の表示部分
        print('読み込んだ画像は {} に {}% 似ています'.format(check_name_high.name,person.candidates[0].confidence*100))
        print('読み込んだ画像は {} に {}% 似ています'.format(check_name_low.name,person.candidates[1].confidence*100)) # Get topmost confidence score
    else:
        print('一致したグループとの詳細情報を得ることができませんでした。')




