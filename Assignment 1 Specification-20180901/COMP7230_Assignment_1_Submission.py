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
        pressure = record['Central Pressure']
        # If the pressure is already a key in the dictionary then set its value to its current value + 1
        # otherwise set its value to 1.
        print(type(pressure))
        distribution_dictionary[pressure] = distribution_dictionary.get(pressure, 0) + 1
    print(distribution_dictionary)
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

    # TODO: Your code here

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

    array_size = 50  # y, x dimensions of the heat-map
    heat_map_data = np.zeros(shape=(array_size, array_size))
    # TODO: Your code here

    return heat_map_data


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
