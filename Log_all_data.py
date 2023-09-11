import logging
import time
from numpy import savetxt
import numpy as np
import csv
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from sys import exit

URI = 'radio://0/80/2M/E7E7E7E7E7'
DEFAULT_HEIGHT = 0.5

is_deck_attached = True

logging.basicConfig(level=logging.ERROR)
i=0
ranging_distances = [0,0,0,0,0,0,0]
ranging_distances3=[0,0]
imu_measurements=[0,0,0]
imu_acc=[0,0,0]
def move_linear_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(0.1)
        mc.up(0.2)
        time.sleep(1)
        mc.down(0.5)
        time.sleep(1)
   


def take_off_simple(scf):
    ...

def log_pos_callback(timestamp, data, logconf):
    print(data)
    global ranging_distances,ranging_distances2, i
    i=i+1
    if i%2==0:
        ranging_distances2 = [timestamp,data['ranging.distance7'],data['ranging.distance0'],data['ranging.distance1'],data['ranging.distance2'],data['ranging.distance3'],data['ranging.distance4']]
        ranging_distances=np.append(ranging_distances, ranging_distances2)
    else:
        ranging_distances2 = [timestamp,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
        ranging_distances=np.append(ranging_distances, ranging_distances2)

def log_pos_callback4(timestamp, data, log2):
    print(data)
    global ranging_distances3,ranging_distances4
    if i%2==0:
        ranging_distances4= [data['ranging.distance5'],data['ranging.distance6']]
        ranging_distances3=np.append(ranging_distances3, ranging_distances4)
    else:
        ranging_distances4= [np.nan,np.nan]
        ranging_distances3=np.append(ranging_distances3, ranging_distances4)
def log_pos_callback2(timestamp, data, log_conf):
    print(data)
    global imu_measurements,imu
    imu = [data['gyro.x'],data['gyro.y'],data['gyro.z']]
    imu_measurements=np.append(imu_measurements,imu)

def log_pos_callback3(timestamp, data, log_conf2):
    print(data)
    global imu_acc,acc1
    acc1= [data['acc.x'],data['acc.y'],data['acc.z']]
    imu_acc=np.append(imu_acc,acc1)
  
def param_deck_flow(name, value_str):
    ...

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        try:
            scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
            time.sleep(1)

            logconf = LogConfig(name='ranging', period_in_ms=10)
            logconf.add_variable('ranging.distance0', 'float')
            logconf.add_variable('ranging.distance1', 'float')
            logconf.add_variable('ranging.distance2', 'float')
            logconf.add_variable('ranging.distance3', 'float')
            logconf.add_variable('ranging.distance4', 'float')
            logconf.add_variable('ranging.distance7', 'float')
            scf.cf.log.add_config(logconf)
            logconf.data_received_cb.add_callback(log_pos_callback)
            log2 = LogConfig(name='ranging', period_in_ms=10)
            log2.add_variable('ranging.distance5', 'float')
            log2.add_variable('ranging.distance6', 'float')
            scf.cf.log.add_config(log2)
            log2.data_received_cb.add_callback(log_pos_callback4)
            log_conf=LogConfig(name='gyro',period_in_ms=10)
            log_conf.add_variable('gyro.x', 'float')
            log_conf.add_variable('gyro.y', 'float')
            log_conf.add_variable('gyro.z', 'float')
            scf.cf.log.add_config(log_conf)
            log_conf.data_received_cb.add_callback(log_pos_callback2)
            log_conf2=LogConfig(name='acc',period_in_ms=10)
            log_conf2.add_variable('acc.x', 'float')
            log_conf2.add_variable('acc.y', 'float')
            log_conf2.add_variable('acc.z', 'float')
            scf.cf.log.add_config(log_conf2)
            log_conf2.data_received_cb.add_callback(log_pos_callback3)
        

        except KeyboardInterrupt:
               # User interrupt the program with ctrl+c
            exit()
  

        if is_deck_attached:
            logconf.start()
            log2.start()
            log_conf.start()
            log_conf2.start()
            time.sleep(2)
            #move_linear_simple(scf)
            logconf.stop()

        n1=len(ranging_distances)/7
        ranging_distances=np.reshape(ranging_distances,(int(n1),7))
        ranging_distances3=np.reshape(ranging_distances3,(int(len(ranging_distances3)/2),2))
        imu_measurements=np.reshape(imu_measurements,(int(len(imu_measurements)/3),3))
        arr3=np.reshape(imu_acc,(int(len(imu_acc)/3),3))
        arr=np.append(ranging_distances,ranging_distances3,axis=1)
        arr1=np.append(arr,imu_measurements,axis=1)
        arr2=np.append(arr1,arr3,axis=1)
        savetxt('combineddata.csv',arr2,delimiter=',')

