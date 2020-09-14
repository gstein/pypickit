#!/usr/bin/python3
#
# Tool to read PK2DeviceFile.dat
#

import sys
import typing
import struct
import yaml
import pprint


def read(df):
    info = read_object(df, Info)
    # Print attributes in the order they were set.
    #pprint.pprint(list(vars(info).items()))

    families = [ ]
    for i in range(info.NumberFamilies):
        families.append(read_object(df, Family))
        #pprint.pprint(list(vars(families[-1]).items()))

    parts = [ ]
    for i in range(info.NumberParts):
        part = read_object(df, Part)
        part.ConfigMasks.append(part.Config9Mask)
        part.ConfigBlank.append(part.Config9Blank)
        parts.append(part)
        #pprint.pprint(list(vars(part).items()))

    scripts = [ ]
    for i in range(info.NumberScripts):
        scripts.append(read_object(df, Script))
        #pprint.pprint(list(vars(scripts[-1]).items()))

    return info, families, parts, scripts


def read_object(df, cls):
    ob = cls()
    # Note that dictionaries are order-preserving.
    for name, t in typing.get_type_hints(cls).items():
        if cls is Script and name == 'Script':
            # Easiest to special case this one field.
            # Read ob.ScriptLength uint16 values.
            ob.Script = [ ]
            for i in range(ob.ScriptLength):
                v = df.read(uint16.blen)
                ob.Script.append(struct.unpack(uint16.fmt, v)[0])
        elif t is str:
            # Read 1 byte for the string-length.
            l = df.read(1)[0]  # 7 bits of length
            if l > 127:
                # Read 2nd byte (high-order) of the length.
                l = (l & 0x7F) + df.read(1)[0] * 128
            #print(f'{name}: read {l} characters')
            setattr(ob, name, df.read(l).decode())
        elif '_' in name:
            nm, l = name.split('_')
            #print(f'{name}: {l} values of {t.blen} bytes, as "{t.fmt}"')
            vals = [ ]
            for i in range(int(l)):
                v = df.read(t.blen)
                vals.append(struct.unpack(t.fmt, v)[0])
            setattr(ob, nm, vals)
        else:
            #print(f'{name}: {t.blen} as "{t.fmt}"')
            v = df.read(t.blen)
            setattr(ob, name, struct.unpack(t.fmt, v)[0])
    return ob


def make_type(name: str, blen: int, fmt: str):
    t = typing.NewType(name, int)
    t.blen = blen
    t.fmt = fmt
    globals()[name] = t

# The device file is little-endian, so use "<" for all formats.
make_type('int8', 1, '<b')
make_type('int16', 2, '<h')
make_type('int32', 4, '<i')
make_type('uint8', 1, '<B')
make_type('uint16', 2, '<H')
make_type('uint32', 4, '<I')
make_type('df_float', 4, '<f')  # don't overwrite "float"
make_type('df_bool', 1, '<?')  # don't overwrite "bool"


class Info:
    VersionMajor: int32
    VersionMinor: int32
    VersionDot: int32
    Notes: str
    NumberFamilies: int32
    NumberParts: int32
    NumberScripts: int32
    Compatibility: uint8

    UNUSED1A: uint8
    UNUSED1B: uint16
    UNUSED2: uint32


class Family:
    FamilyID: uint16
    FamilyType: uint16
    SearchPriority: uint16
    FamilyName: str
    ProgEntryScript: uint16
    ProgExitScript: uint16
    ReadDevIDScript: uint16
    DeviceIDMask: uint32
    BlankValue: uint32
    BytesPerLocation: uint8
    AddressIncrement: uint8
    PartDetect: df_bool
    ProgEntryVPPScript: uint16
    UNUSED1: uint16
    EEMemBytesPerWord: uint8
    EEMemAddressIncrement: uint8
    UserIDHexBytes: uint8
    UserIDBytes: uint8
    ProgMemHexBytes: uint8
    EEMemHexBytes: uint8
    ProgMemShift: uint8
    TestMemoryStart: uint32
    TestMemoryLength: uint16
    Vpp: df_float


class Part:
    PartName: str
    Family: uint16
    DeviceID: uint32
    ProgramMem: uint32
    EEMem: uint16
    EEAddr: uint32
    ConfigWords: uint8
    ConfigAddr: uint32
    UserIDWords: uint8
    UserIDAddr: uint32
    BandGapMask: uint32
    ConfigMasks_8: uint16
    ConfigBlank_8: uint16
    CPMask: uint16
    CPConfig: uint8
    OSSCALSave: df_bool
    IgnoreAddress: uint32
    VddMin: df_float
    VddMax: df_float
    VddErase: df_float
    CalibrationWords: uint8
    ChipEraseScript: uint16
    ProgMemAddrSetScript: uint16
    ProgMemAddrBytes: uint8
    ProgMemRdScript: uint16
    ProgMemRdWords: uint16
    EERdPrepScript: uint16
    EERdScript: uint16
    EERdLocations: uint16
    UserIDRdPrepScript: uint16
    UserIDRdScript: uint16
    ConfigRdPrepScript: uint16
    ConfigRdScript: uint16
    ProgMemWrPrepScript: uint16
    ProgMemWrScript: uint16
    ProgMemWrWords: uint16
    ProgMemPanelBufs: uint8
    ProgMemPanelOffset: uint32
    EEWrPrepScript: uint16
    EEWrScript: uint16
    EEWrLocations: uint16
    UserIDWrPrepScript: uint16
    UserIDWrScript: uint16
    ConfigWrPrepScript: uint16
    ConfigWrScript: uint16
    OSCCALRdScript: uint16
    OSCCALWrScript: uint16
    DPMask: uint16
    WriteCfgOnErase: df_bool
    BlankCheckSkipUsrIDs: df_bool
    IgnoreBytes: uint16
    ChipErasePrepScript: uint16
    BootFlash: uint32
    Config9Mask: uint16
    Config9Blank: uint16
    ProgMemEraseScript: uint16
    EEMemEraseScript: uint16
    ConfigMemEraseScript: uint16
    reserved1EraseScript: uint16
    reserved2EraseScript: uint16
    TestMemoryRdScript: uint16
    TestMemoryRdWords: uint16
    EERowEraseScript: uint16
    EERowEraseWords: uint16
    ExportToMPLAB: df_bool
    DebugHaltScript: uint16
    DebugRunScript: uint16
    DebugStatusScript: uint16
    DebugReadExecVerScript: uint16
    DebugSingleStepScript: uint16
    DebugBulkWrDataScript: uint16
    DebugBulkRdDataScript: uint16
    DebugWriteVectorScript: uint16
    DebugReadVectorScript: uint16
    DebugRowEraseScript: uint16
    DebugRowEraseSize: uint16
    DebugReserved5Script: uint16
    DebugReserved6Script: uint16
    DebugReserved7Script: uint16
    DebugReserved8Script: uint16
    LVPScript: uint16


class Script:
    ScriptNumber: uint16
    ScriptName: str
    ScriptVersion: uint16
    UNUSED1: uint32
    ScriptLength: uint16
    Script: typing.List[uint16]
    Comment: str


def print_yaml(info, families, parts, scripts):
    data = {
        # Use the instance variable dicts, not the objects
        'info': vars(info),
        'families': [vars(f) for f in families],
        'parts': [vars(p) for p in parts],
        'scripts': [vars(s) for s in scripts],
        }
    ### newer pyyaml could use sort_keys=False. but for now, just override
    ### the representer for "dict" objects. use a list of the items, in
    ### their original/unsorted order.
    def my_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            list(data.items()),
            flow_style=False)
    yaml.add_representer(dict, my_representer)
    yaml.dump(data, sys.stdout, default_flow_style=False)


if __name__ == '__main__':
    data = read(open(sys.argv[1], 'rb'))
    print_yaml(*data)
