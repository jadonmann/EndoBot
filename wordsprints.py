import csv
from discord.ext import commands, tasks
from discord.utils import get
from oauth2client import client

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

def test_script(discord_client, user_id):
    username = discord_client.get_user(user_id)
    split_username = str(username).split("#")

    return split_username