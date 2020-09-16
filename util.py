#!/usr/bin/python3

import usb.core


### are there other boards out there? using other IDs?
ID_VENDOR = 0x04d8
ID_PRODUCT = 0x0033

# Use the vendor-specific configuration, and endpoints
CONFIG_VENDOR = 2
ENDPOINT_IN = 0x81
ENDPOINT_OUT = 0x01

# Firmware commands for the PICkit
FWCMD_ENTER_BOOTLOADER           = 0x42
FWCMD_NO_OPERATION               = 0x5A
FWCMD_FIRMWARE_VERSION           = 0x76
FWCMD_SETVDD                     = 0xA0
FWCMD_SETVPP                     = 0xA1
FWCMD_READ_STATUS                = 0xA2
FWCMD_READ_VOLTAGES              = 0xA3
FWCMD_DOWNLOAD_SCRIPT            = 0xA4
FWCMD_RUN_SCRIPT                 = 0xA5
FWCMD_EXECUTE_SCRIPT             = 0xA6
FWCMD_CLR_DOWNLOAD_BUFFER        = 0xA7
FWCMD_DOWNLOAD_DATA              = 0xA8
FWCMD_CLR_UPLOAD_BUFFER          = 0xA9
FWCMD_UPLOAD_DATA                = 0xAA
FWCMD_CLR_SCRIPT_BUFFER          = 0xAB
FWCMD_UPLOAD_DATA_NOLEN          = 0xAC
FWCMD_END_OF_BUFFER              = 0xAD
FWCMD_RESET                      = 0xAE
FWCMD_SCRIPT_BUFFER_CHKSM        = 0xAF
FWCMD_WR_INTERNAL_EE             = 0xB1
FWCMD_RD_INTERNAL_EE             = 0xB2


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

        self.write(FWCMD_FIRMWARE_VERSION)
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
