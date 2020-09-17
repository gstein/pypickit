#!/usr/bin/python3
#
# Detect the PICkit board, and what MCU is present.
#

import sys

import util


def set_vdd(pk, voltage, threshold):
    # REFERENCE: CPICkitFunctions::SetVDDVoltage(...)

    voltage = max(voltage, 2.5)

    # magic
    ccp = int((voltage*32 + 10.5) * 64)
    fault = int(min((threshold*voltage / 5) * 255, 210.0))

    return pk.write(
        util.FWCMD_SETVDD,
        ccp &  0x0FF,  # low-byte
        ccp // 0x100,  # high-byte
        fault,
        )


def set_vpp(pk, voltage, threshold):
    # REFERENCE: CPICkitFunctions::SetVppVoltage(...)

    # magic
    vppADC = voltage * 18.61
    vFault = threshold * voltage * 1.61

    return pk.write(
        util.FWCMD_SETVPP,
        0x40,  # cppValue
        int(vppADC),
        int(vFault),
        )


def detect(pk):
    set_vdd(pk, voltage, 0.85)

    vpp = families[family].Vpp
    if vpp < 1.0:
        # Near zero. Use Vdd voltage.
        set_vpp(vdd, 0.7)
    else:
        set_vpp(vpp, 0.7)

    set_speed()
    set_MCLR(True)
    turn_on_vdd()
    time.sleep(50)  ### units??
    run_script()
    turn_off_vdd()
    set_MCLR(False)
    device_id = 0 ### read result
    ### search parts


if __name__ == '__main__':
    pk = util.PICkit()
    #set_vdd(pk, 3.0, 0.85)

    #with util.enable_MCU(pk):
    #    print('DO SOMETHING')
