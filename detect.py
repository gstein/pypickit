#!/usr/bin/python3
#
# Detect the PICkit board, and what MCU is present.
#

import sys

import util




def detect(pk):
    for family in ():
        pk.set_vdd(voltage, 0.85)

        vpp = families[family].Vpp
        if vpp < 1.0:
            # Near zero. Use Vdd voltage.
            pk.set_vpp(vdd, 0.7)
        else:
            pk.set_vpp(vpp, 0.7)

        pk.set_speed()

        with util.enable_MCU(pk):
            time.sleep(0.050)  # wait 50 msec for PIC to power up

            run_script()
            result = read()

        device_id = 0 ### read result
        ### search parts


if __name__ == '__main__':
    pk = util.PICkit()
    info = util.Info()
    #set_vdd(pk, 3.0, 0.85)

    #with util.enable_MCU(pk):
    #    print('DO SOMETHING')
