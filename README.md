# py3samsdk
Python 3 wrapper for NREL's System Advisor Model SDK.

At the moment, this package is compatible with the March 14, 2016 SAM SDK release.  The core interface is a modified version of NREL's Python 2 API.


## Using the package
* Install the [NREL System SAM SDK](https://sam.nrel.gov)
* Find the system library (ssc.dylib, ssc.so, ssc.dll) and copy to your Python path
* Install the py3samsdk package

```python
from py3samsdk import PySSC

ssc_lib = './ssc.dylib'  # path to SAM SSC Library
ssc = PySSC(ssc_lib)
```

### Running tests
Note that the ssc_lib must be inside the root package directory for the tests to pick up the module.

## Notes
* The API package API may change rapidly.
* Some scheduled improvements are to improve the library path mechanism and to set up continuous testing/integration.

