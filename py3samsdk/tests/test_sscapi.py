import unittest
import numpy as np
import numpy.testing as npt
from py3samsdk import PySSC


dll_path = "../../"


class TestSSCAPI(unittest.TestCase):
    # test to list all ssc version and build information
    def test_version(self):
        ssc = PySSC(dll_path)
        print('ssc version = ', ssc.version())
        npt.assert_(ssc.version() >= 159)

    # test to list all modules available in ssc
    def test_module_list(self):
        ssc = PySSC(dll_path)
        modules = ssc.get_modules()
        npt.assert_('cashloan' in modules.keys())
        npt.assert_('pvwattsv5' in modules.keys())

    def test_array_set_get(self):
        ssc = PySSC(dll_path)
        dat = ssc.data_create()
        arr = np.arange(0, 50)
        ssc.data_set_array(dat, "TestArray", arr)  # set
        ret_array = ssc.data_get_array(dat, "TestArray")  # get
        npt.assert_array_almost_equal(arr, ret_array)

    def test_matrix(self):
        ssc = PySSC(dll_path)
        dat = ssc.data_create()
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        ssc.data_set_matrix(dat, "TestMatrix", matrix)  # set
        ret_matrix = ssc.data_get_matrix(dat, "TestMatrix")  # get
        
        npt.assert_array_almost_equal(ret_matrix, matrix)

#
# def module_and_variables_test():
#          ssc_entry = ssc.Entry()
#          module_index = 0
#          while (ssc_entry.get()):
#               module_name = ssc_entry.name()
#               description = ssc_entry.description()
#               version = ssc_entry.version()
#               print("\nModule: " , module_name , ", version: " , version)
#               print(" " + description)
#               module_index += 1
#
#               ssc_module = ssc.Module(module_name)
#               ssc_info = ssc.Info(ssc_module)
#
#               while (ssc_info.get()):
#                        print("\t" , ssc_info.var_type() , ": \"" , ssc_info.name() , "\" " , " [" , ssc_info.data_type() , "] " + ssc_info.label() , " (" , ssc_info.units() , ")")
#
# def variables_list(module):
#          ssc_module = ssc.Module(module)
#          ssc_info = ssc.Info(ssc_module)
#
#          print("Variables for " , module)
#          while (ssc_info.get()):
#               print("\t" , ssc_info.var_type() , ": \"" , ssc_info.name() , "\" " , " [" , ssc_info.data_type() , "] " + ssc_info.label() , " (" , ssc_info.units() , ")")
#
#
#
