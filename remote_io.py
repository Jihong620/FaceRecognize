import time

from pymodbus.client.sync import ModbusTcpClient
# client=ModbusTcpClient(config.io_ip)
# remote_io.voltage_supply(client,channel)

def voltage_supply(client,channel):
    try:
        # 觸發adamio訊號狀態True=1，False=0
        # 信號:綠燈
        if channel == '0' :
            client.write_coil(16, True)  #DO0 ON
            time.sleep()
            client.write_coil(16, False)  #DO0 OFF
        # 信號:紅燈
        elif channel == '1' :
            client.write_coil(17, True) #DO1 ON
            time.sleep(1)
            client.write_coil(17, False)  #DO1 OFF
        # 信號:電子鎖
        elif channel == '2' :
            client.write_coil(18, True) #DO2 ON
            time.sleep(10)
            client.write_coil(18, False)  #DO2 OFF
        # 信號:遮光信號
        elif channel == '3' :
            client.write_coil(19, True) #DO3 ON
            time.sleep(0.1)
            client.write_coil(19, False)  #DO3 OFF
        elif channel == '4' :
            client.write_coil(20, True) #DO4 ON
            time.sleep(0.1)
            client.write_coil(20, False)  #DO4 OFF
        elif channel == '5':
            client.write_coil(21, True) #DO5 ON
            time.sleep(0.1)
            client.write_coil(21, False)  #DO5 OFF
        else:
            print('out of channel !')
    except Exception as err:
        print(err)
