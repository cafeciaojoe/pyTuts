import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.positioning.position_hl_commander import PositionHlCommander

from cflib.utils.reset_estimator import reset_estimator

# # URI to the Crazyflie to connect to
# uri_drone = 'radio://0/90/2M/A0A0A0A0AA' #drone
# uri_sensor = 'radio://0/80/2M/A0A0A0A0A8'

# URI to the Crazyflie to connect to
uri_drone = 'radio://0/90/2M/A0A0A0A0AA' 
uri_sensor = 'radio://0/80/2M/E7E7E7E7E8'

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

def run_sequence(scf_s, scf_d):
    cf_d = scf_d.cf

    # Arm the Crazyflie
    cf_d.platform.send_arming_request(True)
    time.sleep(1.0)

    # https://www.bitcraze.io/documentation/repository/crazyflie-lib-python/master/api/cflib/positioning/position_hl_commander/
    with PositionHlCommander(scf_d, controller=PositionHlCommander.CONTROLLER_PID, default_velocity=.5) as pc:
        pc.go_to(0.0, 0.0, 0.4)
        pc.go_to(0.0, 0.0, 1.2)
        pc.go_to(0.5, -0.5, 1.2)
        pc.go_to(0.5, 0.5, 1.2)
        pc.go_to(-0.5, 0.5, 1.2)
        pc.go_to(-0.5, -0.5, 1.2)
        pc.go_to(0.0, 0.0, 1.2)
        pc.go_to(0.0, 0.0, 0.4)
        # for position in sequence:
        #     print('Setting position {}'.format(position))
        #     for i in range(25):
        #         cf_d.commander.send_position_setpoint(position[0],
        #                                             position[1],
        #                                             position[2],
        #                                             position[3])
        #         time.sleep(0.1)
        
        # for _ in range(30):
        #     # Continuously send the zero setpoint until the drone is recognized as landed
        #     # to prevent the supervisor from intervening due to missing regular setpoints
        #     cf_d.commander.send_setpoint(0, 0, 0, 0)
        #     time.sleep(0.1)

        change_param(scf_s, 'motorPowerSet', 'm1', 0)
        change_param(scf_s, 'motorPowerSet', 'm2', 0)
        change_param(scf_s, 'motorPowerSet', 'm3', 0)
        change_param(scf_s, 'motorPowerSet', 'm4', 0)

    cf_d.commander.send_stop_setpoint()
    # Hand control over to the high level commander to avoid timeout and locking of the Crazyflie
    cf_d.commander.send_notify_setpoint_stop()

    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)

def amplify_and_send_motors(scf_s, m_values, center=32768, amplification_factor=1.0, power=1, idle_threshold=1000):
    avg = sum(m_values) / 4.0
    if avg < idle_threshold:
        # Drone is not flying, set all motors to zero
        amplified = [0, 0, 0, 0]
    else:
        amplified = []
        for m in m_values:
            diff = m - avg
            # Amplify difference (optionally non-linear)
            amp = center + amplification_factor * (diff ** power if diff >= 0 else -((-diff) ** power))
            # Clamp to valid PWM range
            amp = max(0, min(65535, int(amp)))
            amplified.append(amp)
    # Send to sensor
    change_param(scf_s, 'motorPowerSet', 'm1', amplified[0])
    change_param(scf_s, 'motorPowerSet', 'm2', amplified[1])
    change_param(scf_s, 'motorPowerSet', 'm3', amplified[2])
    change_param(scf_s, 'motorPowerSet', 'm4', amplified[3])

# Then, update your log_callback:
def log_callback(timestamp, data, logconf):
    m_keys = ['motor.m1', 'motor.m2', 'motor.m3', 'motor.m4']
    if all(k in data for k in m_keys):
        m_values = [data[k] for k in m_keys]
        amplify_and_send_motors(scf_s, m_values, center=32768, amplification_factor=12.0, power=1)

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

    log_conf = LogConfig(name='motor', period_in_ms=200)
    log_conf.add_variable('motor.m1', 'uint16_t')
    log_conf.add_variable('motor.m2', 'uint16_t')
    log_conf.add_variable('motor.m3', 'uint16_t')
    log_conf.add_variable('motor.m4', 'uint16_t')

    with SyncCrazyflie(uri_sensor, cf=Crazyflie(rw_cache='./cache')) as scf_s:
        create_param_callback(scf_s, 'motorPowerSet', 'enable')
        time.sleep(1)
        change_param(scf_s, 'motorPowerSet', 'enable', 1)
        time.sleep(1)
        create_param_callback(scf_s, 'motorPowerSet', 'm1')
        time.sleep(1)
        create_param_callback(scf_s, 'motorPowerSet', 'm2')
        time.sleep(1)
        create_param_callback(scf_s, 'motorPowerSet', 'm3')
        time.sleep(1)
        create_param_callback(scf_s, 'motorPowerSet', 'm4')
        time.sleep(1)
        change_param(scf_s, 'motorPowerSet', 'm1', 20000)
        time.sleep(1)
        change_param(scf_s, 'motorPowerSet', 'm1', 0)
        time.sleep(1)
        with SyncCrazyflie(uri_drone, cf=Crazyflie(rw_cache='./cache')) as scf_d:
            reset_estimator(scf_d)
            start_log_async(scf_d, log_conf)
            #start_position_printing(scf)
            run_sequence(scf_s, scf_d)
            time.sleep(1)



