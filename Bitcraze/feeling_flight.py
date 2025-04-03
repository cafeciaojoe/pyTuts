import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/A0A0A0A0A8'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

param_set_interval = .01


def param_callback(name, value):
    print('The crazyflie has parameter ' + name + ' set at number: ' + value)

def motor_power(scf, groupstr, namestr, value):
    cf = scf.cf
    full_name = groupstr + '.' + namestr

    cf.param.add_update_callback(group=groupstr, name=namestr,
                                 cb=param_callback)
    time.sleep(param_set_interval)

    if namestr == 'enable':
        cf.param.set_value(full_name, value)
        time.sleep(param_set_interval)

    else:
        pwm = int((value/100)*65535)
        print(pwm)
        cf.param.set_value(full_name, pwm)
        time.sleep(param_set_interval)

    
if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
    lg_stab.add_variable('stabilizer.roll', 'float')
    lg_stab.add_variable('stabilizer.pitch', 'float')
    lg_stab.add_variable('stabilizer.yaw', 'float')

    power = 50 #as a percentage

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        motor_power(scf, 'motorPowerSet', 'enable', 1)
        # time.sleep(3)
        # motor_power(scf, 'motorPowerSet', 'm1', 20)
        # time.sleep(3)
        # motor_power(scf, 'motorPowerSet', 'm1', 0)
        # time.sleep(3)

        for i in range (1,101):
            motor_power(scf, 'motorPowerSet', 'm1', i)
            time.sleep(param_set_interval)
            
        motor_power(scf, 'motorPowerSet', 'm1', 0)


