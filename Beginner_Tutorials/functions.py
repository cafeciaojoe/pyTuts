scf = 9
scf.gf = 9

def simple_log_async(scf, logconf):
    cf = scf.gf
    cf.log.add_config(logconf)


simple_log_async(1,2)