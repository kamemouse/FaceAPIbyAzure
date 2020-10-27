from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person
import os
import io
import sys
import uuid
import time




face_client = FaceClient(
    "https://face-test-maronn.cognitiveservices.azure.com/",
    CognitiveServicesCredentials("c0cc87482dae4261a0fa6b77ac58cc78")
)




PERSON_GROUP_ID = str(uuid.uuid4())

face_client.person_group.create(person_group_id=PERSON_GROUP_ID,name=PERSON_GROUP_ID)

# Define woman friend
ishiharasatomi = face_client.person_group_person.create(person_group_id=PERSON_GROUP_ID,name="石原さとみ")

# Define man friend
sasakinozomi = face_client.person_group_person.create(person_group_id=PERSON_GROUP_ID,name="佐々木のぞみ")


ishiharasatomi_images = os.listdir("Original/ishiharasatomi")
sasakinozomi_images = os.listdir("Original/sasakinozomi")

# Add to a woman person
for image in ishiharasatomi_images:
    try:
        image = "Original/ishiharasatomi/" + image
        i = open(image,"r+b")
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, ishiharasatomi.person_id, i,)
        time.sleep(4)
    except Exception as e:
        print(e)
        time.sleep(4)

    

# Add to a man person
for image in sasakinozomi_images:
    try:
        image = "Original/sasakinozomi/" + image
        s = open(image,"r+b")
        face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, sasakinozomi.person_id, s,name="nozomi")
        time.sleep(4)
    except Exception  as e:
        print(e)
        time.sleep(4)

face_client.person_group.train(PERSON_GROUP_ID)

while(True):
    training_status = face_client.person_group.get_training_status(PERSON_GROUP_ID)
    print("Training status.{}".format(training_status.status))
    if(training_status.status is TrainingStatusType.succeeded):
        break
    elif(training_status.status is TrainingStatusType.failed):
        sys.exit("Trainig the person group has failed")
    time.sleep(5)

file_path = "test/1.jpg"
detect_faces = face_client.face.detect_with_stream(
        open(file_path,mode="rb"),
    )

face_ids = []
for detect_face in detect_faces:
    face_ids.append(detect_face.face_id)

result = face_client.face.identify(face_ids=face_ids, person_group_id=PERSON_GROUP_ID,maxNumOfCandidatesReturned=2)
print(len(result[0].candidates))
# Identify faces
if not result:
    print('一致するグループは存在しませんでした')
for person in result:
    if len(person.candidates) > 0:
        check_name = face_client.person_group_person.get(PERSON_GROUP_ID,person.candidates[0].person_id)
        print('読み込んだ画像は {} に {}% 似ています'.format(check_name.name,person.candidates[0].confidence*100))
        # print('読み込んだ画像は {} に {}% 似ています'.format(check_name.name,person.candidates[1].confidence*100)) # Get topmost confidence score
    else:
        print('一致したグループとの詳細情報を得ることができませんでした。')




