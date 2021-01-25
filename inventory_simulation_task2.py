'''
Inventory_simulation_task2

Author: Armin Berger

This program is an inventory management system for a company selling cantilever umbrellas.
It will provide the user with the stock count and revenue at the end of an n year cycle given a certain input date.

Some of the features of this program are fully adopted from task 1 or are adopted with slight changes to accommodate for 
the requirements of task 2. The reason why we are able to transfer a lot of code from task 1 to task 2, is because task
1 was developed in a manner that individual components woudld meet both task 1 and 2 requirements. 

An example of that can be seen in the functions simulate_rrp_from_default_start_year_till_end_year() and 
simulate_distributed_items_from_default_start_year_till_end_year() where temporary adjustments are made to rrp and 
distributed quantity in accordance with whether it is peak season or not. This would have not be necessary to do for
task 1 since the these changes are temporary and have no long run effect on the distributed quantity and rrp over the
years. Directly including this feature when writing task one, however, makes the code easily transferable to task 2
without major adjustments.

This program uses Boolean variables in combination with loops to check for the occurrence of certain conditions and
adjust variables over time.

The program overall has x functions of which each is annotate in accordance to their purpose and function.

The following set of additional assumptions were made:
- When defectives are sold at the start of each month they are deducted from inventory like any other normal sales

'''''

# This is a collection of global variables that are used throughout the entire program in different functions
# In case the user wants to change any of these variables, this can be conveniently done here and no further adjustments
# to the code need to be made
NO_YEAR_SIM = 3  # number of years of the simulation, can be customized but is set to 3 years by default
PER_DEF = 5     # percentage of defective items that get returned to the company every month, can be customized but is
                # set to 5 by default
CRIS_RECUR_FREQ = 9 # frequency of financial crisis, can be customized but is set to 9 years by default

default_start_year = 2000   # the year the company was found and based upon which all starting variables are based on
default_start_month = 1     # the month the company was found
default_start_day = 1        # the day the company was found

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
        year = int(date_string[0:4])
        if year < 2000:
            raise ValueError
        else:
            return year
    except ValueError:
        print("Incorrect Date Format. "
              "Date Format must be YYYYMMDD and YYYY should be >= 2000 . "
              "Default Start Year of 2000 will be used.")
        return default_start_year

# catch faulty month inputs that don't meet the date format (months smaller than 1 and larger than 12)
# using try and except block
def get_month(date_string):
    try:
        month = int(date_string[4:6])
        if month < 1 or month > 12:
            raise ValueError
        else:
            return month
    except ValueError:
        print("Incorrect Date Format. "
              "Date Format must be YYYYMMDD and MM should be >= 01 and <= 12 . "
              "Default Start Month of 01 will be used.")
        return default_start_month

# catch faulty days input that does't meet the date format (check January has 31 days, in case of a leap year, that
# feb has 29 days, etc. ) using try and except block
# this is done by comparing the input date int(date_string[6:8]) with the days of a certain month in the
# leap_year_days_in_month_dict and the non_leap_year_days_in_month_dict
def get_day(date_string):
    try:
        day = int(date_string[6:8])
        if is_leap_year(int(date_string[0:4])): # checks days in a month for leap years
            if day < 1 or day > leap_year_days_in_month_dict[int(date_string[4:6])]:
                raise ValueError
            else:
                return day
        else:            # checks days in a month for a non leap years
            if day < 1 or day > non_leap_year_days_in_month_dict[int(date_string[4:6])]:
                raise ValueError
            else:
                return day
    except ValueError:
        print("Incorrect Date Format. "
              "Date Format must be YYYYMMDD and DD should be >= 1 and <=31 depending on the month and leap year. "
              "Default Start Day of 01 will be used.")
        return default_start_day

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
This function reads in data form a txt file called “AU_INV_START.txt”. The data contains 1. Starting date,
2. Total stock available, and 3. Starting revenue for the starting date from which onwards the simulation will be done. 
The data which is being read in is stored as int values in a dictionary. The key names for these three values
are "start_date": XXX, "start_stock": XXX, "start_revenue": XXX .
'''''
def read_data():
    data = dict()   # dictionary that stores the read in file date

    # use of try and except block to catch faulty data input
    try:
        f = open('AU_INV_START_TASK_2.txt')         # create file handle that reads in file date
        file_lines = f.readlines()                  # read line by line of file handel f using readlines() function
    except FileNotFoundError:                       # throw error in case file is not found and no data could be read in
        print('Input File not Found. Exiting ...')
        exit(0)                                    # exit program, user should check whether “AU_INV_START.txt” exists
                                                   # or is saved in the right folder

    for i in range(0, len(file_lines)):             # iterate through each line in the file using a for loop
        file_lines[i] = ''.join(file_lines[i].split())
        file_lines[i] = file_lines[i].strip()        #strip line of whitespace
        if not file_lines[i] in ['\n', '\r\n', '']: # ?
            if i == 0:          # if line equals to first line of the file
                # save input as value for key 'start_date' in dict data
                data['start_date'] = (get_year(file_lines[i]), get_month(file_lines[i]), get_day(file_lines[i]))
            elif i == 1:        # if line equals to second line of the file
                data['start_stock'] = get_stock_value(file_lines[i]) # save input as value for key 'start_stock'
            elif i == 2:        # if line equals to third line of the file
                data['start_revenue'] = get_revenue_value(file_lines[i])   # save input as value for key 'start_revenue'
            # if condition not met print error 'incorrect data' and exit program
            else:
                print('Incorrect Data Format for File. Exiting ...')
                exit(0)
        # if condition not met print error 'incorrect data' and exit program
        else:
            print('Incorrect Data Format for File. Exiting ...')
            exit(0)

    return data

'''''
This function checks whether a year is a leap year or not. A leap year usually every 4 years. Every 100 year a leap year
is skipped unless the year is divisible by 400. The alogrithm performed for these calculations adapts the structure taken
from https://www.programiz.com/python-programming/examples/leap-year . If a year turns out to be a leap year a Boolaen
variable = True is returned 
'''''
def is_leap_year(year):
    if (year % 4) == 0: # use remainder operate to check whether year is evenly dividable by 4 and is thus
                         # a potential leap year
        if (year % 100) == 0:   # use remainder operate to check whether year is evenly dividable by 100, if yes then
            if (year % 400) == 0:   # use the remainder operate to check whether year is evenly dividable by 400,
                return True         # if so year is a leap year
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


def get_start_date(data):
    start_year = int(data[0])
    start_month = int(data[1])
    start_day = int(data[2])
    return start_year, start_month, start_day


def get_end_date(data):
    start_year = int(data[0])
    end_year = start_year + NO_YEAR_SIM
    end_month = int(data[1])
    end_day = int(data[2])

    return end_year, end_month, end_day

# utility function to validate values
#
def get_total_number_of_days_from_start_date_till_end_date(data):
    data = data['start_date']
    start_year = int(data[0])
    start_month = int(data[1])
    start_day = int(data[2])

    end_year, end_month, end_day = get_end_date(data)

    current_year_pointer = start_year
    current_month_pointer = start_month
    current_day_pointer = start_day

    total_days_counted = 0

    end_date_reached = False

    while current_year_pointer < end_year:
        while current_month_pointer <= 12:
            if is_leap_year(current_year_pointer):
                while current_day_pointer <= leap_year_days_in_month_dict[current_month_pointer]:
                    if (current_day_pointer == end_day) and (current_month_pointer == end_month) and (
                            current_year_pointer == end_year):
                        end_date_reached = True
                        break
                    total_days_counted = total_days_counted + 1
                    current_day_pointer = current_day_pointer + 1

                if end_date_reached:
                    break
                current_month_pointer = current_month_pointer + 1
                current_day_pointer = 1
            else:
                while current_day_pointer <= non_leap_year_days_in_month_dict[current_month_pointer]:
                    if (current_day_pointer == end_day) and (current_month_pointer == end_month) and (
                            current_year_pointer == end_year):
                        end_date_reached = True
                        break
                    total_days_counted = total_days_counted + 1
                    current_day_pointer = current_day_pointer + 1

                if end_date_reached:
                    break
                current_month_pointer = current_month_pointer + 1
                current_day_pointer = 1

        if end_date_reached:
            break

        current_year_pointer = current_year_pointer + 1
        current_month_pointer = 1

    return total_days_counted
'''''
This function simulates the change of the rrp over time, till it reaches the end year. This is required since the rrp
changes over time due to 1. inflation and 2. the effects of financial crisis occurring every 9 year and lasting for 
another two years. This function is written in a way that the crisis frequency can be adjusted using
the CRIS_RECUR_FREQ variable.
'''''
def simulate_rrp_from_default_start_year_till_end_year(end_year):
    sales_rrp_dict = dict()     # dict saving the changes to rrp over time

    current_rrp = default_start_rrp     # set initial rrp to default_start_rrp of year 2000
                                        # define variables to calculate fin crisis

    # fin cris variables which allow us to calculate whether a certain year is a fin crisis year
    global_crisis_year_one_factor = default_start_year + CRIS_RECUR_FREQ
    global_crisis_year_two_factor = default_start_year + CRIS_RECUR_FREQ + 1
    global_crisis_year_three_factor = default_start_year + CRIS_RECUR_FREQ + 2

    # boolean variables for fin crisis years, new financial years and peak season
    # are set for later use. If one of these boolean variables are set to
    # to True, the current year is a certain financial crisis year, a new financial year or it is peak season
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
            while current_month_pointer <= 12:      # iterate through all 12 months of a year
                while current_day_pointer <= leap_year_days_in_month_dict[current_month_pointer]:

                    # the following if statements check whether the current iterated day is in a financial crisis year
                    # check for whether the currently iterated year is the first year of a financial crisis
                    # needs to meet two conditions: 1. iterated year == fin crisis year one factor and fin crisis year
                    # one should be not True (should be False)
                    # if those conditions are met, adjust rrp by global_financial_crisis_year_one_rrp_increment_factor
                    # and round to two decimals
                    # in the last step the boolean variable to indicate whether a fin crisis is occurring is set to

                    if (current_year_pointer == global_crisis_year_one_factor) and not global_crisis_year_one_mode:
                        print(current_year_pointer,global_crisis_year_one_factor)
                        current_rrp = round(current_rrp * global_financial_crisis_year_one_rrp_increment_factor, 2)
                        global_crisis_year_one_mode = True

                    # a similar logic is applied to whether the process of checking whether a the currently iterated
                    # year is a second financial crisis year, if yes the rrp is adjusted by the global_financial_crisis_
                    # year_two_rrp_increment_factor and rounded to two decimals
                    if (current_year_pointer == global_crisis_year_two_factor) and not global_crisis_year_two_mode:
                        print(current_year_pointer, global_crisis_year_one_factor)
                        current_rrp = round(current_rrp * global_financial_crisis_year_two_rrp_increment_factor, 2)
                        global_crisis_year_two_mode = True

                    # similar logic as above applies to the process of checking for fin crisis year three
                    if (current_year_pointer == global_crisis_year_three_factor) and not global_crisis_year_three_mode:
                        print(current_year_pointer, global_crisis_year_one_factor)
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

                    current_day_pointer = current_day_pointer + 1    # increment day counter after each iterated day
                # increment month counter after each fully iterated month

                current_month_pointer = current_month_pointer + 1
                current_day_pointer = 1         # reset day counter to one after each month

            current_year_pointer = current_year_pointer + 1 # increment year counter after each fully iterated year
            current_month_pointer = 1               # reset month counter to one after each year

        # for this part of the if statement we use the same logic as above to iterate through the years until the start
        # of the simulation. The difference is that for this part of the if statement we iterate through non leap years.
        # Since the logic is identical it will not be described again.
        else:   # if current iterated year is not a leap year
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
function.
'''''
def simulate_distributed_items_from_default_start_year_till_end_year(end_year):
    sales_distributed_items_dict = dict()   # dict to save the changes of distributed items per days over time

    # defining variables in one place that will be used throughout the function
    # set starting distributed quantity for the simulation

    # fin cris variables which allow us to calculate whether a certain year is a fin crisis year
    current_distributed_quantity = default_start_distributed_quantity
    global_crisis_year_one_factor = default_start_year + CRIS_RECUR_FREQ
    global_crisis_year_two_factor = default_start_year + CRIS_RECUR_FREQ + 1
    global_crisis_year_three_factor = default_start_year + CRIS_RECUR_FREQ + 2

    # boolean variable for fin crisis years, new financial years and peak season
    # are set for later use. If one of these boolean variables are set to
    # to True, the current year is a certain financial crisis year, a new financial year or it is peak season
    global_crisis_year_one_mode = False
    global_crisis_year_two_mode = False
    global_crisis_year_three_mode = False
    financial_year_mode = False
    peak_season_mode = False

    current_day_pointer = default_start_day     # counter variable for days to iterate through the days of a month
    current_month_pointer = default_start_month # counter variable for months to iterate through the months of a year
    current_year_pointer = default_start_year   # variable for years to iterate through the years of the simulation

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
                        # removed the effect of peak season on distributed quantity
                        current_distributed_quantity = \
                            current_distributed_quantity / peak_season_distributed_quantity_increment_factor
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
                current_day_pointer = 1                          # reset day counter to one after each month

            current_year_pointer = current_year_pointer + 1     # increment year counter after each fully iterated year
            current_month_pointer = 1               # reset month counter to one after each year

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
    defective_items = 0         # create defective item counter
    non_defective_items = 0     # create non defective item counter

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
    current_year = default_start_year            # set current year to default start year

    # dict distributed_quantity_sales_dict() contains the daily amount distributed items (values) at
    # different dates in time (keys)
    for date in distributed_quantity_sales_dict:    # using a for loop iterate through the dates of the dict
        current_date = date                         # set current date = to 'date key' in in dict

        # date[1] are the iterated months of every year date[2] are the iterated months
        # at the very end of each month and every year
        # the month of the sales in the sales dict is larger than the current month counter
        # or the year of the sales in the sales dict is larger than the current year counter.
        # If that condition is met we calculate the defectives of a month using the sales of non defectives
        # figure and multiplying it with the defective item percentage (PER_DEF / 100.00)
        if (date[1] > current_month) or (date[2] > current_year):
            defective_items = non_defective_items * (PER_DEF / 100.00)
            defective_items = get_rounded_distributed_quantity(defective_items) # round defective items

            # append defective + non defective items as a tuple to defective_and_non_defective_items_monthly_sales_dict
            # as values, as well as the matching rrp value for the defective + non defective items
            # with the key being the a tuple of current_month and current_year)
            # turned two dicts into one dict using tuples
            defective_and_non_defective_items_monthly_sales_dict[(current_month, current_year)] = \
                (defective_items, (non_defective_items - defective_items),
                 rrp_sales_dict[(default_start_day, current_month, current_year)], rrp_sales_dict[(default_start_day,
                                                                                                   current_month,
                                                                                                   current_year)])

            current_month = date[1] # set month counter == to month from distributed_quantity_sales_dict
            current_year = date[2]  # set month counter == to month from distributed_quantity_sales_dict
            non_defective_items = 0 # reset non_defective_item counter

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

    return defective_and_non_defective_items_monthly_sales_dict # return dict full of defectives and non defective
                                                # items which can be sold each month until the end of the simulation
''''
This function is unique to task 2. It calculates the amount of defectives which are available for sale per day. This is
required since we need to know the amount of defectives which can be sold every day since it impacts the revenue
of a day. That is particularly important for the first month and last month of the simulation since the date of the
simulation start could be in the middle of a month and thus we need to consider how many defectives in that month have 
been sold already.
As parameters it reads in the defective_and_non_defective_items_monthly_sales_dict and the starting date of the 
simulation as day, month and year.
'''''
def simulate_defective_and_non_defective_items_for_specific_month(defective_and_non_defective_items_monthly_sales_dict,
                                                                  day,
                                                                  month,
                                                                  year):
    specific_month_sales_dict = dict()  # dict saving the specific sales data for a given month

    # call the function simulate_distributed_items_from_default_start_year_till_end_year() with the variable end year as
    # a parameter and save its output (a dict containing the record of distributed items over time) in a dictionary
    # called  distributed_quantity_sales_dict
    # to cover edge cases (test examining either the beginning or the end of a range) in this program an extra year of
    # data is read in as a safety buffer in case that information is needed
    distributed_quantity_sales_dict = simulate_distributed_items_from_default_start_year_till_end_year(year + 1)
    rrp_sales_dict = simulate_rrp_from_default_start_year_till_end_year(year + 1)
    # call the function simulate_rrp_from_default_start_year_till_end_year() with the variable end year as
    # a parameter and save its output (a dict containing the record of rrp changes over time) in a dictionary
    # called rrp_sales_dic
    # to cover edge cases (test examining either the beginning or the end of a range) in this program an extra year of
    # data is read in as a safety buffer in case that information is needed

    # Next we need to figuring out where we are starting with our simulation (specific date) since the stock,
    # defective and revenue calculations are all impacted by this
    # First check for the special case of January 2000, where you don't need to consider defectives which are carried
    # over from a previous month
    # if month == jan year == 2000 then defective_items = 0 and defective_items_rrp = 0.00
    if month == default_start_month and year == default_start_year:
        defective_items = 0
        defective_items_rrp = 0.00
    else:           # used in case month == jan but year != 2000 (larger than 2000 in all cases)
        if (month == default_start_month) and (year > default_start_year):
            # for a given year during January the number of defective_items from last years December are saved
            # needed for January revenue calculation
            defective_items = defective_and_non_defective_items_monthly_sales_dict[(12, year - 1)][0]
            defective_items_rrp = rrp_sales_dict[(default_start_day, 12, year - 1)]
            # for a given year during January the rrp for defectives from last years December are saved
            # needed for January revenue calculation

        # use same logic as above
        # for a given year during any month then than Jan the number of defective_items from last month are saved
        # needed for the months revenue calculation
        else:       # use when month is > jan
            defective_items = defective_and_non_defective_items_monthly_sales_dict[(month - 1, year)][0]
            defective_items_rrp = rrp_sales_dict[(default_start_day, month - 1, year)]
            # for a given year during any month then than Jan the rrp of defectives from last month are saved
            # needed for the months revenue calculation

    distributed_quantity = distributed_quantity_sales_dict[(day, month, year)]
    non_defective_items_rrp = rrp_sales_dict[(default_start_day, month, year)]

    # for a given year during January of a year > 2000 defect items = a date tuple (dd/mm/yyyy) and a tuple
    # documenting (the number of defectives which can be sold on a certain day, the number of non defectives
    # sold, the rrp defectives are sold at, and the rrp non defectives are sold at)

    # iterate through all the dates in distributed_quantity_sales_dict (which contains the number of units distributed
    # every day over time until the end of the simulation)
    for date in distributed_quantity_sales_dict:
        current_month = date[1] # set current month counter == currently iterated month in dict
        current_year = date[2]  # set current year counter == currently iterated month in dict
        # in case month and year counter are equal to the starting month and year of the simulation
        # set the default_start_day to the currently iterated day
        if (current_month == month) and (current_year == year):
            current_day = default_start_day
            if is_leap_year(date[2]):   # check for whether iterated year is a leap year
                # iterate through the days of a certain month
                while current_day <= leap_year_days_in_month_dict[current_month]:
                    # check whether defective items are larger than the daily distributed_quantity
                    if defective_items > distributed_quantity:
                        # if yes , the actually distributed quantity of regular items on that particular date is 0
                        # thus this needs to be reflected in specific_month_sales_dict
                        specific_month_sales_dict[(current_day, current_month, current_year)] = (
                            distributed_quantity, 0, defective_items_rrp, non_defective_items_rrp)
                    else:
                        if defective_items > 0: # condition in case there are some non defectives left
                            # if yes , the actually distributed quantity of regular items on that particular date is
                            # distributed_quantity - defective_items and needs to be saved in specific_month_sales_dict
                            specific_month_sales_dict[(current_day, current_month, current_year)] = \
                                (defective_items, distributed_quantity - defective_items, defective_items_rrp,
                                 non_defective_items_rrp)
                        # if there are no defectives left on a certain date the number of defective_items on that day is
                        # 0 and the distributed_quantity does not need to be adjusted
                        else:
                            specific_month_sales_dict[(current_day, current_month, current_year)] = \
                                (0, distributed_quantity, defective_items_rrp, non_defective_items_rrp)
                    defective_items = defective_items - distributed_quantity
                    current_day = current_day + 1   # increase day counter by 1
            # in case the currently iterated year is not a leap year use the same logic as above but with the
            # non_leap_year_days_in_month_dict as a base of the iteration
            else:
                while current_day <= non_leap_year_days_in_month_dict[current_month]:
                    if defective_items > distributed_quantity:
                        specific_month_sales_dict[(current_day, current_month, current_year)] = (
                            distributed_quantity, 0, defective_items_rrp, non_defective_items_rrp)
                    else:
                        if defective_items > 0:
                            specific_month_sales_dict[(current_day, current_month, current_year)] = \
                                (defective_items, distributed_quantity - defective_items, defective_items_rrp,
                                 non_defective_items_rrp)
                        else:
                            specific_month_sales_dict[(current_day, current_month, current_year)] = \
                                (0, distributed_quantity, defective_items_rrp, non_defective_items_rrp)
                    defective_items = defective_items - distributed_quantity
                    current_day = current_day + 1
            break   # after starting month of simulation is done, break

    #print('MONTH - YEAR : '+ str(month) +', '+str(year))

    return specific_month_sales_dict    # return data on day by day unit sales considering defectives


'''''
This function uses the same logic as simulate_defective_and_non_defective_items_for_specific_month but this time it is
applied to the end month of the simulated time period. 
It calculates the amount of defectives which are available for sale per day. This is
required since we need to know the amount of defectives which can be sold every day since it impacts the revenue
of a day.As parameters it reads in the defective_and_non_defective_items_monthly_sales_dict and the ending date of the 
simulation as end_day, end_month and end_year. These parameters are then used in the
simulate_defective_and_non_defective_items_for_specific_month function and append the data to the 
specific_month_sales_dict.
'''''
def simulate_defective_and_non_defective_items_for_ending_month(defective_and_non_defective_items_monthly_sales_dict,
                                                                end_day,
                                                                end_month,
                                                                end_year):
    specific_month_sales_dict = \
        simulate_defective_and_non_defective_items_for_specific_month(
            defective_and_non_defective_items_monthly_sales_dict, end_day, end_month, end_year)

    return specific_month_sales_dict

'''''
This function calculates the revenue of the first month of simulation, starting on the specific date entered. Since a 
starting date might be in the middle of a month it is required to calculate the day by day revenue of the starting
months. 
'''''
def get_first_month_revenue(specific_month_sales_dict, first_day):
    defective_items_revenue = 0.00          # set float variable to save defective_items_revenue
    non_defective_items_revenue = 0.00      # set float variable to save non_defective_items_revenue

    # iterate through all days of the starting month of the specific_month_sales_dict
    for date in specific_month_sales_dict:
        # if day of month in starting month of the specific_month_sales_dict >= the first day of the simulation
        if date[0] >= first_day:
            # calculate rounded defective_items_revenue by multiplying number of defectives to be sold with
            # matching defective rrp
            defective_items_revenue = round(
                defective_items_revenue + (specific_month_sales_dict[date][0] *
                                           specific_month_sales_dict[date][2] *
                                           defective_items_rrp_percentage), 2)

            # calculate rounded non_defective_items_revenue by multiplying number of non_defectives with regular rrp
            non_defective_items_revenue = \
                round(non_defective_items_revenue + (specific_month_sales_dict[date][1] *
                                                     specific_month_sales_dict[date][3]), 2)

    # get first month revenue of simulation by adding revenue of defective_items and non_defective_items
    first_month_revenue = round(defective_items_revenue + non_defective_items_revenue, 2)

    return first_month_revenue  # return first_month_revenue float

'''''
This function calculates the revenue of the last month of simulation. Since the ending date might be in the middle of
a month, it is required to calculate the day by day revenue of the starting months. Follows the same logic as the above
function get_first_month_revenue() but does it for the last month.
'''''
def get_last_month_revenue(specific_month_sales_dict, last_day):
    defective_items_revenue = 0.00      # set float variable to save defective_items_revenue
    non_defective_items_revenue = 0.00  # set float variable to save non_defective_items_revenue

    # iterate through all days of the starting month of the specific_month_sales_dict
    for date in specific_month_sales_dict:
        if date[0] < last_day:
            # calculate rounded defective_items_revenue by multiplying number of defectives to be sold with
            # matching defective rrp
            defective_items_revenue = round(
                defective_items_revenue + (specific_month_sales_dict[date][0] *
                                           specific_month_sales_dict[date][2] *
                                           defective_items_rrp_percentage), 2)
            # calculate rounded non_defective_items_revenue by multiplying number of non_defectives with regular rrp
            non_defective_items_revenue = \
                round(non_defective_items_revenue + (specific_month_sales_dict[date][1] *
                                                     specific_month_sales_dict[date][3]), 2)

    # get first month revenue of simulation by adding revenue of defective_items and non_defective_items
    last_month_revenue = round(defective_items_revenue + non_defective_items_revenue, 2)

    return last_month_revenue   # return first_month_revenue float



'''''
This function calculates the revenue from defective and non defective items in the 'middle' months of the simulation 
(months between the start and end month). The function uses data from the 
defective_and_non_defective_items_monthly_sales_dict to calculate the revenue for these 'middle months'.
'''''
def get_middle_months_revenue(defective_and_non_defective_items_monthly_sales_dict,
                              first_month, last_month, first_year, last_year):
    defective_items_revenue = 0.00      # set float variable to save defective_items_revenue
    non_defective_items_revenue = 0.00  # set float variable to save non_defective_items_revenue

    start_flag = False  # create boolean variable (used as indicator) and set it to false
    target_months = []  # create list called target_months

    # iterate through the months of the defective_and_non_defective_items_monthly_sales_dict
    for date in defective_and_non_defective_items_monthly_sales_dict:
        # if month in dict == to last month of simulation and last year of simulation, break
        # we break because for the last month of the simulation we need to use the get_last_month_revenue() function
        if (date[0] == last_month) and (date[1] == last_year):
            break       # breaks and thus excludes anything past the last month of the end year of simulation

        # detects whether we have entered the first month of our simulation
        if (date[0] == first_month) and (date[1] == first_year):
            start_flag = True   # sets boolean indicator == True
            continue
        # start localising the middle months of our simulation
        if start_flag:
            target_months.append(date)

    # iterate through all middle months of the simulation between start and end month of the simulation
    for date in target_months:
        # calculate rounded defective_items_revenue by multiplying number of defectives to be sold with
        # matching defective rrp
        defective_items_revenue = round(
            defective_items_revenue + (defective_and_non_defective_items_monthly_sales_dict[date][0] *
                                       defective_and_non_defective_items_monthly_sales_dict[date][2] *
                                       defective_items_rrp_percentage), 2)

        # calculate rounded non_defective_items_revenue by multiplying number of non_defectives with regular rrp
        non_defective_items_revenue = \
            round(non_defective_items_revenue + (defective_and_non_defective_items_monthly_sales_dict[date][1] *
                                                 defective_and_non_defective_items_monthly_sales_dict[date][3]), 2)

    # get middle month revenue of simulation by adding revenue of defective_items and non_defective_items
    middle_months_revenue = round(defective_items_revenue + non_defective_items_revenue, 2)

    return middle_months_revenue    # return middle month revenue dict


'''''
This function writes data form a dict called 'output_data' to a txt file called “AU_INV_END.txt”. The data contains
the 1. Ending date, 2. Total stock available at the end of the simulation period, and 3. Ending revenue for the 
simulation period. After that the function closes the txt file. 
'''''
def write_data(output_data):
    f = open('AU_INV_END_TASK_2.txt', 'w')
    f.write(str(output_data['end_year']) + '\n')
    f.write(str(output_data['end_stock']) + '\n')
    f.write(str(output_data['end_revenue']))
    f.close()

'''''
This is the main function of the assignment which calculates the revenue and stock using the input of earlier
functions. The output of the function is a dict called output_data which returns ..
'''''
def cal_stock_revenue(inventory_data):
    output_data = dict()    # create  output_data dict

    # function gets the start date using the values of the key 'start_date' in dict inventory_data
    # from function get_start_date() which is the functions parameter
    start_year, start_month, start_day = get_start_date(inventory_data['start_date'])
    end_year, end_month, end_day = get_end_date(inventory_data['start_date'])
    # function gets the end date using the values of the key 'start_date'  in dict inventory_data from the
    # function get_end_date()

    start_stock = int(inventory_data['start_stock']) # reads in starting inventory using the parameter inventory_data
    start_revenue = int(inventory_data['start_revenue']) # reads in start revenue using the parameter inventory_data

    # read in defective and non defective sales data using the
    # simulate_defective_and_non_defective_items_from_default_start_year_till_end_year() function
    defective_and_non_defective_items_monthly_sales_dict = \
        simulate_defective_and_non_defective_items_from_default_start_year_till_end_year(end_year + 1)

    # if the simulation does not start on the first day of a month, we need to work on an individual day base
    if start_day != default_start_day:

        # revenue of the first month is calculated using the get_first_month_revenue() function in combination with the
        # simulate_defective_and_non_defective_items_for_specific_month() function
        # the sales data needed is taken from defective_and_non_defective_items_monthly_sales_dict
        first_month_revenue = \
            get_first_month_revenue(
                simulate_defective_and_non_defective_items_for_specific_month(
                    defective_and_non_defective_items_monthly_sales_dict, start_day, start_month, start_year),
                start_day)

        # revenue of the middle months is calculated using the get_middle_months_revenue() function
        # the sales data needed is taken from defective_and_non_defective_items_monthly_sales_dict
        middle_months_revenue = \
            get_middle_months_revenue(defective_and_non_defective_items_monthly_sales_dict,
                                      start_month, end_month, start_year, end_year)

        # revenue of the last month is calculated using the get_last_month_revenue() function in combination with the
        # simulate_defective_and_non_defective_items_for_specific_month() function
        # the sales data needed is taken from defective_and_non_defective_items_monthly_sales_dict
        last_month_revenue = \
            get_last_month_revenue(
                simulate_defective_and_non_defective_items_for_specific_month(
                    defective_and_non_defective_items_monthly_sales_dict, end_day, end_month, end_year), end_day)

        # to get the end revenue we add start_revenue, first_month_revenue, middle_months_revenue, and
        # last_month_revenue. We then round the sum of that result
        end_revenue = round(start_revenue, 2) + round(first_month_revenue + middle_months_revenue + last_month_revenue,
                                                   2)

    # if the simulation starts on the first day of a month we can work with full month data instead of having
    # to work with daily data
    else:
        defective_items_revenue = 0.00      # set defective_items_revenue to 0
        non_defective_items_revenue = 0.00  # set non_defective_items_revenue to 0

        start_flag = False      # create boolean variable, indicating the start of the simulation, and set to False
        target_months = []      # create list for targeted months of simulation (summary of all simulated months

        # iterate through the months of defective_and_non_defective_items_monthly_sales_dict
        for date in defective_and_non_defective_items_monthly_sales_dict:
            # if month == to end month of the simulation and year == to end year of the simulation break
            if (date[0] == end_month) and (date[1] == end_year):
                break

            # if month == to start month of the simulation and year == to start year of the simulation
            # starting appending the dates of the simulated period to target_months list and set boolean indicator to
            # True
            if (date[0] == start_month) and (date[1] == start_year):
                target_months.append(date)
                start_flag = True
                continue

            # while boolean indicator is set to True, continue on appending the simulated period to target_months list
            if start_flag:
                target_months.append(date)

        # iterate through target_months using for loop
        for date in target_months:
            # if month is unequal to the end_month and year is unequal to the end_year
            # calculate rounded defective_items_revenue by multiplying number of defectives to be sold with
            # matching defective rrp of a certain month
            if (date[0] != end_month) and (date[1] != end_year):
                defective_items_revenue = round(
                    defective_items_revenue + (defective_and_non_defective_items_monthly_sales_dict[date][0] *
                                               defective_and_non_defective_items_monthly_sales_dict[date][2] *
                                               defective_items_rrp_percentage), 2)
            # calculate rounded non_defective_items_revenue by multiplying number of non_defectives with regular rrp
            # of a certain month
            non_defective_items_revenue = \
                round(non_defective_items_revenue + (defective_and_non_defective_items_monthly_sales_dict[date][1] *
                                                     defective_and_non_defective_items_monthly_sales_dict[date][3]), 2)

        # to get the end revenue we add start_revenue, first_month_revenue, middle_months_revenue, and
        # last_month_revenue. We then round the sum of that result
        end_revenue = round(start_revenue, 2) + round(defective_items_revenue, 2) + round(non_defective_items_revenue,
                                                                                          2)
    end_stock = start_stock     # set end_stock equal to start_stock
    # call the function simulate_distributed_items_from_default_start_year_till_end_year() with the variable end year as
    # a parameter and save its output (a dict containing the record of distributed items over time) in a dictionary
    # called distributed_items_dict
    # to cover edge cases (test examining either the beginning or the end of a range) in this program an extra year of
    # data is read in as a safety buffer in case that information is needed
    distributed_items_dict = simulate_distributed_items_from_default_start_year_till_end_year(end_year + 1)

    # create boolean variable, indicating the start of the simulation, and set to False
    stock_calculation_start_flag = False
    target_dates_for_stock = []     # create list for targeted months of simulation (summary of all simulated months

    # iterate through the dates of distributed_items_dict
    for date in distributed_items_dict:
        # if day == to end day, month == to end month of the simulation, and year == to end year of the simulation break
        if (date[0] == end_day) and (date[1] == end_month) and (date[2] == end_year):
            break

        # if day == to start day, month == to start month , and year == to start year of the simulation
        # starting appending the dates of the simulated period to target_dates_for_stock list and set
        # boolean indicator to True
        if (date[0] == start_day) and (date[1] == start_month) and (date[2] == start_year):
            target_dates_for_stock.append(date)
            stock_calculation_start_flag = True
            continue

        # while boolean indicator is set to True, continue on appending the simulated period to
        # target_dates_for_stock list
        if stock_calculation_start_flag:
            target_dates_for_stock.append(date)

    # iterate through each date in target_dates_for_stock list using a for loop
    for date in target_dates_for_stock:
        # subtract the daily quantity of the overall stock each day
        end_stock = end_stock - distributed_items_dict[date]

        # if stock level <= 400 at the end of a day, reorder 600 units
        if end_stock <= 400:
            end_stock = end_stock + 600

    # based on th length of months and days (single vs double digits) we need to append a 0 to months or days to
    # get a uniform date that follows the yyyy/mm/dd format
    if (len(str(end_month)) == 2) and (len(str(end_day)) == 2):
        output_data['end_year'] = str(end_year) + str(end_month) + str(end_day)
    elif (len(str(end_month)) == 1) and (len(str(end_day)) == 2):
        output_data['end_year'] = str(end_year) + '0' + str(end_month) + str(end_day)
    elif (len(str(end_month)) == 2) and (len(str(end_day)) == 1):
        output_data['end_year'] = str(end_year) + str(end_month) + '0' + str(end_day)
    else:
        output_data['end_year'] = str(end_year) + '0' + str(end_month) + '0' + str(end_day)

    # add key 'end_stock' with value int(end_stock) and key 'end_revenue' with rounded value end_revenue
    output_data['end_stock'] = int(end_stock)
    output_data['end_revenue'] = round(end_revenue, 2)

    return output_data

#
if __name__ == '__main__':
    start_data = read_data()
    end_data = cal_stock_revenue(start_data)
    write_data(end_data)
    print(end_data)
