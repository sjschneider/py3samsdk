# #####################################################################
#
#   System Simulation Core (SSC) Python Wrapper
#   Author: Aron Dobos @ NREL and Steven Janzou @ NREL
#   Contributions: Stephen Schneider <stesch@alumni.stanford.edu>
#
# #####################################################################


import string, sys, struct, os
from ctypes import *
import numpy
from py3samsdk.decorators import sam_ctypes


c_number = c_float  # must be c_double or c_float depending on how defined in sscapi.h


class PySSC:
    """A Python 3 wrapper for the SAM SDk"""
    # Constants
    INVALID = 0
    STRING = 1
    NUMBER = 2
    ARRAY = 3
    MATRIX = 4

    INPUT = 1
    OUTPUT = 2
    INOUT = 3

    def __init__(self, dll_dir=""):
        try:
            if sys.platform == 'win32' or sys.platform == 'cygwin':
                if 8*struct.calcsize("P") == 64:
                    self.pdll = CDLL(dll_dir + "ssc.dll")
                else:
                    self.pdll = CDLL(dll_dir + "ssc.dll")
            elif sys.platform == 'darwin':
                self.pdll = CDLL(dll_dir + "ssc.dylib")
            elif sys.platform == 'linux2':
                self.pdll = CDLL(dll_dir + 'ssc.so')   # instead of relative path, require user to have on LD_LIBRARY_PATH
            else:
                print("Platform not supported ", sys.platform)
        except OSError:
            raise OSError("SAM SSC library was not found on the Python Path or in this folder.")

    @sam_ctypes
    def version(self):
        self.pdll.ssc_version.restype = c_int
        return self.pdll.ssc_version()

    @sam_ctypes
    def data_create(self):
        self.pdll.ssc_data_create.restype = c_void_p
        return self.pdll.ssc_data_create()

    @sam_ctypes
    def data_free(self, p_data):
        self.pdll.ssc_data_free(c_void_p(p_data))

    @sam_ctypes
    def data_clear(self, p_data):
        self.pdll.ssc_data_clear(c_void_p(p_data))

    @sam_ctypes
    def data_unassign(self, p_data, name):
        self.pdll.ssc_data_unassign(c_void_p(p_data), c_char_p(name))

    @sam_ctypes
    def data_query(self, p_data, name):
        self.pdll.ssc_data_query.restype = c_int
        return self.pdll.ssc_data_query(c_void_p(p_data), c_char_p(name))

    @sam_ctypes
    def data_first(self, p_data):
        self.pdll.ssc_data_first.restype = c_char_p
        return self.pdll.ssc_data_first(c_void_p(p_data))

    @sam_ctypes
    def data_next(self, p_data):
        self.pdll.ssc_data_next.restype = c_char_p
        return self.pdll.ssc_data_next(c_void_p(p_data))

    @sam_ctypes
    def data_set_string(self, p_data, name, value):
        self.pdll.ssc_data_set_string(c_void_p(p_data), c_char_p(name), c_char_p(value))

    @sam_ctypes
    def data_set_number(self, p_data, name, value):
        self.pdll.ssc_data_set_number(c_void_p(p_data), c_char_p(name), c_number(value))

    @sam_ctypes
    def data_set_array(self, p_data, name, parr):
        count = len(parr)
        arr = (c_number*count)()
        arr[:] = parr  # set all at once instead of looping
        return self.pdll.ssc_data_set_array(c_void_p(p_data), c_char_p(name), pointer(arr), c_int(count))

    @sam_ctypes
    def data_set_matrix(self, p_data, name, mat):
        nrows = len(mat)
        ncols = len(mat[0])
        size = nrows*ncols
        arr = (c_number*size)()
        idx = 0
        for r in range(nrows):
            for c in range(ncols):
                arr[idx] = c_number(mat[r][c])
                idx += 1
        return self.pdll.ssc_data_set_matrix(c_void_p(p_data), c_char_p(name), pointer(arr), c_int(nrows), c_int(ncols))

    @sam_ctypes
    def data_set_table(self, p_data, name, tab):
        return self.pdll.ssc_data_set_table(c_void_p(p_data), c_char_p(name), c_void_p(tab))

    @sam_ctypes
    def data_get_string(self, p_data, name):
        self.pdll.ssc_data_get_string.restype = c_char_p
        return self.pdll.ssc_data_get_string(c_void_p(p_data), c_char_p(name))

    @sam_ctypes
    def data_get_number(self, p_data, name):
        val = c_number(0)
        self.pdll.ssc_data_get_number(c_void_p(p_data), c_char_p(name), byref(val))
        return val.value

    @sam_ctypes
    def data_get_array(self, p_data, name):
        count = c_int()
        self.pdll.ssc_data_get_array.restype = POINTER(c_number)
        parr = self.pdll.ssc_data_get_array(c_void_p(p_data), c_char_p(name), byref(count))
        arr = parr[0:count.value]  # extract all at once
        return arr

    @sam_ctypes
    def data_get_matrix(self, p_data, name):
        nrows = c_int()
        ncols = c_int()
        self.pdll.ssc_data_get_matrix.restype = POINTER(c_number)
        parr = self.pdll.ssc_data_get_matrix(c_void_p(p_data), c_char_p(name), byref(nrows), byref(ncols))
        idx = 0
        mat = []
        for r in range(nrows.value):
            row = []
            for c in range(ncols.value):
                row.append(float(parr[idx]))
                idx += 1
            mat.append(row)
        return mat
        
    # don't call data_free() on the result, it's an internal
    # pointer inside SSC
    @sam_ctypes
    def data_get_table(self, p_data, name):
        return self.pdll.ssc_data_get_table(c_void_p(p_data), name)

    @sam_ctypes
    def module_entry(self, index):
        self.pdll.ssc_module_entry.restype = c_void_p
        return self.pdll.ssc_module_entry(c_int(index))

    @sam_ctypes
    def entry_name(self, p_entry):
        self.pdll.ssc_entry_name.restype = c_char_p
        return self.pdll.ssc_entry_name(c_void_p(p_entry))

    @sam_ctypes
    def entry_description(self, p_entry):
        self.pdll.ssc_entry_description.restype = c_char_p
        return self.pdll.ssc_entry_description(c_void_p(p_entry))

    @sam_ctypes
    def entry_version(self, p_entry):
        self.pdll.ssc_entry_version.restype = c_int
        return self.pdll.ssc_entry_version(c_void_p(p_entry))

    def get_modules(self):
        modules = dict()
        i = 0
        while self.module_entry(i):
            entry = self.module_entry(i)
            mod_name = self.entry_name(entry)
            mod_desc = self.entry_description(entry)
            mod_ver = self.entry_version(entry)
            modules[mod_name] = {'description': mod_desc, 'version': mod_ver}
            i += 1
        return modules

    @sam_ctypes
    def module_create(self, name):
        self.pdll.ssc_module_create.restype = c_void_p
        return self.pdll.ssc_module_create(c_char_p(name))

    @sam_ctypes
    def module_free(self, p_mod):
        self.pdll.ssc_module_free(c_void_p(p_mod))

    @sam_ctypes
    def module_var_info(self, p_mod, index):
        self.pdll.ssc_module_var_info.restype = c_void_p
        return self.pdll.ssc_module_var_info(c_void_p(p_mod), c_int(index))

    @sam_ctypes
    def info_var_type(self, p_inf):
        return self.pdll.ssc_info_var_type(c_void_p(p_inf))

    @sam_ctypes
    def info_data_type(self, p_inf):
        return self.pdll.ssc_info_data_type(c_void_p(p_inf))

    @sam_ctypes
    def info_name(self, p_inf):
        self.pdll.ssc_info_name.restype = c_char_p
        return self.pdll.ssc_info_name(c_void_p(p_inf))

    @sam_ctypes
    def info_label(self, p_inf):
        self.pdll.ssc_info_label.restype = c_char_p
        return self.pdll.ssc_info_label(c_void_p(p_inf))

    @sam_ctypes
    def info_units(self, p_inf):
        self.pdll.ssc_info_units.restype = c_char_p
        return self.pdll.ssc_info_units(c_void_p(p_inf))

    @sam_ctypes
    def info_meta(self, p_inf):
        self.pdll.ssc_info_meta.restype = c_char_p
        return self.pdll.ssc_info_meta(c_void_p(p_inf))

    @sam_ctypes
    def info_group(self, p_inf):
        self.pdll.ssc_info_group.restype = c_char_p
        return self.pdll.ssc_info_group(c_void_p(p_inf))

    @sam_ctypes
    def info_uihint(self, p_inf):
        self.pdll.ssc_info_uihint.restype = c_char_p
        return self.pdll.ssc_info_uihint(c_void_p(p_inf))

    @sam_ctypes
    def module_exec(self, p_mod, p_data):
        self.pdll.ssc_module_exec.restype = c_int
        return self.pdll.ssc_module_exec(c_void_p(p_mod), c_void_p(p_data))

    @sam_ctypes
    def module_exec_simple_no_thread(self, modname, data):
        self.pdll.ssc_module_exec_simple_nothread.restype = c_char_p
        return self.pdll.ssc_module_exec_simple_nothread(c_char_p(modname), c_void_p(data))

    @sam_ctypes
    def module_log(self, p_mod, index):
        log_type = c_int()
        time = c_float()
        self.pdll.ssc_module_log.restype = c_char_p
        return self.pdll.ssc_module_log(c_void_p(p_mod), c_int(index), byref(log_type), byref(time))

    @sam_ctypes
    def module_exec_set_print(self, prn):
        return self.pdll.ssc_module_exec_set_print(c_int(prn))
