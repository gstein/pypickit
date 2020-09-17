# pypickit
## Python-based PICkit tools

An initial subset of tools normally provided by **PK2CMD**, but modernized
and moved to a Python-based platform for future support.

## Available Tools

### `devfile.py`

This tool can transform any device data file that you have, into a YAML
file for consumption by `pypickit`.

There is already a `PK2DeviceFile.yaml` provided in this repository,
so you may not need to use this script. If you have some newer chips,
or need some device data corrections that are contained in your `.dat`
file, then this could be useful.

It appears there are some recent device additions, updates, and corrections,
managed over at the PICKitPlus project. `devfile.py` will produce a `.yaml` for
use by this package. That project is located at:
https://sourceforge.net/projects/pickit3plus/files/

### `detect.py`

TBD


## Dependencies

On Ubuntu
```
# apt install python3-yaml libusb1-dev
```
```
$ python3 -m pip install pyusb
```

## References

The MicroChip PICkit2 and PICkit3 tooling is deprecated. A snapshot of the
all-important **PK2CMD** package is located at:
https://github.com/psmay/pk2cmd

**NOTE**: PK2CMD is **NOT** Open Source. Thus, `pypickit`
includes no source derived from PK2CMD.

Using PK2CMD on Ubuntu, rather than `pypickit`:
* https://andrewmemory.wordpress.com/2020/01/08/programing-with-a-pickit-2-on-linux/
* https://blog.toonormal.com/2016/01/26/using-a-pickit2-on-linux/


## License

This package is licensed under the Apache License, v2.0.

No code has been incorporated from the PK2CMD application.

The `Pk2DeviceFile.yaml` contains device data, presented in a new format
and arrangement, and offered under ALv2.


