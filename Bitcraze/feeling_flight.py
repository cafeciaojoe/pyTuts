import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

from cflib.utils.reset_estimator import reset_estimator

# URI to the Crazyflie to connect to
uri_drone = 'radio://0/90/2M/A0A0A0A0AA' #drone
uri_sensor = 'radio://0/80/2M/A0A0A0A0A8'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

param_set_interval = .01
m1_pwm = False

# Change the sequence according to your setup
#             x    y    z  YAW
sequence = [
    (0.0, 0.0, 0.4, 0),
    (0.0, 0.0, 1.2, 0),
    (0.5, -0.5, 1.2, 0),
    (0.5, 0.5, 1.2, 0),
    (-0.5, 0.5, 1.2, 0),
    (-0.5, -0.5, 1.2, 0),
    (0.0, 0.0, 1.2, 0),
    (0.0, 0.0, 0.4, 0),
]

def param_callback(name, value):
    print('The crazyflie has parameter ' + name + ' set at number: ' + value)

def create_param_callback(scf, groupstr, namestr):
    cf = scf.cf
    full_name = groupstr + '.' + namestr

    cf.param.add_update_callback(group=groupstr, name=namestr,
                                 cb=param_callback)
    time.sleep(param_set_interval)

def change_param(scf, groupstr, namestr, value):
    cf = scf.cf
    full_name = groupstr + '.' + namestr
  
    cf.param.set_value(full_name, value)
    time.sleep(param_set_interval)

def take_off(cf, position):
    take_off_time = 1.0
    sleep_time = 0.1
    steps = int(take_off_time / sleep_time)
    vz = position[2] / take_off_time

    print(f'take off at {position[2]}')

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)


def position_callback(timestamp, data, logconf):
    x = data['kalman.stateX']
    y = data['kalman.stateY']
    z = data['kalman.stateZ']
    print('pos: ({}, {}, {})'.format(x, y, z))


def start_position_printing(scf):
    log_conf = LogConfig(name='Position', period_in_ms=500)
    log_conf.add_variable('kalman.stateX', 'float')
    log_conf.add_variable('kalman.stateY', 'float')
    log_conf.add_variable('kalman.stateZ', 'float')

    scf.cf.log.add_config(log_conf)
    log_conf.data_received_cb.add_callback(position_callback)
    log_conf.start()


def run_sequence(scf_s, scf_d, sequence):
    cf_d = scf_d.cf

    # Arm the Crazyflie
    cf_d.platform.send_arming_request(True)
    time.sleep(1.0)

    take_off(cf_d, sequence[0])
    time.sleep(1.0)

    global m1_pwm

    for position in sequence:
        print('Setting position {}'.format(position))
        for i in range(5):
            cf_d.commander.send_position_setpoint(position[0],
                                                position[1],
                                                position[2],
                                                position[3])
            change_param(scf_s, 'motorPowerSet', 'm1', m1_pwm/2)
            time.sleep(1)

    change_param(scf_s, 'motorPowerSet', 'm1', 0)

    cf_d.commander.send_stop_setpoint()
    # Hand control over to the high level commander to avoid timeout and locking of the Crazyflie
    cf_d.commander.send_notify_setpoint_stop()


    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def log_callback(timestamp, data, logconf):
    #print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    global m1_pwm  # Declare m1_pwm as global to modify it
    if 'motor.m1' in data:
        m1_pwm = data['motor.m1']
        print(f'm1_pwm updated to: {m1_pwm}')
    

def start_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_callback)
    logconf.start()
    time.sleep(3)
    #logconf.stop()

    
if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    log_conf = LogConfig(name='motor', period_in_ms=1000)
    log_conf.add_variable('motor.m1', 'uint16_t')
    log_conf.add_variable('motor.m2', 'uint16_t')
    log_conf.add_variable('motor.m3', 'uint16_t')
    log_conf.add_variable('motor.m4', 'uint16_t')

    with SyncCrazyflie(uri_sensor, cf=Crazyflie(rw_cache='./cache')) as scf_s:
        create_param_callback(scf_s, 'motorPowerSet', 'enable')
        time.sleep(2)
        change_param(scf_s, 'motorPowerSet', 'enable', 1)
        time.sleep(2)
        create_param_callback(scf_s, 'motorPowerSet', 'm1')
        time.sleep(2)
        change_param(scf_s, 'motorPowerSet', 'm1', 20000)
        time.sleep(2)
        change_param(scf_s, 'motorPowerSet', 'm1', 0)
        time.sleep(2)
        with SyncCrazyflie(uri_drone, cf=Crazyflie(rw_cache='./cache')) as scf_d:
            reset_estimator(scf_d)
            start_log_async(scf_d, log_conf)
            #start_position_printing(scf)
            run_sequence(scf_s, scf_d, sequence)

