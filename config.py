# I/O config
# 與 IPC 對接後的設定 IP 位址(非內網)
Adam6052_IPAddress ='169.254.0.1'
channel_green = '0'
channel_red = '1'
channel_lock= '2'
webcam_face = 0
webcam_qrcode = 1
time_set = 15
io_voltage_supply = True
insert_to_db = True
upload_FTP = True
save_local = True

# local config
local_path = r'./result/'
local_wrong_path = r'./result/wrong/'

# GUi_interface_setting
keras_model = 'facenet_keras.h5'
encodings_path = 'encodings_1103.pkl'
# normalize 正規化因子 l2
# l2_normalizer = Normalizer('l2')
face_detector = 'mtcnn_weights.npy'

# aidb config
DBNAME="ai_db"
DBUSERNAME="postgres"
DBPASSWORD="mis-12345"
DBHOST="10.104.2.73"
DBPORT="5432"

# FTP config
ftp_ip = "10.104.2.71"
ftp_name = "tcaiexe"
ftp_password = "mis-12345"
ftp_path = r'/TCAI/CRM2_edge_34/Face_Recognize/'

# SQL command
insert_db_command = "insert into ai_db.img0301raw01(date_time,job_number,img_path,result) VALUES('{}','{}','{}','{}')"


