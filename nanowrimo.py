import csv
from async_timeout import asyncio
from oauth2client import client
import discord
import calendar
import datetime

# set_nano_goal  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Sets the user's NaNoWriMo monthly goal to their chosen value
# INPUTS:
#       - (string) sprint_counter_filename: the location of the sprint counter filename
#       - (string) user_id: the ID in column 0 of the sprint counter filename
#       - (int) goal_to_set: the word count to be saved to the sprint counter file 
# RETURNS:
#       - (int) status: the error status of the function. 0 if okay, less than 0 if not 
def set_nano_goal(sprint_bot_counter_filename, user_id, goal_to_set):
    # Check to see if the user is already listed in the CSV
    found_user = 0

    # Generate a temporary array to store CSV data in
    temp_file = list()

    # Open and search the sprint counter CSV
    # Read through output file
    with open(sprint_bot_counter_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = ",")

        # Print to temp file while also checking if user ID already exists
        for row in reader:
            temp_file.append(row)
            if str(row[0]) == str(user_id):
                found_user = 1
                # If the user ID is found, remove it from the temp file
                temp_file.remove(row)

                # Print the new NaNo goal to the file
                out = [str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(goal_to_set)]
                temp_file.append(out)

        # If the user is new to the list, add them and their word count as-is
        if found_user != 1:
            out = [str(user_id), str(0), str(0), str(0), str(0), str(0), str(goal_to_set)]
            temp_file.append(out)

    # Print the temp file back out to the CSV file
    with open(sprint_bot_counter_filename, "w") as loaded_file:
        writer = csv.writer(loaded_file, delimiter = ",")
        writer.writerows(temp_file)

    return 0

# delete_nano_goal - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Sets the user's NaNoWriMo monthly goal to 0
# INPUTS:
#       - (string) sprint_counter_filename: the location of the sprint counter filename
#       - (string) user_id: the ID in column 0 of the sprint counter filename
# RETURNS:
#       - (int) return_val: the error status of the function. 0 if okay, less than 0 if not 
def delete_nano_goal(sprint_bot_counter_filename, user_id):
    return_val = set_nano_goal(sprint_bot_counter_filename, user_id, 0)
    return return_val

# see_nano_goal  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Checks the user's NaNoWriMo word count goal as well as their current progress
# INPUTS:
#       - (string) sprint_counter_filename: the location of the sprint counter filename
#       - (string) user_id: the ID in column 0 of the sprint counter filename
# RETURNS:
#       - (int) NaNo_Goal: the requested goal, and also the error status of the function. Any positive value if okay, less than 0 if not 
#       - (int) Current_Monthly_Progress: current word count of the total month 
def see_nano_goal(sprint_bot_counter_filename, user_id):
    # Check to see if the user is already listed in the CSV
    found_user = 0

    NaNo_Goal = 0

    # Open and search the sprint counter CSV
    # Read through output file
    with open(sprint_bot_counter_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = ",")

        for row in reader:
            if str(row[0]) == str(user_id):
                found_user = 1
                
                NaNo_Goal = int(row[6])
                Current_Monthly_Progress = int(row[3])

    if found_user == 1:
        return NaNo_Goal, Current_Monthly_Progress
    
    return -1, -1

# see_nano_goal  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Sets EVERY user's NaNoWriMo monthly goal to 0 (done at the beginning of each month)
# INPUTS:
#       - (string) sprint_counter_filename: the location of the sprint counter filename
# RETURNS:
#       N/A
def reset_all_nano_goals(sprint_bot_counter_filename):
   # Generate a temporary array to store CSV data in
    temp_file = list()

    # Open and search the sprint counter CSV
    # Read through output file
    with open(sprint_bot_counter_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = ",")

        # Print to temp file while also scrubbing file
        for row in reader:
            # Print the updated NaNo goal to the file
            out = [str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(0)]
            temp_file.append(out)

    # Print the temp file back out to the CSV file
    with open(sprint_bot_counter_filename, "w") as loaded_file:
        writer = csv.writer(loaded_file, delimiter = ",")
        writer.writerows(temp_file)

    return 0

# nano_leaderboard - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Generates a Discord embed that lists and sorts all users' word count totals for the current NaNo session
# INPUTS:
#       - (string) sprint_counter_filename: the location of the sprint counter CSV file to be processed
# RETURNS:
#       - (zip) tuples: the zipped list containing all seven lists' data - this is processed within the main script
def nano_leaderboard(sprint_counter_filename):
    user_id = list()
    day_word_count = list()
    week_word_count = list()
    month_word_count = list()
    year_word_count = list()
    lifetime_word_count = list()
    nano_goal_count = list()

    # Open the sprint count file
    with open(sprint_counter_filename, "r") as opened_file:
        opened_csv = csv.reader(opened_file, delimiter = ",")

        for row in opened_csv:
            user_id.append(int(row[0]))
            day_word_count.append(int(row[1]))
            week_word_count.append(int(row[2]))
            month_word_count.append(int(row[3]))
            year_word_count.append(int(row[4]))
            lifetime_word_count.append(int(row[5]))
            nano_goal_count.append(int(row[6]))
        
        # Sort all users, greatest to least, by zipping the two arrays together and sorting by the second array
        zipped_list = zip(user_id, day_word_count, week_word_count, month_word_count, year_word_count, lifetime_word_count, nano_goal_count)

        sorted_list = sorted(zipped_list, key = lambda x: x[1], reverse = True)

        # Unzip the arrays so they can be re-zipped later during the embed buildup
        tuples = zip(*sorted_list)

        return tuples

# calculate_daily_goal - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Calculates the remaining number of days in a month and the number of remaining words required to "win" the challenge
# INPUTS:
#       - (int) goal: the numerical goal loaded in from the word count CSV file
#       - (int) progress: the number of words written so far in the month, also loaded in from the word count CSV file
# RETURNS:
#       - (int) daily_goal: the goal required to "win" the challenge
def calculate_daily_goal(goal, progress):
    # Determine the number of remaining days in the current month
    today = datetime.datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    todays_date = int(today.strftime("%d"))

    remaining_days = 1 + days_in_month - todays_date
    
    # Calculate daily goal
    daily_goal = 0
    delta_wc = int(goal) - int(progress)
    if delta_wc >= 0:
        # Goal not yet complete
        daily_goal = round(delta_wc/remaining_days, 3)
    else:
        daily_goal = 0

    return daily_goal

# nano_leaderboard_prostprocessing - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Generates an output message used in a Discord Embed that is used for a NaNoWriMo Leaderboard
# INPUTS:
#       - (zip) tuples: large data storage list used to carry sprint data lines between Python functions
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
def nano_leaderboard_postprocessing(tuples, client):
    user_list, day_wc, week_wc, month_wc, year_wc, lifetime_wc, nano_goal  = [list(tuple) for tuple in tuples]
    output_message = ""

    number_of_participants = 0

    # Print out sorted results to embed
    for i, j, k, l, m, n, o in zip(user_list, day_wc, week_wc, month_wc, year_wc, lifetime_wc, nano_goal):
        # Only display the user if they have a nonzero word count goal
        if int(o) != 0:
            number_of_participants += 1

            # Example configuration line: [User_ID (pos 0)],[Day_Total (pos 1)],[Week_Total (pos 2)],[Month_Total (pos 3)],[Year_Total (pos 4)],[Lifetime_Total (pos 5)],[NaNo_Goal (pos 6)]

            month_wc_postprocessed = int(l)
            nano_goal_postprocessed = int(o)

            daily_goal = calculate_daily_goal(nano_goal_postprocessed, month_wc_postprocessed)
            percentage_complete = month_wc_postprocessed/nano_goal_postprocessed * 100

            username = client.get_user(int(i))
            split_username = str(username).split("#")

            output_message_interim = "**@%s**:\n\t%s of %s words completed - %s percent\n\t%s words/day to finish on time!\n" % (split_username[0], str(month_wc_postprocessed), str(nano_goal_postprocessed), str(round(percentage_complete, 2)), str(round(daily_goal, 2)))
            output_message = output_message + output_message_interim

    if number_of_participants == 0:
        return 0, "There are no users participating!"
    elif number_of_participants != 0:
        return 0, output_message
    else:   
        return -1, "NULL"


# nano_final_leaderboard_prostprocessing - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Generates an output message used in the final Discord Embed that runs at the end of a NaNo month
# INPUTS:
#       - (zip) tuples: large data storage list used to carry sprint data lines between Python functions
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
def nano_final_leaderboard_postprocessing(tuples, client):
    user_list, day_wc, week_wc, month_wc, year_wc, lifetime_wc, nano_goal  = [list(tuple) for tuple in tuples]
    output_message = ""

    number_of_participants = 0

        # Print out sorted results to embed
    for i, j, k, l, m, n, o in zip(user_list, day_wc, week_wc, month_wc, year_wc, lifetime_wc, nano_goal):
        # Only display the user if they have a nonzero word count goal
        if int(o) != 0:
            number_of_participants += 1

            # Example configuration line: [User_ID (pos 0)],[Day_Total (pos 1)],[Week_Total (pos 2)],[Month_Total (pos 3)],[Year_Total (pos 4)],[Lifetime_Total (pos 5)],[NaNo_Goal (pos 6)]

            month_wc_postprocessed = int(l)
            nano_goal_postprocessed = int(o)

            daily_goal = calculate_daily_goal(nano_goal_postprocessed, month_wc_postprocessed)
            percentage_complete = month_wc_postprocessed/nano_goal_postprocessed * 100

            username = client.get_user(int(i))
            split_username = str(username).split("#")

            if percentage_complete < 100:
                output_message_interim = "**@%s**:\n\t%s of %s words completed! (%s percent)\n" % (split_username[0], str(month_wc_postprocessed), str(nano_goal_postprocessed), str(round(percentage_complete, 2)))
            else:
                output_message_interim = "**@%s**:\n\t%s of %s words completed! (%s percent) - 🏆🏆 WINNER 🏆🏆\n" % (split_username[0], str(month_wc_postprocessed), str(nano_goal_postprocessed), str(round(percentage_complete, 2)))
            output_message = output_message + output_message_interim

    if number_of_participants == 0:
        return 0, "There are no users participating!"
    elif number_of_participants != 0:
        return 0, output_message
    else:   
        return -1, "NULL"