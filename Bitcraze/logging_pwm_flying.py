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

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

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


def run_sequence(scf, sequence):
    cf = scf.cf

    # Arm the Crazyflie
    cf.platform.send_arming_request(True)
    time.sleep(1.0)

    take_off(cf, sequence[0])
    time.sleep(1.0)

    for position in sequence:
        print('Setting position {}'.format(position))
        for i in range(50):
            cf.commander.send_position_setpoint(position[0],
                                                position[1],
                                                position[2],
                                                position[3])
            time.sleep(0.1)

    cf.commander.send_stop_setpoint()
    # Hand control over to the high level commander to avoid timeout and locking of the Crazyflie
    cf.commander.send_notify_setpoint_stop()

    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    time.sleep(3)
    #logconf.stop()

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    log_conf = LogConfig(name='motor', period_in_ms=10)
    log_conf.add_variable('motor.m1', 'uint16_t')
    log_conf.add_variable('motor.m2', 'uint16_t')
    log_conf.add_variable('motor.m3', 'uint16_t')
    log_conf.add_variable('motor.m4', 'uint16_t')
  
    with SyncCrazyflie(uri_drone, cf=Crazyflie(rw_cache='./cache')) as scf:
        simple_log_async(scf, log_conf)
        reset_estimator(scf)
        #start_position_printing(scf)
        run_sequence(scf, sequence)
        