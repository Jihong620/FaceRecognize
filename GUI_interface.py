import PySimpleGUI as sg
import numpy as np
from scipy.spatial.distance import cosine
from mtcnn_modules.mtcnn.mtcnn import MTCNN
from tensorflow.keras.models import load_model
import encoding_data
import cv2
from sklearn.preprocessing import Normalizer
import sys

"""
Demo program that displays a webcam using OpenCV
"""

'===== setting ====='
encoder_model = 'facenet_keras.h5'
encodings_path = 'encodings_1.pkl'
# normalize 正規化因子 l2
l2_normalizer = Normalizer('l2')
face_detector = MTCNN(weights_file = 'mtcnn_modules/mtcnn/data/mtcnn_weights.npy')
face_encoder = load_model(encoder_model)
encoding_dict = encoding_data.load_pickle(encodings_path)
'==================='

def recognize(img,detector, encoder, encoding_dict, name='unknown', recognition_t=0.1, confidence_t = 0.99, required_size=(160,160),):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detector.detect_faces(img_rgb)
    for res in results:
        if res['confidence'] < confidence_t:
            continue
        face, pt_1, pt_2 = encoding_data.get_face(img_rgb, res['box'])
        encode = encoding_data.get_encode(encoder, face, required_size)
        encode = l2_normalizer.transform(encode.reshape(1, -1))[0]
        # name = 'unknown'

        # distance = float('inf')
        for db_name, db_encode in encoding_dict.items():
            dist = cosine(db_encode, encode)
            if dist < recognition_t:
                name = db_name
                distance = dist

        if name == 'unknown':
            cv2.rectangle(img, pt_1, pt_2, (0, 0, 255), 2)
            cv2.putText(img, name, pt_1, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        else:
            cv2.rectangle(img, pt_1, pt_2, (0, 255, 0), 2)
            cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 200, 200), 2)
            # cv2.putText(img, name + f'__{distance:.2f}', (pt_1[0], pt_1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1,
            #             (0, 200, 200), 2)
    return img

def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('人臉辨識程式 DEMO', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('開始辨識', size=(10, 1), font='Helvetica 14'),
               sg.Button('儲存影像', size=(10, 1), font='Helvetica 14'),
               sg.Button('中止', size=(10, 1), font='Helvetica 14'),
               sg.Button('離開', size=(10, 1), font='Helvetica 14'),
               sg.Text('PASS!', size=(6, 1),  font='Helvetica 14', background_color='green'),
               sg.Text('NG!', size=(4, 1),  font='Helvetica 14', background_color='red')]]
    # sg.Print('PASS!', text_color='white', background_color='green', font='Helvetica 14')

    # create the window and show it without the plot
    window = sg.Window('人臉辨識程式_210608.v0.1',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = True
    while True:
        event, values = window.read(timeout=20)
        if event == '離開' or event == sg.WIN_CLOSED:
            return

        elif event == '開始辨識':
            recording = True

        elif event == '中止':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        elif event == '儲存影像':
            # 儲存當下影像
            pass
        if recording:
            ret, frame = cap.read()
            frame = recognize(frame, face_detector, face_encoder, encoding_dict)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)

if __name__ =='__main__':
    main()
