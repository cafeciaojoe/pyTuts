#https://github.com/orgs/bitcraze/discussions/794

import time
import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

URI1 = 'radio://0/80/2M/E7E7E7E703'
URI2 = 'radio://0/80/2M/E7E7E7E704'

uris = {
    URI1,
    URI2,
}

def log_sync(scf):
    lg_vars = {
        'gyro.x': 'float',
        'gyro.y': 'float',

    }

    lg_stab = LogConfig(name='Gyro', period_in_ms=100)
    for key in lg_vars:
        lg_stab.add_variable(key, lg_vars[key])

    with SyncLogger(scf, lg_stab) as logger:
        endTime = time.time() + 10

        for log_entry in logger:
            uri = scf.cf.link_uri
            timestamp = log_entry[0]
            data = log_entry[1]
            #print(log_entry)
            print(f'{uri}, {timestamp}, {data}')
            # Do your stuff here

            if time.time() > endTime:
                break


if __name__ == '__main__':

    cflib.crtp.init_drivers(enable_debug_driver=False) # initialize drivers
    factory = CachedCfFactory(rw_cache='./cache')

    with Swarm(uris, factory=factory) as swarm:
        swarm.parallel(log_sync)