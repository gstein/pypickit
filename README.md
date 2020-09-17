# pypickit
## Python-based PICkit tools

An initial subset of tools normally provided by **PK2CMD**, but modernized
and moved to a Python-based platform for future support.

## Available Tools

### `devfile.py`

TBD

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


