"""
COMP7230 - 2018 Assignment 1 code skeleton.

TODO: Replace this with your student id
Student ID: u6811816

In this assignment you will be writing some short pieces of code to process and
display data related to historical tropical cyclones in Australia.

The assignment will be marked out of 20 and is worth 20% of your final grade for COMP7230.

The assignment is structured as follows:

    Part 1 consists of Questions 1, 2 and 3 and deals with basic data cleaning,
    and preparation. It is worth a total of five (5) marks.

    Part 2 consists of Questions 4, 5 and 6 and deals with simple data visualisation
    including a histogram and the cyclone tracking. It is worth a total of seven (7)
    marks.

    Part 3 consists of Question 7 and deals with more complex data visualisation
    where you have to generate a heat-map. It is worth four (4) marks.
    Please be aware that this is a challenging question and make sure you have
    solved parts 1 and 2 before spending too much time on this question.

There will also be four (4) marks allocated to code quality, which includes such
aspects as:

    Appropriate commenting
    Variable naming
    Efficiency of computation
    Code structure and organisation

In addition to this file COMP7230_Assignment_1_Submission.py, we have also provided
a suite of unit tests COMP7230_Assignment_1_Submission_Tests.py which
will help you to test your work. These tests work in an identical fashion to the examples
we use in the Labs, so please familiarise yourself with those if you are not
sure how to make use of them. Please note that these tests are there to assist you,
but passing the tests is NOT a guarantee that your solution is correct.

Once you have completed questions 1-4, you should be able to run this file and
produce a histogram. Question 5 requires you to improve the histogram to make it
clearer and easier to understand.

Once you have completed questions 1, 2, 3 and 6, you should be able to run
COMP7230_Assignment_1_Animation.py and see the cyclone events animating on the map.

Once you have completed questions 1, 2, 3 and 7, you should be able to run
COMP7230_Assignment_1_Heatmap.py and produce the heat-map.

The assignment must be entirely your own work. Copying other students or sharing
solutions is a breach of the ANU Academic Honesty Policy and will be dealt with
accordingly. We reserve the right to ask any student to explain their code, and further
action may be taken if they are unable to do so.

The Assignment is due at 4pm, 7 September 2018. We will mark whatever is
uploaded into Wattle at that point, and late submissions will not be marked.

Once marks are released, you will have two weeks in which to question your mark.
After this period has elapsed, your mark will be considered final and no further
changes will be made.

If you ask for a re-mark, your assignment will be re-marked entirely, and your mark
may go UP or DOWN as a result.

The original data set was obtained from: http://www.bom.gov.au/cyclone/history/
The map was obtained from: https://www.google.com.au/maps
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import math
# Some constants you can make use of.

# The latitude and longitude extent of the provided map.
MAP_TOP = -6.2
MAP_BOTTOM = -36.82
MAP_LEFT = 106.8
MAP_RIGHT = 174.77

# Constant for Part 3.
EARTH_RADIUS = 6371  # Mean radius of the earth in kilometers.


########################################################################################################################
#                                   Part 1 - Data preparation and cleaning
#                                   Questions 1 - 3.        5 Marks total.
########################################################################################################################

#                                   Question 1.             1 Mark.
def is_valid_record(record):
    """
    This function tests whether a record has all the data that is required. Specifically, whether
    there is a non-empty value for central pressure and wind speed.
    :param record: A list containing a row of data in the file.
    format = [Name, ID, datetime, Type, Lat, Long, Central Pressure, Mean radius gf wind, Max wind speed, Comment]
    Each element in the list is a string.
    :return True if central pressure and wind speed have non-empty values, False otherwise.
    """

    if len(record[6]) > 0 and len(record[8]) > 0:
        return True
    else:
        return False


#                                   Question 2.             2 Marks.
def parse_record(record):
    """
    This function converts a record in the data into a dictionary of key value pairs for each attribute/attribute value.
    :param record: A list containing a row of data in the file.
    format = [Name, ID, datetime, Type, Lat, Long, Central Pressure, Mean radius gf wind, Max wind speed, Comment]
    :return: A dictionary containing key value pairs for each attribute and value. It should contain the following
    attributes (of the corresponding types).
    "id" (string), "name" (string), "year" (int), "month" (int), "day" (int), "hour" (int), "central pressure" (float),
    "radius" (float), "speed" (float), "lat" (float), "long" (float)
    where "radius" is the Mean radius of gf wind, and "speed" is the Max wind speed.
    If a value is blank in the data, it should be left out of the dictionary.
    """
    # Creating a list of keys so that we can zip these with the values and then create a dict
    # Doing this instead of adding each key individually will make it easier to make changes should the keys change
    # and reduce the amount of code.
    record_dictionary = {}
    # Let's remove the values in record that wont go into our dictionary
    record.pop(3)
    record.pop()
    # By parsing the datetime into a Datetime.datetime object we can easily access the year,month,day and hour without
    # resorting to regex.
    record_datetime = dt.datetime.strptime(record.pop(2), '%Y-%m-%d %H:%M')
    # Now we add the values we want from the datetime to record to set up the next part.
    record.extend([record_datetime.year, record_datetime.month, record_datetime.day, record_datetime.hour])
    # Here we zip the value, key and the type we want the value to be in together. This logically groups them together
    # and results in neater code then enumerating the values and using the index to access the appropriate key and type
    # from the keys and types lists respectively.
    keys = ['name', 'id', 'lat', 'long', 'central pressure', 'radius', 'speed', 'year', 'month', 'day', 'hour']
    types = [str, str, float, float, float, float, float, int, int, int, int]
    values_keys_types = zip(record,keys,types)
    # Here we add our values to the dictionary. We add the _ to the variable name type_ to avoid clashing with the
    # key word type whilst maintaining the obvious/descriptive name for the variable.
    for value, key, type_ in values_keys_types:
        if str(value):
            record_dictionary[key] = type_(value)
    return record_dictionary


#                                   Question 3.             2 Marks.
def convert_lat_long(lat, long):
    """
    This function converts latitude and longitude values into map coordinates.
    :param lat: a latitude value (float)
    :param long: a longitude value (float)
    :return: a tuple of x, y coordinates (x, y), where (0.0, 0.0) is the bottom left corner of the map
    and (1.0, 1.0) is the top right corner.
    You should make use of the constants described in the heading.
    """
    # First we get the x and y position relative to MAP_BOTTOM and MAP_TOP
    relative_y = lat - MAP_BOTTOM
    relative_x = long - MAP_LEFT

    # Now we normalise our relative x and y to be between 0 and 1
    y = relative_y / (MAP_TOP - MAP_BOTTOM)
    x = relative_x / (MAP_RIGHT - MAP_LEFT)

    return x, y


########################################################################################################################
#                                   Part 2 - Basic Data Visualisation
#                                   Questions 4 - 6.        7 Marks total.
########################################################################################################################

#                                   Question 4.             2 Marks
def pressure_distribution(records):
    """
    For this question you need to aggregate the data we will use to build the histogram of central pressure.
    :param records: A list of dictionaries, each element of the list is a dictionary containing the data for a single
    record, as produced by Question 2.
    :return: A dictionary, of {central pressure measurement : frequency count} pairs.
    """

    distribution_dictionary = dict()

    for record in records:
        # Save pressure to variable for readability
        pressure = record['central pressure']
        # If the pressure is already a key in the dictionary then set its value to its current value + 1
        # otherwise set its value to 1.
        distribution_dictionary[pressure] = distribution_dictionary.get(pressure, 0) + 1
    return distribution_dictionary


#                                   Question 5.             3 Marks
def pressure_histogram(distribution_dictionary):
    """
    Once you have completed Questions 1, 2 and 4, this function will create a histogram of the
    central pressure measurements.
    However, the histogram is not a particularly good one:
        It is hard to interpret.
        It is very cluttered.
        It is missing some important features - axis labels, a title, etc.
    Your task is to improve the histogram in whatever way you see fit.

    Marks will be awarded based on how well your new histogram conveys information,
    how easy it is to interpret, and whether it is formatted appropriately.

    You are free to modify the code below, or even delete it and replace it with your own if you wish.
    Please make sure you explain what you are doing (and why) in the comments.

    If you make use of external resources, please don't forget to reference them in the comments.

    :param distribution_dictionary: The dictionary of {central pressure : frequency count} key, value pairs, as
    produced by Question 4.
    :return: None
    """

    # Here to ensure there isn't an error if Q4 is not completed.
    if not distribution_dictionary:
        return None

    # Order the data based on the central pressure value.
    frequency_data = sorted(distribution_dictionary.items())

    # Generate the lists of x values and y values.
    x_list = [frequency_data[i][0] for i in range(len(frequency_data))]
    y_list = [frequency_data[i][1] for i in range(len(frequency_data))]

    # Display the histogram
    plt.bar(x_list, y_list, width=1)
    plt.title("Histogram to show frequency of central pressure values")
    plt.xlabel("Central Pressure")
    plt.ylabel("Frequency")
    plt.show()

    return None


#                                   Question 6.             2 Marks
def animation_data(cyclone_records):
    """
    You need to prepare the track data for each cyclone, so they can be animated on the map.
    :param cyclone_records: A list of dictionaries, each element of the list is a dictionary containing the data
    for a single record, as produced by Question 2.
    :return: A list of (year, month, day, hour, latitude, longitude, wind_speed, name) tuples, in CHRONOLOGICAL order.
    The first four elements in each tuple should be integers, the next 3 should be floats, name should be a string.
    """
    cyclone_track = list()

    # First convert the dictionaries into tuples of the correct format and add to cyclone_track
    for cyclone_record in cyclone_records:
        record_tuple = (cyclone_record['year'], cyclone_record['month'], cyclone_record['day'], cyclone_record['hour'],
                        cyclone_record['lat'], cyclone_record['long'], cyclone_record['speed'], cyclone_record['name'])
        cyclone_track.append(record_tuple)

    # Now we order them chronologically, we can do this in line line by making use of list.sort's key parameter
    # This allows us to specify a key to use for sorting. In this case we will convert our year,month,day,hour values
    # to a datetime and then compare these.
    cyclone_track.sort(key=lambda x: dt.datetime(x[0], x[1], x[2], x[3]))
    return cyclone_track


########################################################################################################################
#                                   Part 3 - Advanced Data Visualisation
#                                   Question 7.             4 Marks total.
########################################################################################################################


#                                   Question 7.             4 Marks
def generate_heat_map(records):
    """
    Please be aware that this is a challenging question and it may take considerable
    effort to solve.
    Make sure you have completed the rest of the assignment to a high standard before
    spending a lot of time on this question.

    This question requires you to generate a heat-map of the data.

    A heat-map is essentially a two dimensional histogram of the data, where high frequencies are represented by
    bright colours (red, orange, etc), and low frequencies are represented by dark colours (green, blue, etc.)
    The data is stored as a two dimensional array of integers, where the integers represent the frequency counts
    for that part of the map. For example:

    [[10, 5],
    [[0, 12]]

    means that 10 cyclones were recorded in the top left quarter of the map, 5 in the top right quarter, etc.

    The default array size is 50 by 50, but you can increase this if you wish.

    For records that do not have a mean gf (gale-force) wind radius measurement, you should just include the grid cell
    that the eye is located in (as given by the latitude and longitude values).

    For records with a mean gf (gale-force) wind radius measurement, you should include any cell that is within
    the radius of the gale force winds (even if only part of the cell is inside the radius).
    The units for the mean gf wind radius attribute are kilometers.

    You should make use of the constants in the heading, as well as any functions you have previously written
    that are relevant.

    Once you have completed the code, you should also write a short comment (~200 words) that describes the
    heat-map, along with any reasons why the heat-map produced might not reflect actual cyclone activity.

    You will be marked on the correctness of your heat-map, as well as the efficiency of the code
    you use to generate the data. One (1) mark will also be allocated to your explanation. Please note that
    you must get the heat-map largely correct in order to receive the mark for the explanation.
    Partial marks may be awarded for partial solutions, as long as the code makes progress towards a
    full solution to the problem.

    :param records: A list of dictionaries, each element of the list is a dictionary containing the data for a single
    record, as produced by Question 2.
    :return: a 2d numpy array of integers.
    """
    array_size = 50
    heat_map_data = np.zeros(shape=(array_size, array_size))
    height_of_box_in_lat = (MAP_TOP - MAP_BOTTOM)/array_size
    width_of_box_in_lon = (MAP_RIGHT - MAP_LEFT)/array_size
    for cyclone in records:
        cyclone_map_data = np.zeros(shape=(array_size, array_size))
        centre_x, centre_y = convert_lat_long(cyclone['lat'], cyclone['long'])
        centre_column, centre_row = int(centre_x * array_size), -int(centre_y * array_size)
        if 'radius' in cyclone:
            # Calculate the length in KM of one degree longitude at the eyes latitude
            # To do this we first calculate the radius of the earth at this degree latitude, we do this by using
            # trigonometry and assuming the earth is a perfect sphere. Then we divide the radius by 360 to get
            # the length in KMs of a single degree longitude at this latitude.
            # Cosine(latitude angle) * Earths Radius (hypotenuse) = Radius at this degree latitude (adjacent)
            radius_at_lat = math.cos(math.radians(cyclone['lat'])) * EARTH_RADIUS
            degree_lon_in_km = radius_at_lat / 360
            for row in range(array_size):
                # Get the latitudinal position of the side of the row (top or bottom of row) closest to the eye.
                # If eye is in row then lat position closest to eye is eyes latitude
                box_top_lat = MAP_TOP - row * height_of_box_in_lat
                box_bottom_lat = MAP_TOP - (row + 1) * height_of_box_in_lat
                closest_latitudes = [cyclone['lat'], box_bottom_lat, box_top_lat]
                row_position = np.sign(centre_row - row)  # Box is above if +ve, inline if 0, below if -ve
                y_distance = 110 * (closest_latitudes[row_position] - cyclone['lat'])  # 1 lat = approx 110KM
                for column in range(array_size):
                    # Get the longitudinal position of the side of the column (left or right side of column) that is
                    # closest to the eye.
                    # If eye is in column then long position closest to eye is eyes longitude.
                    box_left_lon = MAP_LEFT + column*width_of_box_in_lon
                    box_right_lon = MAP_LEFT + (column+1)*width_of_box_in_lon
                    closest_longitudes = [cyclone['long'], box_left_lon, box_right_lon]
                    column_position = np.sign(column - centre_column)
                    x_distance = degree_lon_in_km*(closest_longitudes[column_position] - cyclone['long'])
                    # Now to get the actual distance we take sqrt(x**2 + y**2)
                    distance_from_eye = math.sqrt(x_distance**2 + y_distance**2)
                    if distance_from_eye < cyclone['radius']:  # Aka if part of cyclone in box
                        cyclone_map_data[row][column] = 1
        elif 'radius' not in cyclone and (0 < centre_y < 1 and 0 < centre_x < 1):
            # If cyclone has no radius and eye is on map then record this.
            cyclone_map_data[centre_row, centre_column] = 1
        # At this point cyclone_map_data has a value of 1 for each box the cyclone is in and 0 for boxes it is not in.
        # By taking the sum of these for every cyclone we will get out hea_map_data.
        heat_map_data += cyclone_map_data
    return heat_map_data
    """
    The heat map produced by the code above is a rough approximation of the example heat map, however it over-estimates 
    how wide cyclones are. You can see this because the two main patched of activity seems stretched out, covering the
    top of australia and some of the pacific countries unlike in the example. This is because the method above uses a 
    heuristic method to convert the lat and long into distance. It assumes 1 lat is precisely 110KM and uses an 
    approximate conversion from longitude to KM based on the latitude of the eye of the storm.
    To make this more accurate I would download the GEOPY package and use its geopy.distance.distance method which uses
    the geodesic method to calculate distance. For details on my heuristic method please see the source code above.
    """

########################################################################################################################
#                                   Do not modify the code below this point.
########################################################################################################################

def read_data_set(file_name):
    """
    Reads in and processes a csv file of the given name.
    :param file_name: The name of the file (string) to process.
    :return: A list of records.
    """

    # Read in the data set
    input_data = open(file_name, mode="r")
    input_reader = csv.reader(input_data)
    next(input_reader)  # Remove the header

    data_set = []

    for record in input_reader:
        if record[1] and record[2] and record[4] and record[5] and is_valid_record(record):
            data_set.append(record)

    input_data.close()

    return data_set


# Once you have finished questions 1, 2 and 4, running this file should produce a histogram.
# Your task for question 5 is to improve the quality and understandability of the histogram.
if __name__ == "__main__":

    data_set = read_data_set("Cyclones.csv")

    parsed_data = []

    for record in data_set:
        parsed_record = parse_record(record)
        if parsed_record:
            parsed_data.append(parsed_record)

    if parsed_data:
        histogram_data = pressure_distribution(parsed_data)
        pressure_histogram(histogram_data)
    else:
        print("You need to complete questions 1, 2 and 4 in order to produce the histogram")
