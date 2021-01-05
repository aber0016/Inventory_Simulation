'''
FIT9136 assignment 1 - TASK 1 - Armin Herman Dieter Berger - aber0016
This program is an inventory management system for a company selling cantilever umbrellas.
It will provide the user with the stock count and revenue at the end of a single year cycle of any given year.

Some of the features of this program for task 1 are not required to be included, however since the code was writen
in a way that it would be easier to accommodate the needs of task 2, they were still included. An example of that can 
be seen in the functions simulate_rrp_from_default_start_year_till_end_year() and 
simulate_distributed_items_from_default_start_year_till_end_year() where temporary adjustments are made to rrp and 
distributed quantity in accordance with whether it is peak season or not. This would have not be necessary to do for
task 1 since the these changes are temporary and have no long run effect on the distributed quantity and rrp over the
years. Directly including this feature when writing task one, however, makes the code easily transferable to task 2
without major adjustments.

This program uses Boolean variables in combination with loops to check for the occurrence of certain conditions and
adjust variables over time.

The program overall has x functions of which each is annotate in accordance to their purpose and function.

The following set of additional assumptions were made in accordance with the feedback of diffrnet tutors and were
required to guide the development of this program.
1.
2.

When defectives are sold at the start of each month they are deducted from inventory like any other normal sales
....

'''''

# This is a collection of global variables that are used throughout the entire program in different functions
# In case the user wants to change any of these variables, this can be conveniently done here and no further adjustments
# to the code need to be made
NO_YEAR_SIM = 1     # number of years of the simulation, since task 1 is only looking at a single year cycle this
                    # variable is set to 1 by default
PER_DEF = 5     # percentage of defective items that get returned to the company every month
CRIS_RECUR_FREQ = 9 # frequency of financial crisis

default_start_year = 2000   # the year the company was found and based upon which all starting variables are based on
default_start_month = 1     # the month the company was found
default_start_day = 1       # the day the company was found

default_start_stock_value = 1000    # the starting inventory of the morning of 01/01/2000
default_start_revenue = 0.00        # the starting revenue of the morning of 01/01/2000

default_start_rrp = 587.50                  # the starting rrp of the non-peak season 2000
peak_season_rrp_increment_factor = 1.20     # factor by which rrp increases during each peak season from Nov - Feb
financial_year_rrp_increment_factor = 1.05  # factor by which rrp increases from financial year to financial year
global_financial_crisis_year_one_rrp_increment_factor = 1.10  # factor by which rrp increases in the 1. fin crisis year
global_financial_crisis_year_two_rrp_increment_factor = 1.05  # factor by which rrp increases in the 2. fin crisis year
global_financial_crisis_year_three_rrp_increment_factor = 1.03 # factor by which rrp increases in the 3. fin crisis year

default_start_distributed_quantity = 27             # the starting distributed_quantity of the non-peak season 2000
peak_season_distributed_quantity_increment_factor = 1.35    # factor by which the distributed_quantity increases during
                                                            # each peak season from Nov - Feb
financial_year_distributed_quantity_increment_factor = 1.10 # factor by which the distributed_quantity increases from
                                                            # financial year to financial year
# factors by which the distributed_quantity decreases in fin crisis year 1 to 3
global_financial_crisis_year_one_distributed_quantity_decrement_factor = 0.80
global_financial_crisis_year_two_distributed_quantity_decrement_factor = 0.90
global_financial_crisis_year_three_distributed_quantity_decrement_factor = 0.95

defective_items_rrp_percentage = 0.80   # percentage of rrp at which defective items are resold every next month

leap_year_days_in_month_dict = {1: 31,  # dictionary that has each month of a leap year as a key (int value)
                                2: 29,  # and has the days of a month as a value (int value)
                                3: 31,
                                4: 30,
                                5: 31,
                                6: 30,
                                7: 31,
                                8: 31,
                                9: 30,
                                10: 31,
                                11: 30,
                                12: 31}

non_leap_year_days_in_month_dict = {1: 31,  # dictionary that has each month of a regular year as a key (int value)
                                    2: 28,  # and has the days of a month as a value (int value)
                                    3: 31,
                                    4: 30,
                                    5: 31,
                                    6: 30,
                                    7: 31,
                                    8: 31,
                                    9: 30,
                                    10: 31,
                                    11: 30,
                                    12: 31}

''''
The program has three functions get_year() get_stock_value() and get_revenue_value() which all check whether the input 
they receive follows the required format and is thus 'valid'. If the input variable is in an invalid format, it throws
an error message. To achieve this we use a try and except statement in combination with the built in exception class
ValueError
'''''
# catch faulty year inputs that don't meet the date format using try and except block
def get_year(date_string):
    try:
        year = int(date_string)
        if year < 2000 and year < 20000:
            raise ValueError
        else:
            return year
    except ValueError:
        print("Incorrect Date Format. "
              "Date Format must be YYYY and YYYY should be >= 2000 . "
              "Default Start Year of 2000 will be used.")
        return default_start_year

# catch faulty stock inputs that don't meet the stock format (negative stock levels) using try and except block
def get_stock_value(stock_string):
    try:
        stock_value = int(stock_string)
        if stock_value < 0:
            raise ValueError
        return stock_value
    except ValueError:
        print("Incorrect Stock Value. "
              "Stock Value should be an Integer >= 0 . "
              "Default Start Stock value of 1000 will be used.")
        return default_start_stock_value

# catch faulty revenue inputs that don't meet the format for revenue (negative starting revenue levels)
def get_revenue_value(revenue_string):
    try:
        revenue_value = float(revenue_string)
        if revenue_value < 0.0:
            raise ValueError
        return revenue_value
    except ValueError:
        print("Incorrect Revenue Value. "
              "Revenue Value should be an Integer/Float >= 0.0 ."
              "Default Start Revenue value of 0.00 will be used.")
        return default_start_revenue

'''''
This function reads in data form a txt file called “AU_INV_START.txt”. The data contains 1. Starting year,
2. Total stock available, and 3. Starting revenue for the year which the simulation will be done for. 
The data which is being read in is stored as int values in a dictionary. The key names for these three values
are "start_year": XXX, "start_stock": XXX, "start_revenue": XXX .
'''''
def read_data():
    data = dict() # dictionary that stores the read in file date

    # use of try and except block to catch faulty data input
    try:
        f = open('AU_INV_START_TASK_1.txt')        # create file handle that reads in file date
        file_lines = f.readlines()                 # read line by line of file handel f using readlines() function
    except FileNotFoundError:                      # throw error in case file is not found and no data could be read in
        print('Input File not Found. Exiting ...')
        exit(0)                                    # exit program, user should check whether “AU_INV_START.txt” exists
                                                   # or is saved in the right folder
    for i in range(0, len(file_lines)):     # iterate through each line in the file using a for loop
        file_lines[i] = ''.join(file_lines[i].split())
        file_lines[i] = file_lines[i].strip()       # strip line of whitespace
        if not file_lines[i] in ['\n', '\r\n', '']: # ?
            if i == 0:                          # if line equals to first line of the file
                data['start_year'] = get_year(file_lines[i])   # save input as value for key 'start_year' in dict data
            elif i == 1:                        # if line equals to second line of the file
                data['start_stock'] = get_stock_value(file_lines[i]) # save input as value for key 'start_stock'
            elif i == 2:                         # if line equals to third line of the file
                data['start_revenue'] = get_revenue_value(file_lines[i]) # save input as value for key 'start_revenue'
            # if condition not met print error 'incorrect data' and exit program
            else:
                print('Incorrect Data Format for File. Exiting ...')
                exit(0)
        else:
            print('Incorrect Data Format for File. Exiting ...')
            exit(0)

    return data     # returns a dict called data which is filled with the information of “AU_INV_START.txt”

'''''
This function checks whether a year is a leap year or not. A leap year usually every 4 years. Every 100 year a leap year
is skipped unless the year is divisible by 400. The alogrithm performed for these calculations adapts the structure taken
from https://www.programiz.com/python-programming/examples/leap-year . If a year turns out to be a leap year a Boolaen
variable = True is returned 
'''''
def is_leap_year(year):
    if (year % 4) == 0:     # use remainder operate to check whether year is evenly dividable by 4 and is thus
                            # a potential leap year
        if (year % 100) == 0:  # use remainder operate to check whether year is evenly dividable by 100, if yes then
            if (year % 400) == 0:   # use the remainder operate to check whether year is evenly dividable by 400,
                                    # if so year is a leap year
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# This function rounds the distributed quantity from a float mathematically correct to an int, without having
# to use the math.ceiling() library. Logic for this algorithm imitates the logic from user Rory Daulton on:
# https://stackoverflow.com/questions/57115951/rounding-a-math-calculation-up-without-math-ceil
def get_rounded_distributed_quantity(current_distributed_quantity):
    if (float(current_distributed_quantity) % 1) >= 0.5:
        current_distributed_quantity = int(-(-current_distributed_quantity // 1))
    else:
        current_distributed_quantity = int(round(current_distributed_quantity))

    return current_distributed_quantity

'''''
This function simulates the change of the rrp over time, till it reaches the end year. This is required since the rrp
changes over time due to 1. inflation and 2. the effects of financial crisis occurring every 9 year and lasting for 
another two years. This function is written in a way that the crisis frequency can be adjusted using
the CRIS_RECUR_FREQ variable.
'''''
def simulate_rrp_from_default_start_year_till_end_year(end_year):
    sales_rrp_dict = dict()             # dict saving the changes to rrp over time

    current_rrp = default_start_rrp     # set initial rrp to default_start_rrp of year 2000
    # define variables to calculate fin crisis
    global_crisis_year_one_factor = default_start_year + CRIS_RECUR_FREQ
    global_crisis_year_two_factor = default_start_year + CRIS_RECUR_FREQ + 1
    global_crisis_year_three_factor = default_start_year + CRIS_RECUR_FREQ + 2

    # boolean variables for fin crisis years, new financial years and peak season
    # are set for later use. If one of these boolean variables are set to
    # to True, the current year is a certain financial crisis year, a new financial year or it is peak season
    global_crisis_year_one_mode = False
    global_crisis_year_one_mode = False
    global_crisis_year_two_mode = False
    global_crisis_year_three_mode = False
    financial_year_mode = False
    peak_season_mode = False

    # create a day, month and year counting variable that enables us to iterate through the the individual days of a
    # year for the purpose of adjusting the rrp over time
    # these 'pointing variables' are set to the start of the companies existence 2000/01/01
    current_day_pointer = default_start_day
    current_month_pointer = default_start_month
    current_year_pointer = default_start_year

    # create a while loop, that continues to iterate through all the years of the simulation
    # where current_year_pointer < end_year
    while current_year_pointer < end_year:
        if is_leap_year(current_year_pointer):  # check whether currently iterated year is a leap year or not
            # if it is, iterate through all 12 months of a certain year
            while current_month_pointer <= 12: # iterate through all 12 months of a year
                while current_day_pointer <= leap_year_days_in_month_dict[current_month_pointer]:

                    # the following if statements check whether the current iterated day is in a financial crisis year
                    # check for whether the currently iterated year is the first year of a financial crisis
                    # needs to meet two conditions: 1. iterated year == fin crisis year one factor and fin crisis year
                    # one should be not True (should be False)
                    # if those conditions are met, adjust rrp by global_financial_crisis_year_one_rrp_increment_factor
                    # and round to two decimals
                    # in the last step the boolean variable to indicate whether a fin crisis is occurring is set to

                    if (current_year_pointer == global_crisis_year_one_factor) and not global_crisis_year_one_mode:
                        current_rrp = round(current_rrp * global_financial_crisis_year_one_rrp_increment_factor, 2)
                        global_crisis_year_one_mode = True

                    # a similar logic is applied to whether the process of checking whetehr a the currently iterated year
                    # is a second financial crisis year, if yes the rrp is adjusted by the global_financial_crisis_
                    # year_two_rrp_increment_factor and rounded to two decimals
                    if (current_year_pointer == global_crisis_year_two_factor) and not global_crisis_year_two_mode:
                        current_rrp = round(current_rrp * global_financial_crisis_year_two_rrp_increment_factor, 2)
                        global_crisis_year_two_mode = True

                    # similar logic as above applies to the process of checking for fin crisis year three
                    if (current_year_pointer == global_crisis_year_three_factor) and not global_crisis_year_three_mode:
                        current_rrp = round(current_rrp * global_financial_crisis_year_three_rrp_increment_factor, 2)
                        global_crisis_year_three_mode = True

                    # the following if statements check whether a certain iterated day is occurring during peak season
                    # does that by checking if the current month counter is >= 11 or <= 2 and peak_season_mode == True
                    # if that is the case rrp gets adjusted based on the peak season rrp increase

                    if (current_month_pointer >= 11 or current_month_pointer <= 2) and not peak_season_mode:
                        current_rrp = round(current_rrp * peak_season_rrp_increment_factor, 2)
                        peak_season_mode = True

                    if (2 < current_month_pointer < 11) and peak_season_mode:
                        # remove the effect of peak season on rrp
                        current_rrp = round(current_rrp / peak_season_rrp_increment_factor, 2)
                        peak_season_mode = False    # set peak season boolean to false again after it is done

                    # after 06/30 the old financial ends, thus financial_year_mode ends to be set to False again
                    if current_month_pointer == 6 and current_day_pointer == 30:
                        financial_year_mode = False

                    # this if statement adjusts rrp for the change in financial years under the condition that the month
                    # counter is = 7 (July) and the days counter is = 1 (start of the new financial year every calender
                    # year
                    if (current_month_pointer == 7) and (current_day_pointer == 1) and not financial_year_mode:
                        current_rrp = round(current_rrp * financial_year_rrp_increment_factor, 2)
                        financial_year_mode = True

                    # this if statement adjusts the variables used to calculate fin crisis after the a end of a of a
                    # financial crisis year
                    if (current_month_pointer == 12 and current_day_pointer == 31) and \
                            (global_crisis_year_one_mode or
                             global_crisis_year_two_mode or
                             global_crisis_year_three_mode):

                        if global_crisis_year_three_mode:
                            global_crisis_year_one_factor = global_crisis_year_three_factor + CRIS_RECUR_FREQ
                            global_crisis_year_two_factor = global_crisis_year_one_factor + 1
                            global_crisis_year_three_factor = global_crisis_year_two_factor + 1

                        # set certain fin crisis indicator boolean variables to False again in case a certain
                        # fin crisis year is done
                        global_crisis_year_one_mode = False
                        global_crisis_year_two_mode = False
                        global_crisis_year_three_mode = False

                    # append the rounded rrp of any iterated day to the sales_rrp_dict as a value, with the date as its
                    # key
                    sales_rrp_dict[(current_day_pointer, current_month_pointer, current_year_pointer)] = \
                        round(current_rrp, 2)

                    current_day_pointer = current_day_pointer + 1  # increment day counter after each iterated day
                # increment month counter after each fully iterated month
                current_month_pointer = current_month_pointer + 1
                current_day_pointer = 1     # reset day counter to one after each month

            current_year_pointer = current_year_pointer + 1     # increment year counter after each fully iterated year
            current_month_pointer = 1                           # reset month counter to one after each year

        # for this part of the if statement we use the same logic as above to iterate through the years until the start
        # of the simulation. The difference is that for this part of the if statement we iterate through non leap years.
        # Since the logic is identical it will not be described again.
        else:    # if current iterated year is not a leap year
            while current_month_pointer <= 12:  # iterate through all 12 months of a certain year
                while current_day_pointer <= non_leap_year_days_in_month_dict[current_month_pointer]:

                    if (current_year_pointer == global_crisis_year_one_factor) and not global_crisis_year_one_mode:
                        current_rrp = round(current_rrp * global_financial_crisis_year_one_rrp_increment_factor, 2)
                        global_crisis_year_one_mode = True

                    if (current_year_pointer == global_crisis_year_two_factor) and not global_crisis_year_two_mode:
                        current_rrp = round(current_rrp * global_financial_crisis_year_two_rrp_increment_factor, 2)
                        global_crisis_year_two_mode = True

                    if (current_year_pointer == global_crisis_year_three_factor) and not global_crisis_year_three_mode:
                        current_rrp = round(current_rrp * global_financial_crisis_year_three_rrp_increment_factor, 2)
                        global_crisis_year_three_mode = True

                    if (current_month_pointer >= 11 or current_month_pointer <= 2) and not peak_season_mode:
                        current_rrp = round(current_rrp * peak_season_rrp_increment_factor, 2)
                        peak_season_mode = True

                    if (2 < current_month_pointer < 11) and peak_season_mode:
                        current_rrp = round(current_rrp / peak_season_rrp_increment_factor, 2)
                        peak_season_mode = False

                    if current_month_pointer == 6 and current_day_pointer == 30:
                        financial_year_mode = False

                    if (current_month_pointer == 7) and (current_day_pointer == 1) and not financial_year_mode:
                        current_rrp = round(current_rrp * financial_year_rrp_increment_factor, 2)
                        financial_year_mode = True

                    if (current_month_pointer == 12 and current_day_pointer == 31) and \
                            (global_crisis_year_one_mode or
                             global_crisis_year_two_mode or
                             global_crisis_year_three_mode):

                        if global_crisis_year_three_mode:
                            global_crisis_year_one_factor = global_crisis_year_three_factor + CRIS_RECUR_FREQ
                            global_crisis_year_two_factor = global_crisis_year_one_factor + 1
                            global_crisis_year_three_factor = global_crisis_year_two_factor + 1

                        global_crisis_year_one_mode = False
                        global_crisis_year_two_mode = False
                        global_crisis_year_three_mode = False

                    sales_rrp_dict[(current_day_pointer, current_month_pointer, current_year_pointer)] = \
                        round(current_rrp, 2)

                    current_day_pointer = current_day_pointer + 1

                current_month_pointer = current_month_pointer + 1
                current_day_pointer = 1

            current_year_pointer = current_year_pointer + 1
            current_month_pointer = 1

    return sales_rrp_dict   # simulate_rrp_from_default_start_year_till_end_year() function returns a dictionary filled
                             # with the rrp changes over time

'''''
This function simulates the change in distributed items per days over time, till it reaches the end year. 
This adjustment is required since the distributed items per days change over time due to 1. increased sales each
financial year and 2. the effects of financial crisis occurring every 9 year and lasting for another two years.
This function is written in a way that the crisis frequency can be adjusted using the CRIS_RECUR_FREQ variable.
The logic for this function is highly similar to the logic of simulate_rrp_from_default_start_year_till_end_year()
function
'''''
def simulate_distributed_items_from_default_start_year_till_end_year(end_year):
    sales_distributed_items_dict = dict()   # dict to save the changes of distributed items per days over time

    # defining variables in one place that will be used throughout the function
    # set starting distributed quantity for the simulation
    current_distributed_quantity = default_start_distributed_quantity
    global_crisis_year_one_factor = default_start_year + CRIS_RECUR_FREQ    # define variables to calculate fin crisis
    global_crisis_year_two_factor = default_start_year + CRIS_RECUR_FREQ + 1  # variable to calculate fin crisis year 2
    global_crisis_year_three_factor = default_start_year + CRIS_RECUR_FREQ + 2 # variable to calculate fin crisis year 3

    # boolean variable for fin crisis years, new financial years and peak season
    # are set for later use. If one of these boolean variables are set to
    # to True, the current year is a certain financial crisis year, a new financial year or it is peak season
    global_crisis_year_one_mode = False
    global_crisis_year_two_mode = False
    global_crisis_year_three_mode = False
    financial_year_mode = False
    peak_season_mode = False

    current_day_pointer = default_start_day # counter variable for days to iterate through the days of a month
    current_month_pointer = default_start_month # counter variable for months to iterate through the months of a year
    current_year_pointer = default_start_year # variable for years to iterate through the years of the simulation

    # as mentioned above the logic use to simulate the change in distributed quantity per day over time is highly
    # similar to the logic use for function simulate_rrp_from_default_start_year_till_end_year().
    # Given this similarity teh description of this logic will not be as detailed since it has be described in detail
    # above.
    # iterate through all the years where current_year_pointer < end_year
    while current_year_pointer < end_year:
        if is_leap_year(current_year_pointer):  # check whether currently iterated year is a leap year or not, if it is
            while current_month_pointer <= 12:  # iterate through all 12 months of ech year
                while current_day_pointer <= leap_year_days_in_month_dict[current_month_pointer]:

                    # the following if statements check whether the current iterated day is in a financial crisis year

                    # check for whether the currently iterated year is the first year of a financial crisis
                    # needs to meet two conditions: 1. iterated year == fin crisis year one factor and fin crisis year
                    # one should be not True (should be False)
                    # if those conditions are met, adjust distributed quantity by
                    # global_financial_crisis_year_one_distributed_quantity_decrement_factor and round the result
                    # in the last step the boolean variable to indicate whether a fin crisis is occurring is set to
                    if (current_year_pointer == global_crisis_year_one_factor) and not global_crisis_year_one_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * \
                            global_financial_crisis_year_one_distributed_quantity_decrement_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        global_crisis_year_one_mode = True

                    # a similar logic is applied to the process of checking whether a the currently iterated
                    # year is a second financial crisis year, if yes the current_distributed_quantity is adjusted
                    # by the global_financial_crisis_year_two_distributed_quantity_decrement_factor and
                    # rounded to two decimals
                    if (current_year_pointer == global_crisis_year_two_factor) and not global_crisis_year_two_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * \
                            global_financial_crisis_year_two_distributed_quantity_decrement_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        global_crisis_year_two_mode = True

                    # similar process as above for fin crisis year 3
                    if (current_year_pointer == global_crisis_year_three_factor) and not global_crisis_year_three_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * \
                            global_financial_crisis_year_three_distributed_quantity_decrement_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        global_crisis_year_three_mode = True

                    # the following if statements check whether a certain iterated day is occurring during peak season
                    # dos that by checking if the current month counter is >= 11 or <= 2 and peak_season_mode == False
                    # if that is the case rrp gets adjusted based on the peak season rrp increase
                    if (current_month_pointer >= 11 or current_month_pointer <= 2) and not peak_season_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * peak_season_distributed_quantity_increment_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        peak_season_mode = True

                    # if peak season is done readjust the current distributed quantity
                    if (2 < current_month_pointer < 11) and peak_season_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity / peak_season_distributed_quantity_increment_factor
                        # removed the effect of peak season on distributed quantity
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        peak_season_mode = False

                    # after 06/30 the old financial ends, thus financial_year_mode ends to be set to False again
                    if current_month_pointer == 6 and current_day_pointer == 30:
                        financial_year_mode = False

                    # this if statement adjusts rrp for the change in financial years under the condition that the month
                    # counter is = 7 (July) and the days counter is = 1 (start of the new financial year every calender
                    # year
                    if (current_month_pointer == 7) and (current_day_pointer == 1) and not financial_year_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * financial_year_distributed_quantity_increment_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        financial_year_mode = True

                    # this if statement adjusts the variables used to calculate fin crisis after the a end of a of a
                    # financial crisis year
                    if (current_month_pointer == 12 and current_day_pointer == 31) and \
                            (global_crisis_year_one_mode or
                             global_crisis_year_two_mode or
                             global_crisis_year_three_mode):

                        if global_crisis_year_three_mode:
                            global_crisis_year_one_factor = global_crisis_year_three_factor + CRIS_RECUR_FREQ
                            global_crisis_year_two_factor = global_crisis_year_one_factor + 1
                            global_crisis_year_three_factor = global_crisis_year_two_factor + 1

                        # set of fin crisis indicator boolean variables to False again
                        global_crisis_year_one_mode = False
                        global_crisis_year_two_mode = False
                        global_crisis_year_three_mode = False

                    # append the rounded distributed quantity of any iterated day to the ales_distributed_items_dict
                    # as a value, with the date as its key
                    sales_distributed_items_dict[(current_day_pointer, current_month_pointer, current_year_pointer)] = \
                        current_distributed_quantity

                    current_day_pointer = current_day_pointer + 1   # increment day counter after each iterated day

                current_month_pointer = current_month_pointer + 1   # increment month after each fully iterated month
                current_day_pointer = 1                             # reset day counter to one after each month

            current_year_pointer = current_year_pointer + 1 # increment year counter after each fully iterated year
            current_month_pointer = 1                       # reset month counter to one after each year

        # for this part of the if statement we use the same logic as above to iterate through the years until the start
        # of the simulation. The difference is that for this part of the if statement we iterate through non leap years.
        # Since the same logic has been applied multiple times before this part of the code will not be spertally
        # given that the logic is the same.
        else:
            while current_month_pointer <= 12:
                while current_day_pointer <= non_leap_year_days_in_month_dict[current_month_pointer]:

                    if (current_year_pointer == global_crisis_year_one_factor) and not global_crisis_year_one_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * \
                            global_financial_crisis_year_one_distributed_quantity_decrement_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        global_crisis_year_one_mode = True

                    if (current_year_pointer == global_crisis_year_two_factor) and not global_crisis_year_two_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * \
                            global_financial_crisis_year_two_distributed_quantity_decrement_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        global_crisis_year_two_mode = True

                    if (current_year_pointer == global_crisis_year_three_factor) and not global_crisis_year_three_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * \
                            global_financial_crisis_year_three_distributed_quantity_decrement_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        global_crisis_year_three_mode = True

                    if (current_month_pointer >= 11 or current_month_pointer <= 2) and not peak_season_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * peak_season_distributed_quantity_increment_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        peak_season_mode = True

                    if (2 < current_month_pointer < 11) and peak_season_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity / peak_season_distributed_quantity_increment_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        peak_season_mode = False

                    if current_month_pointer == 6 and current_day_pointer == 30:
                        financial_year_mode = False

                    if (current_month_pointer == 7) and (current_day_pointer == 1) and not financial_year_mode:
                        current_distributed_quantity = \
                            current_distributed_quantity * financial_year_distributed_quantity_increment_factor
                        current_distributed_quantity = get_rounded_distributed_quantity(current_distributed_quantity)
                        financial_year_mode = True

                    if (current_month_pointer == 12 and current_day_pointer == 31) and \
                            (global_crisis_year_one_mode or
                             global_crisis_year_two_mode or
                             global_crisis_year_three_mode):

                        if global_crisis_year_three_mode:
                            global_crisis_year_one_factor = global_crisis_year_three_factor + CRIS_RECUR_FREQ
                            global_crisis_year_two_factor = global_crisis_year_one_factor + 1
                            global_crisis_year_three_factor = global_crisis_year_two_factor + 1

                        global_crisis_year_one_mode = False
                        global_crisis_year_two_mode = False
                        global_crisis_year_three_mode = False

                    sales_distributed_items_dict[(current_day_pointer, current_month_pointer, current_year_pointer)] = \
                        current_distributed_quantity

                    current_day_pointer = current_day_pointer + 1

                current_month_pointer = current_month_pointer + 1
                current_day_pointer = 1

            current_year_pointer = current_year_pointer + 1
            current_month_pointer = 1

    return sales_distributed_items_dict

'''''
This function calculates the number of defective items that is returned at the end of each month to the company. Then it
saves the amount of defective items as a key to a dict() called defective_and_non_defective_items_monthly_sales_dict.
Based on this knowledge we can adjust the revenue accordingly in the cal_stock_revenue() function.
'''''
def simulate_defective_and_non_defective_items_from_default_start_year_till_end_year(end_year):
    defective_and_non_defective_items_monthly_sales_dict = dict()   # dict to save the defective and non defective items
                                                                    # that occur every month
    defective_items = 0         # defective item counter
    non_defective_items = 0     # non defective item counter

    # call the function simulate_distributed_items_from_default_start_year_till_end_year() with the variable end year as
    # a parameter and save its output (a dict containing the record of distributed items over time) in a dictionary
    # called  distributed_quantity_sales_dict
    distributed_quantity_sales_dict = simulate_distributed_items_from_default_start_year_till_end_year(end_year)
    rrp_sales_dict = simulate_rrp_from_default_start_year_till_end_year(end_year)
    # call the function simulate_rrp_from_default_start_year_till_end_year() with the variable end year as
    # a parameter and save its output (a dict containing the record of rrp changes over time) in a dictionary
    # called rrp_sales_dic

    current_date = (1, 1, default_start_year)   # variable displaying the current date
    current_month = 1                           # variable counter for months
    current_year = default_start_year           # set current year to default start year

    # dict distributed_quantity_sales_dict() contains the daily amount distributed items (values) at
    # different dates in time (keys)
    for date in distributed_quantity_sales_dict:    # using a for loop iterate through dict keys
        current_date = date                         # set current date = to 'date key' in in dict

        # date[1] are the iterated months of every year date[2] are the iterated months
        # at the very end of each month and every year
        # the month of the sales in the sales dict is larger than the current month counter
        # or the year of the sales in the sales dict is larger than the current year counter.
        # If that condition is met we calculate the defectives of a month using the sales of non defectives
        # figure and multiplying it with the defective item percentage (PER_DEF / 100.00)
        if (date[1] > current_month) or (date[2] > current_year):
            defective_items = non_defective_items * (PER_DEF / 100.00)
            defective_items = get_rounded_distributed_quantity(defective_items)     # round defective items

            # append defective + non defective items as a tuple to defective_and_non_defective_items_monthly_sales_dict
            # as values, as well as the matching rrp value for the defective + non defective items
            # with the key being the a tuple of current_month and current_year)
            # turned two dicts into one dict using tuples
            defective_and_non_defective_items_monthly_sales_dict[(current_month, current_year)] = \
                (defective_items, (non_defective_items - defective_items),
                 rrp_sales_dict[(default_start_day, current_month, current_year)], rrp_sales_dict[(default_start_day,
                                                                                                   current_month,
                                                                                                   current_year)])

            current_month = date[1]     # set month counter == to month from distributed_quantity_sales_dict
            current_year = date[2]      # set month counter == to month from distributed_quantity_sales_dict
            non_defective_items = 0     # reset non_defective_item counter

        # for every day calculate the amount of non defectives that have been sold this month on leading up to this day
        # with the following formula:
        non_defective_items = non_defective_items + distributed_quantity_sales_dict[date] - defective_items
        defective_items = 0

    # since the above for loop does not iterate the very last month of the simulated period
    # we need to get the  number of defective items manually one more time
    defective_items = non_defective_items * (PER_DEF / 100.00)
    defective_items = get_rounded_distributed_quantity(defective_items) # round the number of defectives using the
                                                    # ealier defined get_rounded_distributed_quantity() function

    # save the defective items, the non defectives that can be sold after selling the defectives of each month and their
    # respective rrps in the form of a tuple as the value of key that consists of the iterated month and year
    defective_and_non_defective_items_monthly_sales_dict[(current_date[1], current_date[2])] = \
        (defective_items, (non_defective_items - defective_items),
         rrp_sales_dict[current_date], rrp_sales_dict[current_date],
         )

    return defective_and_non_defective_items_monthly_sales_dict     # return dict full of defectives and non defective
                                                # items which can be sold each month until the end of the simulation


'''''
This is the main function of the assignment which calculates the revenue and stock using the input of earlier
functions. The output of the function is a dict called output_data which returns ..
'''''
def cal_stock_revenue(inventory_data):
    # function gets the start year using the value of the key 'start_year' from dict inventory_data which is the
    # functions parameter
    start_year = int(inventory_data['start_year'])
    end_year = int(inventory_data['start_year'] + NO_YEAR_SIM)  # gets end year by adding the number of years of the
                                                                # simulation variable NO_YEAR_SIM

    # function gets the start stock using the value of the key 'start_stock' from dict inventory_data which is the
    # functions parameter
    start_stock = int(inventory_data['start_stock'])
    # function gets the start revenue using the value of the key 'start_revenue' from dict inventory_data which is the
    # functions parameter
    start_revenue = int(inventory_data['start_revenue'])

    output_data = dict()    # define dict that will contain this functions output data

    # read in function simulate_defective_and_non_defective_items_from_default_start_year_till_end_year() which stores
    # the monthly sales of defective items and non defective items given the already sold defective items each month
    # reading in one extra year of records in case information on defectives after simulation end is needed (geared
    # towards task 2)
    defective_and_non_defective_items_sales_dict = \
        simulate_defective_and_non_defective_items_from_default_start_year_till_end_year(end_year + 1)

    defective_items_revenue = 0.00      # create float variable tracking the revenue from defective items
    non_defective_items_revenue = 0.00  # create float variable tracking the revenue from non defective items

    start_flag = False      # create boolean variable used to indicate the start of the simulation
    target_months = []      # create list for target months

    # using a for loop iterate through the dict defective_and_non_defective_items_sales_dict, which stores monthly
    # sales of defective items and non defective items
    for date in defective_and_non_defective_items_sales_dict:
        # if month == Jan and year == end year the end of the simulation is reached, break loop
        if (date[0] == 1) and (date[1] == end_year):
            break

        # if month == Jan and year == start year of the simulation, the function starts appending relevant sales data
        # to target_months list
        if (date[0] == 1) and (date[1] == start_year):
            target_months.append(date)
            start_flag = True           # set boolean variable indicating the start of the simulation to True
            continue

        # if boolean variable indicating the start of the simulation is True, continue on appending relevant sales data
        # to target_months list
        if start_flag:
            target_months.append(date)

    # iterate through the monthly defective and non defective item sales list
    for date in target_months:
        # for month != January and year != end of the simulation year
        if (date[0] != 1) and (date[1] != end_year):
            # rounded defective_items_revenue for a certain month equals to the number of defective items * rrp of that
            # month * the defective items sales price percentage (0.80)
            defective_items_revenue = round(
                defective_items_revenue + (defective_and_non_defective_items_sales_dict[date][0] *
                                           defective_and_non_defective_items_sales_dict[date][2] *
                                           defective_items_rrp_percentage), 2)


        non_defective_items_revenue = \
            round(non_defective_items_revenue + (defective_and_non_defective_items_sales_dict[date][1] *
                                                 defective_and_non_defective_items_sales_dict[date][3]), 2)

    # after all the months of the target year have been iterated through set start_stock to end_stock
    end_stock = start_stock
    # save call the function simulate_distributed_items_from_default_start_year_till_end_year() with the variable end
    # year as a parameter and save its output (a dict containing the record of distributed items over time) in a
    # dictionary called distributed_items_dict
    distributed_items_dict = simulate_distributed_items_from_default_start_year_till_end_year(end_year)

    stock_calculation_start_flag = False    # create boolean variable used to indicate the start of the
                                            # stock_calculation_start_flag
    target_dates_for_stock = []             # create list for target dates for stock

    # iterate through all the years from 2000 till the end year of the simulation
    #
    for date in distributed_items_dict:
        # if the date is == 01/01/end_year break out off the for loop
        if (date[0] == 1) and (date[1] == 1) and (date[2] == end_year):
            break

        #if the date is == 01/01/start_year append
        if (date[0] == 1) and (date[1] == 1) and (date[2] == start_year):
            # append the dates (month/year) of the simulated year to the list target_dates_for_stock, in this case only
            # January
            target_dates_for_stock.append(date)
            # set boolean variable stock_calculation_start_flag, used to indicate the start of the stock calculation
            # to True
            stock_calculation_start_flag = True
            continue

        # if statement which is excecuted when stock_calculation_start_flag == True
        if stock_calculation_start_flag:
            # append the rest of the dates (month/year) of the simulated year to the list target_dates_for_stock
            target_dates_for_stock.append(date)

    # iterate through each day (date) in target_dates_for_stock
    for date in target_dates_for_stock:
        # calculate the end of the day stock for each day day through the target year by subtracting the daily
        # distributed quantity from
        end_stock = end_stock - distributed_items_dict[date]

        # if stock drops under 400 units at the end of a day, restock 600 units again
        if end_stock <= 400:
            end_stock = end_stock + 600

    # add data as values into output data_data dict for the keys 'end_year','end_stock','end_revenue'
    output_data['end_year'] = int(end_year)
    output_data['end_stock'] = int(end_stock)
    output_data['end_revenue'] = \
        round(round(start_revenue, 2) + round(defective_items_revenue, 2) + round(non_defective_items_revenue, 2), 2)
        # add up all three rounded revenue components
    return output_data

'''''
This function writes data form a dict called 'output_data' to a txt file called “AU_INV_END.txt”. The data contains
the 1. Ending year, 2. Total stock available at the end of the year, and 3. Ending revenue for the year which was 
simulated. After that the function closes the txt file. 
'''''
def write_data(output_data):
    f = open('AU_INV_END_TASK_1.txt', 'w')
    f.write(str(output_data['end_year']) + '\n')
    f.write(str(output_data['end_stock']) + '\n')
    f.write(str(output_data['end_revenue']))
    f.close()

# this if statement is responsible for executing all three main functions read_data(), cal_stock_revenue(), and
# write_data()
if __name__ == '__main__':
    start_data = read_data()
    end_data = cal_stock_revenue(start_data)
    write_data(end_data)
    print(end_data)
