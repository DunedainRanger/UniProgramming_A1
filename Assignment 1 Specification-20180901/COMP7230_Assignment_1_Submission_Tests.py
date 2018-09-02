"""
COMP7230 2018 Assignment 1

This file contains the unit tests that you can use to provide some verification
of your answers to questions 1-4 and question 6.

Please note that these tests are there to assist you, and that passing the
tests for a particular question is a good indication you are on the right
track. However it does NOT guarantee that your answer is completely correct.

You do not need to modify the contents of this file.
"""

import unittest
from COMP7230_Assignment_1_Submission import *


class TestSubmission(unittest.TestCase):

    def test_is_valid_record(self):
        """ Basic test that is_valid_record is working correctly. """

        #[Name, ID, datetime, Type, Lat, Long, Central Pressure, Mean radius gf wind, Max wind speed, Comment]
        r1 = ["unnamed","AU190607_01U","1907-01-17 23:00","T","-13","146.5","994","","10.3",
              "Imported from CYCARD; June 2009"]
        r2 = ["unnamed","AU190607_01U","1907-01-17 23:00","T","-13","146.5","","","10.3",
              "Imported from CYCARD; June 2009"]
        r3 = ["unnamed","AU190607_01U","1907-01-17 23:00","T","-13","146.5","994","","",
              "Imported from CYCARD; June 2009"]
        self.assertTrue(is_valid_record(r1), "Everything is present")
        self.assertFalse(is_valid_record(r2), "Missing Central Pressure")
        self.assertFalse(is_valid_record(r3), "Missing Max wind speed")

    def test_parse_record(self):
        """ Basic test that parse_record is working correctly. """

        r1 = ["unnamed", "AU190607_01U", "1907-01-17 23:00", "T", "-13", "146.5", "994", "100", "10.3",
              "Imported from CYCARD; June 2009"]
        r2 = ["unnamed", "AU190607_01U", "1907-01-17 23:00", "T", "-13", "146.5", "994", "", "10.3",
              "Imported from CYCARD; June 2009"]
        a1 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 994.0, "radius": 100.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        a2 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 994.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        self.assertEqual(parse_record(r1), a1)
        self.assertEqual(parse_record(r2), a2)

    def test_convert_lat_long(self):
        """ Basic test that convert_lat_long is working correctly. """

        self.assertEqual(convert_lat_long(MAP_BOTTOM, MAP_LEFT), (0.0, 0.0), "The bottom left should be: 0.0, 0.0")
        self.assertEqual(convert_lat_long(MAP_TOP, MAP_RIGHT), (1.0, 1.0), "The top right should be: 1.0, 1.0")
        x, y = convert_lat_long(-13.0, 146.5)
        self.assertEqual(round(x, 5), 0.58408)
        self.assertEqual(round(y, 5), 0.77792)

    def test_pressure_distribution(self):
        """ Basic test that pressure_distribution is working correctly. """

        r1 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 994.0, "radius": 100.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        r2 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 994.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        r3 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 995.0, "radius": 100.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        r4 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 996.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        a1 = {994.0: 2, 995.0: 1, 996.0: 1}
        self.assertEqual(pressure_distribution([r1, r2, r3, r4]), a1)

    def test_animation_data(self):
        """ Basic test that animation_data is working correctly. """

        r1 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 17, "hour": 23,
              "central pressure": 994.0, "radius": 100.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        r2 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 18, "hour": 0,
              "central pressure": 994.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        r3 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 18, "hour": 1,
              "central pressure": 995.0, "radius": 100.0, "speed": 10.3, "lat": -13.0, "long": 146.5}
        r4 = {"id": "AU190607_01U", "name": "unnamed", "year": 1907, "month": 1, "day": 18, "hour": 2,
              "central pressure": 996.0, "speed": 10.3, "lat": -13.0, "long": 146.5}

        a1 = (1907, 1, 17, 23, -13.0, 146.5, 10.3, "unnamed")
        a2 = (1907, 1, 18, 0, -13.0, 146.5, 10.3, "unnamed")
        a3 = (1907, 1, 18, 1, -13.0, 146.5, 10.3, "unnamed")
        a4 = (1907, 1, 18, 2, -13.0, 146.5, 10.3, "unnamed")

        self.assertEqual(animation_data([r1, r2, r3, r4]), [a1, a2, a3, a4])

if __name__ == '__main__':
    unittest.main()
