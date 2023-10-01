import csv
from discord.ext import commands, tasks
from discord.utils import get
from oauth2client import client
from os.path import exists
import datetime

import nanowrimo
import dataprocessing

import discord

intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

# adjust_sprintstats - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Adds or subtracts numerical values from a certain user's sprint stats
# INPUTS:
#       - (int) value: the value that will be added or subtracted from the day and sum total
#       - (int) user_id: the discord id of the user whose totals will be adjusted
#       - (string) sprint_bot_counter_filename: the location of the CSV file where the historical sprint data is stored
# RETURNS:
#       - (int) error: an error code. 0 if all is well, -1 if the user is not listed in the documentation.
def adjust_sprintstats(value, user_id, sprint_bot_counter_filename):
    error = 0
    found_user = 0

    # Check to make sure if the user with id user_id is actually in the sprint document
    temp_file = list()

    # Read through data file
    with open(sprint_bot_counter_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = ",")

        # Print to temp file while also checking if user ID already exists
        for row in reader:
            temp_file.append(row)
            for current_id in row:
                if current_id == str(user_id):
                    found_user = 1
                    
                    # If the user ID is found, remove it from the temp file
                    temp_file.remove(row)

                    # Adjust the word count values
                    wc = int(value) + int(row[1])
                    week_wc = int(value) + int(row[2])
                    month_wc = int(value) + int(row[3])
                    year_wc = int(value) + int(row[4])
                    lifetime_wc = int(value) + int(row[5])
                    NaNo_Goal = int(row[6])

                    # Print the new adjusted word count back to the CSV
                    out = [user_id, str(wc), str(week_wc), str(month_wc), str(year_wc), str(lifetime_wc), str(NaNo_Goal)]
                    # output_string += "@%s: %s words\n" % (username, str(wc))
                    temp_file.append(out)

        # If the user is new to the list, return an error
        if found_user != 1:
            error = -1
            
        # Print the temp file back out to the CSV file
        with open(sprint_bot_counter_filename, "w") as loaded_file:
            writer = csv.writer(loaded_file, delimiter = ",")
            writer.writerows(temp_file)

    return error

# count_user_sprints - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# This function counts the number of sprints a user has completed while EndoBot was running. Used for statistics!
# INPUTS:
#       - (string) user_sprint_totals_folder_name: the name of the folder wherein all user sprint data is stored
#       - (int) user_id: the discord ID for the user whose data will be read
# RETURNS:
#       - (int) count: the count of the number of sprints the user has participated in
def count_user_sprints(user_sprint_totals_folder_name, user_id):
    # Build the filepath of the user
    user_sprint_totals_filepath = str(user_sprint_totals_folder_name) + "/" + str(user_id) + ".csv"

    # Check to see if the file exists
    if not exists(user_sprint_totals_filepath):
        return -1

    # Open the file
    reader = csv.reader(open(user_sprint_totals_filepath))

    # Read the number of lines
    number_of_lines = len(list(reader))

    return number_of_lines

# process_sprint_word_counts - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes word count values collected from other Discord sprint assist bots and imports them into the sprint counter file.
# INPUTS:
#       - (string) sprint_bot_counter_filename: the location of the CSV file where the historical sprint data is stored 
#       - (string) current_sprinter_id: the ID for the current user whose sprint statistics are being modified.
#       - (string) current_sprinter_wc: the user's word count.
# RETURNS:
#       - N/A
def process_sprint_word_counts(sprint_bot_counter_filename, current_sprinter_id, current_sprinter_wc):
        # Check to see if the user is already listed in the CSV
        found_user = 0

        # Generate a temporary array to store CSV data in
        temp_file = list()

            # Read through output file
        with open(sprint_bot_counter_filename, "r") as loaded_file:
            reader = csv.reader(loaded_file, delimiter = ",")

            # Print to temp file while also checking if user ID already exists
            for row in reader:
                temp_file.append(row)
                for current_id in row:
                    if current_id == current_sprinter_id:
                        found_user = 1
                        # If the user ID is found, remove it from the temp file
                        temp_file.remove(row)

                        # Example configuration line: [User_ID (pos 0)],[Day_Total (pos 1)],[Week_Total (pos 2)],[Month_Total (pos 3)],[Year_Total (pos 4)],[Lifetime_Total (pos 5)],[NaNo_Goal (pos 6)]

                        # Combine the new word count with the old one
                        wc = int(current_sprinter_wc) + int(row[1])
                        week_wc = int(current_sprinter_wc) + int(row[2])
                        month_wc = int(current_sprinter_wc) + int(row[3])
                        year_wc = int(current_sprinter_wc) + int(row[4])
                        lifetime_wc = int(current_sprinter_wc) + int(row[5])
                        NaNo_Goal = int(row[6])

                        # Print the new combo word count to the CSV
                        out = [current_sprinter_id, str(wc), str(week_wc), str(month_wc), str(year_wc), str(lifetime_wc), str(NaNo_Goal)]
                        # output_string += "@%s: %s words\n" % (username, str(wc))
                        temp_file.append(out)
                    
            # If the user is new to the list, add them and their word count as-is
            if found_user != 1:
                out = [current_sprinter_id, current_sprinter_wc, current_sprinter_wc, current_sprinter_wc, current_sprinter_wc, current_sprinter_wc, 0]
                # output_string += "@%s: %s words\n" % (username, current_sprinter_wc)
                temp_file.append(out)
            
        # Print the temp file back out to the CSV file
        with open(sprint_bot_counter_filename, "w") as loaded_file:
            writer = csv.writer(loaded_file, delimiter = ",")
            writer.writerows(temp_file)

# sprinto_word_count_processor  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Retrieves usernames and word counts for each sprint and adds them to the tabulator.
# INPUTS:
#       - (string) message_contents: the contents of the message
#       - (string) sprint_bot_counter_filename: the location of the CSV file where the historical sprint data is stored 
#       - (string) nanowrimo_filename: the location of the CSV file where the NaNoWriMo data is stored
#       - (string) nanowrimo_enabled: either "Yes" or "No", this determines whether a NaNoWriMo challenge is currently ongoing
#       - (string) sprint_bot_individual_counter_folder: the location of the folder containing the server's complete user sprint data
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: 0 if successful, <0 if not
#       - (string list) all_sprinter_ids: a list of all user IDs that were processed in the sprint bot completion message
#       - (string list) all_printer_wcs: a list of all user's sprint statistics in the sprint bot completion message
def sprinto_word_count_processor(message_contents, sprint_bot_counter_filename, nanowrimo_filename, nanowrimo_enabled, sprint_bot_individual_counter_folder, current_guild_id):
    all_sprinter_ids = list()
    all_sprinter_wcs = list()

    today = datetime.date.today()

    day = today.day
    month = today.month
    year = today.year
    # week = datetime.date(year, month, day).isocalendar()[1]

    today_dateformatted = "%s-%s-%s" % (str(year), str(month), str(day))

    status = 0
    output_string = "" # "**Current Yearly Total Sprint Stats**\n\n"

    # Begin by parsing @Sprinto's output message and retrieve the user ID and the word count
    sprinters = message_contents.split("<@!")

    # In the newly created array of user ID/word count pairs, begin to sort through them one by one to see if they're already listed in the CSV
    cc = 0
    for i in sprinters:
        # Skip the first entry in the array as it is junk
        if cc == 0:
            cc += 1
            continue

        # Split the User ID and the word count apart
        interim = i.split("> — **")
        current_sprinter_id = interim[0]

        if i.find("word deleted") != -1:
            interim2 = interim[1].split(" word deleted**")
            interim2[0] = "-" + interim2[0]
        elif i.find("words deleted") != -1:
            interim2 = interim[1].split(" words deleted**")
            interim2[0] = "-" + interim2[0]
        elif i.find("word**") != -1:
            interim2 = interim[1].split(" word**")
        elif i.find("words**") != -1:
            interim2 = interim[1].split(" words**")

        current_sprinter_wc = interim2[0]
        current_sprinter_wc = current_sprinter_wc.replace(",","")

        all_sprinter_ids.append(current_sprinter_id)
        all_sprinter_wcs.append(current_sprinter_wc)

        process_sprint_word_counts(sprint_bot_counter_filename, current_sprinter_id, current_sprinter_wc)

        # Add the sprint result to the NaNoWriMo counter, if a NaNoWriMo challenge is currently in effect
        if nanowrimo_enabled == "True":
            nanowrimo.add_nano_words(nanowrimo_filename, current_sprinter_id, current_sprinter_wc)

        # Print user's contribution into their respective sprint stats csv
        status = dataprocessing.dump_to_user_file(sprint_bot_individual_counter_folder, current_sprinter_id, today_dateformatted, current_sprinter_wc)

    return status, all_sprinter_ids, all_sprinter_wcs

# writerbot_word_count_processor - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Retrieves usernames and word counts for each sprint and adds them to the tabulator.
# INPUTS:
#       - (string) message_contents: the contents of the message
#       - (string) sprint_bot_counter_filename: the location of the CSV file where the historical sprint data is stored 
#       - (string) nanowrimo_filename: the location of the CSV file where the NaNoWriMo data is stored
#       - (string) nanowrimo_enabled: either "Yes" or "No", this determines whether a NaNoWriMo challenge is currently ongoing
#       - (string) sprint_bot_individual_counter_folder: the location of the folder containing the server's complete user sprint data
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: 0 if successful, <0 if not
#       - (string list) all_sprinter_ids: a list of all user IDs that were processed in the sprint bot completion message
#       - (string list) all_printer_wcs: a list of all user's sprint statistics in the sprint bot completion message
def writerbot_word_count_processor(message_contents, sprint_bot_counter_filename, nanowrimo_filename, nanowrimo_enabled, sprint_bot_individual_counter_folder, current_guild_id):
    all_sprinter_ids = list()
    all_sprinter_wcs = list()

    today = datetime.date.today()

    day = today.day
    month = today.month
    year = today.year
    # week = datetime.date(year, month, day).isocalendar()[1]

    today_dateformatted = "%s-%s-%s" % (str(year), str(month), str(day))

    status = 0
    output_string = "" # "**Current Yearly Total Sprint Stats**\n\n"

    # Begin by parsing @Writer-Bot's output message and retrieve the user ID and the word count
    sprinters = message_contents.split("<@")

    # In the newly created array of user ID/word count pairs, begin to sort through them one by one to see if they're already listed in the CSV
    cc = 0
    for i in sprinters:
        # Skip the first entry in the array as it is junk
        if cc == 0:
            cc += 1
            continue  

        # Since a feature of @Writer-Bot is the ability to sprint without a wordcount, wordcounts not being provided is a frequent possibility  
        # Check to see if there is a word count
        if i.find("**") != -1:
            # Split the User ID and the word count apart
            interim = i.split("> — **")
            current_sprinter_id = interim[0]

            if i.find("word**") != -1:
                interim2 = interim[1].split(" word**")
            elif i.find("words**") != -1:
                interim2 = interim[1].split(" words**")

            current_sprinter_wc = interim2[0]
            current_sprinter_wc = current_sprinter_wc.replace(",","")

        # If a wordcount isn't provided, set the WC to 0 and proceed as normal
        else:
            # Split the User ID and the word count apart
            interim = i.split(">")
            current_sprinter_id = interim[0]

            current_sprinter_wc = 0
        
        all_sprinter_ids.append(current_sprinter_id)
        all_sprinter_wcs.append(current_sprinter_wc)

        process_sprint_word_counts(sprint_bot_counter_filename, current_sprinter_id, current_sprinter_wc)

        # Add the sprint result to the NaNoWriMo counter, if a NaNoWriMo challenge is currently in effect
        if nanowrimo_enabled == "True":
            nanowrimo.add_nano_words(nanowrimo_filename, current_sprinter_id, current_sprinter_wc)

        # Print user's contribution into their respective sprint stats csv
        status = dataprocessing.dump_to_user_file(sprint_bot_individual_counter_folder, current_sprinter_id, today_dateformatted, current_sprinter_wc)

    return status, all_sprinter_ids, all_sprinter_wcs