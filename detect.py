#!/usr/bin/python3
#
# Detect the PICkit board, and what MCU is present.
#

import sys
import pprint
import time
import struct

import util


def detect(pk, info, vdd):
    #for i in range(len(info.families)):
    #    # These values are/should be the same.
    #    print('INDEX:', i, 'ID:', info.families[i]['FamilyID'])
    #pprint.pprint([(f['FamilyName'], f['PartDetect'], f['SearchPriority'],
    #                f['FamilyID'], f['FamilyType'])
    #               for f in info.families])

    # Look for a family that has "PartDetect" enabled. Look for them
    # in order, according to SearchPriority.
    families = sorted((family['SearchPriority'], family)
                      for family in info.families
                      if family['PartDetect'])
    #pprint.pprint([(f['FamilyName'], f['PartDetect'], f['SearchPriority'], f['FamilyID'])
    #               for _, f in families])
    for _, family in families:
        part = detect_in_family(pk, info, family, vdd)
        if part:
            return part


def detect_in_family(pk, info, family, vdd):
    print('FAMILY:', family['FamilyName'])
    #print('FAMILY:', family)

    def run_script(name):
        which = family[name]
        if which == 0:
            return
        script = info.scripts[which - 1]
        #print('SCRIPT:', name, script)
        assert len(script['Script']) == script['ScriptLength']
        cmd = (util.FWCMD_CLR_UPLOAD_BUFFER,
               (util.FWCMD_EXECUTE_SCRIPT,
                len(script['Script']),
                bytes(v & 0xFF for v in script['Script']),
                ),
               )
        #print('CMD:', cmd)
        pk.write(cmd)

    pk.set_vdd(vdd, 0.85)

    vpp = family['Vpp']
    if vpp < 1.0:
        # Near zero. Use Vdd voltage.
        pk.set_vpp(vdd, 0.7)
    else:
        pk.set_vpp(vpp, 0.7)

    # The default speed is fine for detection.
    pk.set_speed()

    with util.enable_MCU(pk):
        time.sleep(0.050)  # wait 50 msec for the PIC to power up

        # Note: auto-detect does not support VPP-first program mode.
        # Just run the programming entry script.
        run_script('ProgEntryScript')
        run_script('ReadDevIDScript')
        pk.write(util.FWCMD_UPLOAD_DATA)
        result = pk.read(5)
        run_script('ProgExitScript')

    print('RESULT:', result)
    # Skip the LENGTH byte. Unpack a 4-byte integer. DeviceIDMask will
    # appropriately mask-off for 2-byte device IDs.
    device_id = ((struct.unpack('<xI', result)[0]
                  >> family['ProgMemShift'])
                 & family['DeviceIDMask'])
    print('DEVICE:', device_id)
    for part in info.parts:
        if part['DeviceID'] == device_id \
           and part['Family'] == family['FamilyID']:
            pprint.pprint(('FOUND:', part))
            return part

    return None


if __name__ == '__main__':
    pk = util.PICkit()
    info = util.Info()

    # Auto-detection uses Vdd=3.0V (if we knew a part, we'd know Vdd/Vpp).
    detect(pk, info, 3.0)
