#https://github.com/orgs/bitcraze/discussions/794

import time
import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

uris = {
    'radio://0/80/2M/E7E7E7E703',
    'radio://0/80/2M/E7E7E7E704',
    # Add more URIs if you want more copters in the swarm
}

def make_uri_dict():
    uri_len = len(uris)

    for key in uris:
        print(key)


def log_async(scf):
    lg_vars = {
        'stateEstimate.x': 'float',
        'stateEstimate.y': 'float',
        'stateEstimate.z': 'float',
        'stateEstimate.roll': 'float',
        'stateEstimate.pitch': 'float',
        'stateEstimate.yaw': 'float',
    }

    lg_stab = LogConfig(name='Position', period_in_ms=100)
    for key in lg_vars:
        lg_stab.add_variable(key, lg_vars[key])

    start_callback(scf, lg_stab)
    for i in range(0,100):
        print('doing stuff, one for each drone',i)
        time.sleep(1)

def start_callback(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    # for i in range(0,100):
    #     print('doing stuff, one for each drone',i)
    #     time.sleep(1)
    logconf.stop()

def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))



def log_sync(scf):
    lg_vars = {
        'stateEstimate.x': 'float',
        'stateEstimate.y': 'float',
        'stateEstimate.z': 'float',
        'stateEstimate.roll': 'float',
        'stateEstimate.pitch': 'float',
        'stateEstimate.yaw': 'float',
    }

    lg_stab = LogConfig(name='Position', period_in_ms=100)
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
        swarm.parallel(log_async)
        print('now i am here')
