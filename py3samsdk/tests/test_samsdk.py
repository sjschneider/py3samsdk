import unittest
import numpy as np
import numpy.testing as npt
from py3samsdk import PySSC
from py3samsdk import sam


dll_path = "../../"


class SmokeTests(unittest.TestCase):
    def test_read_weather_file(self):
        ssc = PySSC(dll_path)
        dat = ssc.data_create()

        wf = './test_files/785140TYA.CSV'
        ssc.data_set_string(dat, 'file_name', wf)
        ssc.module_exec_simple_no_thread('wfreader', dat)

        lat = ssc.data_get_number(dat, 'lat')
        lon = ssc.data_get_number(dat, 'lon')
        lat_lon = np.array([lat, lon])
        npt.assert_array_almost_equal(lat_lon, np.array([18.5, -67.1]), 1)

    def test_SAM_PVWatts_run1(self):
        ssc = PySSC(dll_path)
        dat = ssc.data_create()
        wf = './test_files/785140TYA.CSV'
        ssc.data_set_string(dat, 'solar_resource_file', wf)

        ssc.data_set_number(dat, 'system_size', 4)
        ssc.data_set_number(dat, 'derate', 0.77)
        ssc.data_set_number(dat, 'track_mode', 0)
        ssc.data_set_number(dat, 'azimuth', 180)
        ssc.data_set_number(dat, 'tilt_eq_lat', 1)
        ssc.data_set_number(dat, 'tilt_eq_lat', 1)
        ssc.data_set_number(dat, 'adjust:constant', 0)
        ssc.data_set_number(dat, 'adjust:factor', 1)
        ssc.data_set_number(dat, "system_capacity", 1.0)
        ssc.data_set_number(dat, "dc_ac_ratio", 1)
        ssc.data_set_number(dat, "losses", 0)
        ssc.data_set_number(dat, "array_type", 2)
        ssc.data_set_number(dat, "tilt", 15)

        ac, dc = sam.run_pvwattsv5(ssc, dat)
        npt.assert_almost_equal(np.sum(ac), 2272, 0)
        ssc.data_free(dat)

    def test_SAM_PVWatts_run2(self):
        ssc = PySSC()
        dat = ssc.data_create()
        wf = './test_files/abilene.tm2'
        ssc.data_set_string(dat, "solar_resource_file", wf)
        ssc.data_set_number(dat, "system_capacity", 4.0)
        ssc.data_set_number(dat, "dc_ac_ratio", 1.1)
        ssc.data_set_number(dat, "tilt", 20)
        ssc.data_set_number(dat, "azimuth", 180)
        ssc.data_set_number(dat, 'inv_eff', 96)
        ssc.data_set_number(dat, 'losses', 14.0757)
        ssc.data_set_number(dat, 'array_type', 0)
        ssc.data_set_number(dat, 'tilt', 20)
        ssc.data_set_number(dat, 'azimuth', 180)
        ssc.data_set_number(dat, 'gcr', 0.4)
        ssc.data_set_number(dat, 'adjust:factor', 1)
        ssc.data_set_number(dat, 'adjust:constant', 0)

        ac, dc = sam.run_pvwattsv5(ssc, dat)
        npt.assert_almost_equal(np.sum(ac), 6391, 0)
        npt.assert_almost_equal(np.sum(dc), 6676.78, 0)
        ssc.data_free(dat)


# class TestWindModel(unittest.TestCase):
#     @staticmethod
#     def setup_wind(ssc, data):
#         ssc.data_set_number(data, 'wind_resource_shear', 0.14)
#         ssc.data_set_number(data, 'wind_resource_turbulence_coeff', 0.1)
#         ssc.data_set_number(data, 'system_capacity', 2.4)
#         ssc.data_set_number(data, 'wind_resource_model_choice', 0)
#         ssc.data_set_number(data, 'wind_characteristics_weibullK', 2.1)
#         ssc.data_set_number(data, 'wind_characteristics_class', 7.6)
#         ssc.data_set_number(data, 'wind_turbine_rotor_diameter', 3.7)
#         ssc.data_set_array(data, 'wind_turbine_powercurve_windspeeds',
#                            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
#                             21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40])
#         ssc.data_set_array(data, 'wind_turbine_powercurve_powerout',
#                            [0, 0, 0, 0, 0.08, 0.2, 0.35, 0.6, 1, 1.6, 2, 2.25, 2.35, 2.4, 2.4, 2.37, 2.3, 2.09, 2, 2,
#                             2, 2, 2, 1.98, 1.95, 1.8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#         ssc.data_set_number(data, 'wind_turbine_cutin', 4)
#         ssc.data_set_number(data, 'wind_turbine_hub_ht', 15)
#         ssc.data_set_number(data, 'wind_turbine_max_cp', 0.42)
#         ssc.data_set_array(data, 'wind_farm_xCoordinates', [0])
#         ssc.data_set_array(data, 'wind_farm_yCoordinates', [0])
#         ssc.data_set_number(data, 'wind_farm_losses_percent', 0)
#         ssc.data_set_number(data, 'wind_farm_wake_model', 0)
#         ssc.data_set_number(data, 'adjust:constant', 0)
#
#     def test_wind_model(self):
#         #wf = 'C:/Users/adobos/Projects/SAMnt/deploy/wind_resource/WY Southern-Flat Lands.srw';
#         wf = './test_files/WY Southern-Flat Lands.srw'
#
#         ssc = PySSC(dll_path)
#         dat = ssc.data_create()
#         self.setup_wind(ssc, dat)
#         ssc.data_set_string(dat, 'wind_resource_filename', wf)
#         sam.run_windmodel(ssc, dat)
#
#         ssc.data_clear(dat)
#
#         # read a weather file for this example program
#         # and extract the data from it into a bunch of Python variables
#         # note: this weather data could come from any source
#
#         # create an SSC data with a bunch of fields
#         wfd = ssc.data_create()
#         ssc.data_set_number(wfd, 'lat', 0)
#         ssc.data_set_number(wfd, 'lon', 0)
#         ssc.data_set_number(wfd, 'elev',  2088)
#
#         # setup column data types: temp=1,pres=2,3=3,dir=4
#         ssc.data_set_array( wfd, 'fields', [1, 2, 4, 3, 1, 2, 4, 3, 1, 2, 4, 3, 1, 2, 4, 3])
#
#         # setup column measurement heights (meters)
#         ssc.data_set_array( wfd, 'heights', [50, 50, 50, 50, 80, 80, 80, 80, 110, 110, 110, 110, 140, 140, 140, 140])
#
#         # read in the matrix of data corresponding to fields and heights above (should have 8760 rows)
#         data = np.loadtxt(open(wf, "rb"), delimiter=",", skiprows=5)
#         ssc.data_set_matrix(wfd, 'data', data)
#
#         # instead of setting a string weather file, simply
#         # set the table variable that contains the various fields
#         # with solar resource data
#         ssc.data_set_table(dat, 'wind_resource_data', wfd)
#
#         # we can free the resource data table now, since
#         # the previous line copies it all into SSC
#         ssc.data_free(wfd)
#
#         # set up other PV parameters and run
#         self.setup_wind(ssc, dat)
#         sam.run_windmodel(ssc, dat)
#
#         ssc.data_free(dat)
#
#
# class TestSolarModel(unittest.TestCase):
#     @staticmethod
#     def setup_pv(self, ssc, data):
#         ssc.data_set_number(data, 'system_capacity', 4)
#         ssc.data_set_number(data, 'module_type', 0)
#         ssc.data_set_number(data, 'array_type', 0)
#         ssc.data_set_number(data, 'losses', 14)
#         ssc.data_set_number(data, 'tilt', 15)
#         ssc.data_set_number(data, 'azimuth', 180)
#         ssc.data_set_number(data, 'adjust:constant', 0)
#
#     def test_solar_model(self):
#         #wf = 'c:/Users/adobos/Projects/SAMnt/tests/Weather Files/user-germany-potsdam-2011-1-min-samcsv.csv' ;
#         #wf = 'C:/Users/adobos/Projects/SAMnt/deploy/solar_resource/USA NC Greensboro (TMY2).csv';
#         wf = './test_files/USA NC Greensboro (TMY2).csv'
#
#         ssc = PySSC(dll_path)
#         dat = ssc.data_create()
#         self.setup_pv(ssc, dat)
#         ssc.data_set_string(dat, 'solar_resource_file', wf)
#         sam.run_pvwattsv5(ssc, dat)
#
#         ssc.data_clear(dat)
#
#         # read a weather file for this example program
#         # and extract the data from it into a bunch of Python variables
#         # note: this weather data could come from any source
#         ssc.data_set_string( dat, 'file_name', wf)
#         ssc.module_exec_simple_no_thread('wfreader', dat)
#         lat = ssc.data_get_number(dat, 'lat')
#         lon = ssc.data_get_number(dat, 'lon')
#         tz = ssc.data_get_number(dat, 'tz')
#         elev = ssc.data_get_number(dat, 'elev')
#         year = ssc.data_get_array(dat, 'year')
#         month = ssc.data_get_array(dat, 'month')
#         day = ssc.data_get_array(dat, 'day')
#         hour = ssc.data_get_array(dat, 'hour')
#         minute = ssc.data_get_array(dat, 'minute')
#         beam = ssc.data_get_array(dat, 'beam')
#         diffuse = ssc.data_get_array(dat, 'diffuse')
#         wspd = ssc.data_get_array(dat, 'wspd')
#         tdry = ssc.data_get_array(dat, 'tdry')
#         albedo = ssc.data_get_array(dat, 'albedo')
#         ssc.data_clear(dat)
#
#         # create an SSC data with a bunch of fields
#         wfd = ssc.data_create();
#         ssc.data_set_number(wfd, 'lat', lat)
#         ssc.data_set_number(wfd, 'lon', lon)
#         ssc.data_set_number(wfd, 'tz',  tz)
#         ssc.data_set_number(wfd, 'elev',  elev)
#
#         ssc.data_set_array(wfd, 'year',  year)
#         ssc.data_set_array(wfd, 'month',  month)
#         ssc.data_set_array(wfd, 'day',  day)
#         ssc.data_set_array(wfd, 'hour', hour)
#
#         # note: if using an hourly TMY file with integrated/averaged
#         # values, do not set the minute column here. otherwise
#         # SSC will assume it is instantaneous data and will not adjust
#         # the sun position in sunrise and sunset hours appropriately
#         # however, if using subhourly data or instantaneous NSRDB data
#         # do explicitly provide the minute data column for sunpos calcs
#
#         # ssc.data_set_array( wfd, 'minute', minute);
#
#         ssc.data_set_array(wfd, 'dn', beam)
#         ssc.data_set_array(wfd, 'df', diffuse)
#         ssc.data_set_array(wfd, 'wspd', wspd)
#         ssc.data_set_array(wfd, 'tdry', tdry)
#         ssc.data_set_array(wfd, 'albedo', albedo)
#
#         # instead of setting a string weather file, simply
#         # set the table variable that contains the various fields
#         # with solar resource data
#         ssc.data_set_table(dat, 'solar_resource_data', wfd)
#
#         # we can free the resource data table now, since
#         # the previous line copies it all into SSC
#         ssc.data_free(wfd)
#
#         # set up other PV parameters and run
#         self.setup_pv(ssc, dat)
#         sam.run_pvwattsv5(ssc, dat)
#
#         ssc.data_free(dat)
