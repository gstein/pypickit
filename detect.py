#!/usr/bin/python3
#
# Detect the PICkit board, and what MCU is present.
#

import sys

import usb.core  # python3 -m pip install pyusb

import util


### are there other boards out there? using other IDs?
ID_VENDOR = 0x04d8
ID_PRODUCT = 0x0033

# Use the vendor-specific configuration, and endpoints
CONFIG_VENDOR = 2
ENDPOINT_IN = 0x81
ENDPOINT_OUT = 0x01


class PICkit:
    def __init__(self):
        ### multiple programmers on the bus? f'it. assume one.
        self.device = usb.core.find(idVendor=ID_VENDOR,
                                    idProduct=ID_PRODUCT)
        #print('FOUND:', self.device)

        ### Ignore the various race/reset issues with configurations
        ### http://libusb.sourceforge.net/api-1.0/libusb_caveats.html#configsel
        self.device.set_configuration(CONFIG_VENDOR)

        interface = self.device.get_active_configuration()[0,0]
        endpoints = interface.endpoints()

        ### for now, don't worry about !=2 endpoints
        assert len(endpoints) == 2
        if endpoints[0].bEndpointAddress == ENDPOINT_IN:
            self.ep_in = endpoints[0]
            self.ep_out = endpoints[1]
        else:
            self.ep_in = endpoints[1]
            self.ep_out = endpoints[0]
        assert self.ep_in.bEndpointAddress == ENDPOINT_IN
        assert self.ep_out.bEndpointAddress == ENDPOINT_OUT

        ### claim the interface?

        self.write(util.FWCMD_FIRMWARE_VERSION)
        result = self.read(8)
        ### check for bootloader mode
        print('VERSION:', tuple(result)[:3])

    def write(self, cmd, *values):
        v = bytes((cmd,) + values)  # ensures all values in [0,255]
        print('WRITE:', v)
        return self.ep_out.write(v)

    def read(self, amt):
        ### ignore AMT. read frames are always 64 bytes.
        ### what to do?
        assert amt <= 64
        return bytes(self.ep_in.read(64))[:amt]


def set_vdd(pk, voltage, threshold):
    # REFERENCE: CPICkitFunctions::SetVDDVoltage

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
    # REFERENCE: CPICkitFunctions::SetVppVoltage

    # magic
    vppADC = voltage * 18.61
    fault = threshold * voltage * 1.61

    return pk.write(
        util.FWCMD_SETVPP,
        0x40,  # cppValue
        vppADC,
        vFault,
        )


def detect(pk):
    set_vdd(pk, voltage, 0.85)
    return

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
    pk = PICkit()
    #set_vdd(pk, 3.0, 0.85)
