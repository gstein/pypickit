#!/usr/bin/python3

import os.path
import contextlib
import marshal

import yaml
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

# Script commands
SCMD_VDD_ON                      = 0xFF
SCMD_VDD_OFF                     = 0xFE
SCMD_VDD_GND_ON                  = 0xFD
SCMD_VDD_GND_OFF                 = 0xFC
SCMD_VPP_ON                      = 0xFB
SCMD_VPP_OFF                     = 0xFA
SCMD_VPP_PWM_ON                  = 0xF9
SCMD_VPP_PWM_OFF                 = 0xF8
SCMD_MCLR_GND_ON                 = 0xF7
SCMD_MCLR_GND_OFF                = 0xF6
SCMD_BUSY_LED_ON                 = 0xF5
SCMD_BUSY_LED_OFF                = 0xF4
SCMD_SET_ICSP_PINS               = 0xF3
SCMD_WRITE_BYTE_LITERAL          = 0xF2
SCMD_WRITE_BYTE_BUFFER           = 0xF1
SCMD_READ_BYTE_BUFFER            = 0xF0
SCMD_READ_BYTE                   = 0xEF
SCMD_WRITE_BITS_LITERAL          = 0xEE
SCMD_WRITE_BITS_BUFFER           = 0xED
SCMD_READ_BITS_BUFFER            = 0xEC
SCMD_READ_BITS                   = 0xEB
SCMD_SET_ICSP_SPEED              = 0xEA
SCMD_LOOP                        = 0xE9
SCMD_DELAY_LONG                  = 0xE8
SCMD_DELAY_SHORT                 = 0xE7
SCMD_IF_EQ_GOTO                  = 0xE6
SCMD_IF_GT_GOTO                  = 0xE5
SCMD_GOTO_INDEX                  = 0xE4
SCMD_EXIT_SCRIPT                 = 0xE3
SCMD_PEEK_SFR                    = 0xE2
SCMD_POKE_SFR                    = 0xE1
SCMD_ICDSLAVE_RX                 = 0xE0
SCMD_ICDSLAVE_TX_LIT             = 0xDF
SCMD_ICDSLAVE_TX_BUF             = 0xDE
SCMD_LOOP_BUFFER                 = 0xDD
SCMD_ICSP_STATES_BUFFER          = 0xDC
SCMD_POP_DOWNLOAD                = 0xDB
SCMD_COREINST18                  = 0xDA
SCMD_COREINST24                  = 0xD9
SCMD_NOP24                       = 0xD8
SCMD_VISI24                      = 0xD7
SCMD_RD2_BYTE_BUFFER             = 0xD6
SCMD_RD2_BITS_BUFFER             = 0xD5
SCMD_WRITE_BUFWORD_W             = 0xD4
SCMD_WRITE_BUFBYTE_W             = 0xD3
SCMD_CONST_WRITE_DL              = 0xD2
SCMD_WRITE_BITS_LIT_HLD          = 0xD1
SCMD_WRITE_BITS_BUF_HLD          = 0xD0
SCMD_SET_AUX                     = 0xCF
SCMD_AUX_STATE_BUFFER            = 0xCE
SCMD_I2C_START                   = 0xCD
SCMD_I2C_STOP                    = 0xCC
SCMD_I2C_WR_BYTE_LIT             = 0xCB
SCMD_I2C_WR_BYTE_BUF             = 0xCA
SCMD_I2C_RD_BYTE_ACK             = 0xC9
SCMD_I2C_RD_BYTE_NACK            = 0xC8
SCMD_SPI_WR_BYTE_LIT             = 0xC7
SCMD_SPI_WR_BYTE_BUF             = 0xC6
SCMD_SPI_RD_BYTE_BUF             = 0xC5
SCMD_SPI_RDWR_BYTE_LIT           = 0xC4
SCMD_SPI_RDWR_BYTE_BUF           = 0xC3
SCMD_ICDSLAVE_RX_BL              = 0xC2
SCMD_ICDSLAVE_TX_LIT_BL          = 0xC1
SCMD_ICDSLAVE_TX_BUF_BL          = 0xC0
SCMD_MEASURE_PULSE               = 0xBF
SCMD_UNIO_TX                     = 0xBE
SCMD_UNIO_TX_RX                  = 0xBD
SCMD_JT2_SETMODE                 = 0xBC
SCMD_JT2_SENDCMD                 = 0xBB
SCMD_JT2_XFERDATA8_LIT           = 0xBA
SCMD_JT2_XFERDATA32_LIT          = 0xB9
SCMD_JT2_XFRFASTDAT_LIT          = 0xB8
SCMD_JT2_XFRFASTDAT_BUF          = 0xB7
SCMD_JT2_XFERINST_BUF            = 0xB6
SCMD_JT2_GET_PE_RESP             = 0xB5
SCMD_JT2_WAIT_PE_RESP            = 0xB4


# Default filename for information about the PIC devices.
DEFAULT_DEVFILE = 'PK2DeviceFile.yaml'


class PICkit:
    def __init__(self):
        self.default_speed = 0

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
        result = self.read(3)
        ### check for bootloader mode
        print('VERSION:', tuple(result))

    def write(self, *values):
        v = bytes(flatten(values))  # ensures all values in [0,255]
        #print('WRITE:', v)
        #if v[0] != FWCMD_FIRMWARE_VERSION: return
        return self.ep_out.write(v)

    def read(self, amt=64):
        ### ignore AMT. read frames are always 64 bytes.
        ### what to do?
        assert amt <= 64
        return bytes(self.ep_in.read(64))[:amt]

    def run_scripts(self, *args):
        flat = flatten(args)
        return self.write(FWCMD_EXECUTE_SCRIPT,
                          len(flat),
                          flat,
                          )

    def vdd_on(self):
        # REFERENCE: CPICkitFunctions::VddOn()
        ### NOTE: assume targetSelfPowered = False
        return self.run_scripts(SCMD_VDD_GND_OFF,
                                SCMD_VDD_ON,
                                )

    def vdd_off(self):
        # REFERENCE: CPICkitFunctions::VddOff()
        ### NOTE: assume targetSelfPowered = False
        return self.run_scripts(SCMD_VDD_OFF,
                                SCMD_VDD_GND_ON,
                                )

    def set_speed(self, speed=None):
        # REFERENCE: CPICkitFunctions::SetProgrammingSpeed()
        if speed is None:
            speed = self.default_speed
        self.run_scripts(SCMD_SET_ICSP_SPEED,
                         speed,
                         )

    def set_vdd(self, voltage, threshold):
        # REFERENCE: CPICkitFunctions::SetVDDVoltage()

        voltage = max(voltage, 2.5)

        ### magic. need explanation
        ccp = int((voltage*32 + 10.5) * 64)
        fault = min((threshold*voltage / 5) * 255, 210.0)

        return self.write(
            FWCMD_SETVDD,
            ccp &  0x0FF,  # low-byte
            ccp // 0x100,  # high-byte
            int(fault),
            )

    def set_vpp(self, voltage, threshold):
        # REFERENCE: CPICkitFunctions::SetVppVoltage()

        ### magic. need explanation
        vppADC = voltage * 18.61
        vFault = threshold * voltage * 1.61

        return self.write(
            FWCMD_SETVPP,
            0x40,  # cppValue
            int(vppADC),
            int(vFault),
            )


class Info:
    def __init__(self, path=None):
        if path is None:
            path = os.path.join(os.path.dirname(__file__),
                                DEFAULT_DEVFILE)

        #print('DEVFILE:', path)
        #import time ; t = time.time()
        mpath = path + '.m'
        if os.path.exists(mpath):
            with open(mpath, 'rb') as mfp:
                data = marshal.load(mfp)
        else:
            data = yaml.load(open(path))
            #print('TIME:', time.time() - t)
            try:
                mfp = open(mpath, 'wb')
            except IOError:
                pass
            else:
                #import pprint ; pprint.pprint(data['info'])
                marshal.dump(data, mfp)
                mfp.close()
        #print('TIME:', time.time() - t)

        #print('DATA:', type(data))
        #print('KEYS:', data.keys())
        vars(self).update(data['info'])
        self.families = data['families']
        self.parts = data['parts']
        self.scripts = data['scripts']


@contextlib.contextmanager
def enable_MCU(pk):
    pk.run_scripts(SCMD_MCLR_GND_ON)
    try:
        pk.vdd_on()
        try:
            yield
        finally:
            pk.vdd_off()
    finally:
        pk.run_scripts(SCMD_MCLR_GND_OFF)


def flatten(v):
    result = [ ]
    for i in v:
        if iterable(i):
            result.extend(flatten(i))
        else:
            result.append(i)
    return result


def iterable(obj):
    try:
        iter(obj)
    except Exception:
        return False
    else:
        return True
