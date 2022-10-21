import PySimpleGUI as sg
import numpy as np
from mtcnn.mtcnn import MTCNN
# from keras.models import load_model
import cv2
# from sklearn.preprocessing import Normalizer
import Face_recognize_function as frf
from tensorflow.keras.models import load_model
# import time
# import threading
"""
Demo program that displays a webcam using OpenCV
"""

#
# def job():
#     for i in range(5):
#         print("Count thread:",i)
#         time.sleep(1)



def main():

    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('人臉辨識程式 DEMO', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('開始辨識', size=(10, 1), font='Helvetica 14'),
               sg.Button('儲存影像', size=(10, 1), font='Helvetica 14'),
               sg.Button('中止', size=(10, 1), font='Helvetica 14'),
               sg.Button('離開', size=(10, 1), font='Helvetica 14'),
               sg.Text('PASS!',key='PASS', size=(6, 1),  font='Helvetica 14', background_color='green', visible=False),
               sg.Text('NG!',key='NG', size=(4, 1),  font='Helvetica 14', background_color='red',visible=False)]]

    # create the window and show it without the plot
    window = sg.Window('人臉辨識程式_210806', layout, location=(600, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    cap = cv2.VideoCapture(0)
    recording = True
    while True:
        event, values = window.read(timeout=20)
        if event == '離開' or event == sg.WIN_CLOSED:
            break

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
            cv2.imwrite(name+'.jpg',frame)
            print(name+'.jpg saved')

        if recording:
            window['PASS'].update(visible=False)
            window['NG'].update(visible=False)
            ret, frame = cap.read()
            frame, name = frf.recognize(frame, face_detector, face_encoder, encoding_dict)
            # frame, name, light = frf.recognize(frame, face_detector, face_encoder, encoding_dict)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)
            # 顯示 PASS 或 NG, 送訊號開鎖或off

            if name == 'unknown':
                # 紅燈
                # t = threading.Thread(target=job)
                # t.start()
                window['NG'].update(visible=True)
                window['PASS'].update(visible=False)
                # t = threading.Thread(target=job)
                # t.start()
                # print(light)

            elif name[0] == 'U':
                # t = threading.Thread(target=job)
                # t.start()
                # 綠燈
                window['PASS'].update(visible=True)
                window['NG'].update(visible=False)
                # t = threading.Thread(target=job)
                # t.start()

            # elif window['PASS'].visible==True or window['NG'].visible==True:
            #     for i in range(10):
            #         time.sleep(1)
            #     t.join()
            #     window['PASS'].update(visible=False)
            #     window['NG'].update(visible=False)
            # 燈號亮後 10 秒熄滅
            # if window['PASS'].visible==True or window['NG'].visible==True:
            #     # time.sleep(10)
            #     window['PASS'].update(visible=False)
            #     window['NG'].update(visible=False)

    cap.release()
    window.close()


'===== setting ====='
encoder_model = 'facenet_keras.h5'
encodings_path = 'encodings_3.pkl'
# normalize 正規化因子 l2
# l2_normalizer = Normalizer('l2')
face_detector = MTCNN(weights_file='mtcnn_weights.npy')
face_encoder = load_model(encoder_model)
encoding_dict = frf.load_pickle(encodings_path)
timeout = 5.0
'==================='


if __name__ =='__main__':
    main()
