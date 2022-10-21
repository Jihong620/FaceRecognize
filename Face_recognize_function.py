import pickle
from sklearn.preprocessing import Normalizer
import cv2
import numpy as np
from scipy.spatial.distance import cosine
import config
import remote_io
from pymodbus.client.sync import ModbusTcpClient
import time

# normalize 正規化因子 l2
l2_normalizer = Normalizer('l2')
client = ModbusTcpClient(config.Adam6052_IPAddress)
client.is_socket_open()
def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict

def normalize(img):
    mean, std = img.mean(), img.std()
    return (img - mean) / std

# get encode
def get_encode(face_encode, face, size):
    face = normalize(face)
    face = cv2.resize(face, size)
    encode = face_encode.predict(np.expand_dims(face, axis=0))[0]
    return encode

# extract face
def get_face(img, box):
    x1, y1, width, height = box
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height
    face = img[y1:y2, x1:x2]
    return face, (x1,y1), (x2,y2)

# star recognize
def recognize(img,detector, encoder, encoding_dict, name='unknown', recognition_t=0.15, confidence_t = 0.99, required_size=(160,160)):

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = get_face(img_rgb, res['box'])
        encode = get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        # name = 'unknown'

        # distance = float('inf')
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t:
                name = db_name
                distance = 100 - dist

        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
            print(name,'NG')
            # result = 'NG'
            # cv2.imwrite(time.strftime('%Y%m%d%H%M%S', time.localtime()) + name + '.jpg', img)
            # filename = time.strftime("%Y%m%d") + '/' + time.strftime("%Y%m%d%H%M%S") + ".jpg"  # 顯示用暫存影像名稱
            # filename_ftp = time.strftime("%Y%m%d%H%M%S") + ".jpg"  # 顯示用暫存影像名稱
            # cv2.imwrite(r"./temp/temp_pic.jpg", img)  # 辨識用暫存影像
            #
            # remote_io.voltage_supply(client, config.channel_red)
            # client.write_coil(16, False)
                # 紅燈信號
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name + f'_{distance:.2f}'+'%', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 200, 200), 2)
            print(name,'PASS')
    return img,name

