import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/A0A0A0A0A9'
latest_cf_sensor_data = False


# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def log_stab_callback(timestamp, data, logconf):
    #print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    global latest_cf_sensor_data
    latest_cf_sensor_data = data
    """adding the timestam to the latest sensor data dict"""
    latest_cf_sensor_data['timestamp'] = timestamp
    #print(timestamp)

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    print('logconf_started')
    last_timestamp = 0
    while True:
        if latest_cf_sensor_data is not False:
            if last_timestamp < latest_cf_sensor_data['timestamp']:
                #print(latest_cf_sensor_data['timestamp'])
                
                last_timestamp = latest_cf_sensor_data['timestamp']
    logconf.stop()

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='stateEstimate', period_in_ms=1000)
    lg_stab.add_variable('stateEstimate.x', 'float')
    lg_stab.add_variable('stateEstimate.y', 'float')
    lg_stab.add_variable('stateEstimate.z', 'float')

    lg_stab.add_variable('stateEstimate.roll', 'float')
    lg_stab.add_variable('stateEstimate.pitch', 'float')
    lg_stab.add_variable('stateEstimate.yaw', 'float')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf_2:
            simple_log_async(scf, lg_stab, scf_2)
