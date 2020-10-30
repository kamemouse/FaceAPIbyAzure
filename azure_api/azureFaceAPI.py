from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import os
import io
import sys
import uuid
import time
import pickle



# Face APIを使用するためにFaceClientをインスタンス化している
face_client = FaceClient(
    "https://face-test-maronn.cognitiveservices.azure.com/",
    CognitiveServicesCredentials("c0cc87482dae4261a0fa6b77ac58cc78")
)



# 顔判別のグループ全体の名前を決めるためにほぼ重複しない文字列を指定する
PERSON_GROUP_ID = str(uuid.uuid4())
with open('person_group_id.pickle', 'wb') as id:
  pickle.dump(PERSON_GROUP_ID , id)

# 顔判別のグループを作成する
face_client.person_group.create(person_group_id=PERSON_GROUP_ID,name=PERSON_GROUP_ID,recognition_model='recognition_03')

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





