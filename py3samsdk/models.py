# Execution models for SAM SDK via PySSC
import numpy as np

def run_windmodel(ssc, data):
    # run PV system simulation
    mod = ssc.module_create("windpower")
    ssc.module_exec_set_print(0)
    if ssc.module_exec(mod, data) == 0:
        print('wind power simulation error')
        idx = 1
        msg = ssc.module_log(mod, 0)
        while msg is not None:
            print('\t: ' + str(msg))
            msg = ssc.module_log(mod, idx)
            idx += 1
    else:
        ann = ssc.data_get_number(data, "annual_energy")
        #print('wind power Simulation ok, annual energy (kwh) =', ann)

    ssc.module_free(mod)


def run_pvwattsv5(ssc, data):
    # run PV system simulation
    mod = ssc.module_create("pvwattsv5")
    ssc.module_exec_set_print(0)
    if ssc.module_exec(mod, data) == 0:
        idx = 1
        msg = ssc.module_log(mod, 0)
        while msg is not None:
            print('\t: ' + str(msg))
            msg = ssc.module_log(mod, idx)
            idx += 1
        raise RuntimeError('PVWatts V5 simulation error')
    else:
        ac = np.array([ssc.data_get_array(data, "ac")]) / 1000
        dc = np.array([ssc.data_get_array(data, "dc")]) / 1000

    ssc.module_free(mod)
    return ac, dc
