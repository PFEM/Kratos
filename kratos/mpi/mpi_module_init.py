from __future__ import absolute_import
import sys

if sys.platform.startswith('linux'):
    # Note: from Python 3.3 onwards, dll load flags are available from module os
    # from Python 3.6 onwards, module DLFCN no longer exists
    flags = sys.getdlopenflags()
    if sys.version_info >= (3,3):
        import os
        dll_load_flags = os.RTLD_NOW | os.RTLD_GLOBAL
    else:
        import DLFCN as dl
        dll_load_flags = dl.RTLD_NOW | dl.RTLD_GLOBAL
    sys.setdlopenflags(dll_load_flags)

from KratosMPI import *
from .. import legacy_mpi_python_interface

if sys.platform.startswith('linux'):
    # restore default system flags
    sys.setdlopenflags(flags)

mpi = legacy_mpi_python_interface.LegacyMPIPythonInterface()
