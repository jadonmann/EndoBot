from os.path import exists
import csv

# Sprint Stats TODO:
#       - most sprints in a day
#       - most productive day
#       - most words in a single sprint
#       - a few graphs (maybe one with each day for the month, and then another that's monthly for the last calendar year)

# dump_to_user_file  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# When prompted, write a new set of user data to a file - and if that file doesn't exist, create it
# INPUTS:
#       - (string) folder_name: the plaintext name of the folder wherein all the user data csv files are stored
#       - (string) user_id: the ID for the user whose data is currently being added to. Also used to load/generate the user's CSV file
#       - (string) date: current date in UTC format (doesn't have to be anything fancy, since it'll only ever be used internally)
#       - (int) word_count: word count value to be passed through to file
# RETURNS:
#       - (int) status: 0 if no errors, <0 otherwise
def dump_to_user_file(folder_name, user_id, date, word_count):
    #Create temp file to store interim values
    temp_file = list()

    # Build user's individually stored data file path
    filename = str(folder_name) + "/" + str(user_id) + ".csv"

    # First, check to see if that file already exists
    if exists(filename):
        # If it does exist, open it and read it through, line by line, and print to an intermediary 
        with open(filename, "r") as current_file:
            reader = csv.reader(current_file, delimiter = ",")
            
            # Build temp file with file's current data
            for row in reader:
                temp_file.append(row)
            
            # Add the new data addition to the next line
            out = [date, str(word_count)]
            temp_file.append(out)

    else:
        # If it doesn't exist, create it and populate the first entry with today's date
        with open(filename, "w") as current_file:
            out = [str(date), str(word_count)]
            temp_file.append(out)

    # Print the temp file back out to the CSV file
    with open(filename, "w") as current_file:
        writer = csv.writer(current_file, delimiter = ",")
        writer.writerows(temp_file)

    return 0

# read_user_file - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Reads a user's file and outputs each row of the file into a comma-delimited 
# INPUTS:
#       - (string) folder_name: the plaintext name of the folder wherein all the user data csv files are stored
#       - (string) user_id: the ID for the user whose data is currently being added to. Also used to load/generate the user's CSV file
#       - (string) date: current date in UTC format (doesn't have to be anything fancy, since it'll only ever be used internally)
# RETURNS:
#       - (int) status: 0 if no errors, -1 if file does not exist
#       - (list) temp_file: ingressed user file, used for further processing in the chain
def read_user_file(folder_name, user_id):
    # Create temp file to store interim values
    temp_file = list()

    # Build user's individually stored data file path
    filename = str(folder_name) + "/" + str(user_id) + ".csv"

    # First, check to see if that file exists
    if exists(filename):
        # If it does exist, open it and read it through, line by line, and print to an intermediary 
        with open(filename, "r") as current_file:
            reader = csv.reader(current_file, delimiter = ",")
            
            # Build temp file with file's current data
            for row in reader:
                temp_file.append(row)

        return 0, temp_file
    else:
        return -1, temp_file