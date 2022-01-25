########################################################################################################
# ENDOBOT ============================================================================================ #
#
# Built using the Discord.py Python API
# Written by JA Mann
# 
# Release 2022.01.24.B
# Release Notes: 
# - Added in functionality to print and display the daily NYT Spelling Bee Puzzle at a certain time every day
# - Added in functionality to view and change configuration file parameters
# - Added in functionality to keep track of all words sprinted using the @Sprinto bot
# - Added in functionality to pull a random line from an AO3 fanfiction (still in development)
#                   
#
# ============================================================================================ ENDOBOT #
########################################################################################################




# ==================================================================================================== #
# IMPORTS AND GLOBAL VARIABLES ----------------------------------------------------------------------- #

from __future__ import print_function
#from asyncio.windows_events import NULL
from async_timeout import asyncio
from cv2 import line
from discord.ext import commands, tasks
from discord.utils import get
from oauth2client import client
from os.path import exists

import random
import discord
import numpy as np
import datetime
import csv
import re

import requests
from html2image import Html2Image
import configparser

# Enables ability to check member IDs within a server (used for Leaderboard functionality)
# This requires a specific permission through Discord's API and will need to be renewed periodically
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

TOKEN = "Your_Token_Here"
CONFIG_FILENAME = "configuration.ini"
GUILD_ID = "Your_Guild_ID_Here"

FILENAME = None
RECEIPTS_FILENAME = None
STARBOARD_OUTPUT_CHANNEL_ID = None
STARBOARD_REACTION_THRESHOLD = None
STARBOARD_EMOJI_DELIMITER = None
RESPONSE_FLAG = None
RESPONSE_FLAG_CASE_SENSITIVE = None
RESPONSE_FLAG_MATCH_EXACT_CASE = None
LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME = None
HOTWORDS_FILENAME = None
MACHINE_LEARNING_RESPONSE_FLAG = None
SPELLING_BEE_URL = None
SPELLING_BEE_OUTPUT_CHANNEL_ID = None
SPELLING_BEE_AUTO_POST = None
SPELLING_BEE_POST_TIME = None
SPELLING_BEE_HTML = None
SPELLING_BEE_CSS = None
SPELLING_BEE_PNG = None
SPRINT_BOT_COUNTER = None
SPRINT_BOT_AUTOTRIGGER = None

DAILY_MESSAGE_TIME = None


# ----------------------------------------------------------------------- IMPORTS AND GLOBAL VARIABLES #
# ==================================================================================================== #



# ==================================================================================================== #
# INITIALIZATIONS ------------------------------------------------------------------------------------ #

# initialize_bot - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Initializes the bot with configuration information read from an INI file
# INPUTS:
#       - (string) config_filename: the master configuration file name
#       - (string) servername: the name of the server to search for in the configuration file INI structure
# RETURNS:
#       - (int) error: returns an error code if there's a problem, 0 otherwise

def initialize_bot(config_filename, servername):
    global FILENAME
    global RECEIPTS_FILENAME
    global STARBOARD_OUTPUT_CHANNEL_ID
    global STARBOARD_REACTION_THRESHOLD
    global STARBOARD_EMOJI_DELIMITER
    global RESPONSE_FLAG
    global RESPONSE_FLAG_CASE_SENSITIVE
    global RESPONSE_FLAG_MATCH_EXACT_CASE
    global LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME
    global HOTWORDS_FILENAME
    global MACHINE_LEARNING_RESPONSE_FLAG
    global SPELLING_BEE_URL
    global SPELLING_BEE_OUTPUT_CHANNEL_ID
    global SPELLING_BEE_AUTO_POST
    global SPELLING_BEE_POST_TIME
    global SPELLING_BEE_HTML
    global SPELLING_BEE_CSS
    global SPELLING_BEE_PNG
    global SPRINT_BOT_COUNTER
    global SPRINT_BOT_AUTOTRIGGER

    global DAILY_MESSAGE_TIME
    
    exists = 0
    
    exists, FILENAME = read_ini_file(config_filename, servername, "starboard_filename")
    if exists == -1:
        return -2
    exists, RECEIPTS_FILENAME = read_ini_file(config_filename, servername, "starboard_receipts")
    if exists == -1:
        return -3
    exists, STARBOARD_OUTPUT_CHANNEL_ID = read_ini_file(config_filename, servername, "starboard_output_channel_id")
    if exists == -1:
        return -4
    exists, STARBOARD_REACTION_THRESHOLD = read_ini_file(config_filename, servername, "starboard_reaction_threshold")
    if exists == -1:
        return -5
    exists, STARBOARD_EMOJI_DELIMITER = read_ini_file(config_filename, servername, "starboard_emoji_delimiter")
    if exists == -1:
        return -6
    exists, RESPONSE_FLAG = read_ini_file(config_filename, servername, "response_flag")
    if exists == -1:
        return -7
    exists, RESPONSE_FLAG_CASE_SENSITIVE = read_ini_file(config_filename, servername, "response_flag_case_sensitive")
    if exists == -1:
        return -8
    exists, RESPONSE_FLAG_MATCH_EXACT_CASE = read_ini_file(config_filename, servername, "response_flag_match_exact_case")
    if exists == -1:
        return -9
    exists, LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME = read_ini_file(config_filename, servername, "loaded_external_media_config_filename")
    if exists == -1:
        return -10
    exists, HOTWORDS_FILENAME = read_ini_file(config_filename, servername, "hotwords_filename")
    if exists == -1:
        return -11
    exists, MACHINE_LEARNING_RESPONSE_FLAG = read_ini_file(config_filename, servername, "machine_learning_response_flag")
    if exists == -1:
        return -12
    exists, SPELLING_BEE_URL = read_ini_file(config_filename, servername, "spelling_bee_url")
    if exists == -1:
        return -13
    exists, SPELLING_BEE_OUTPUT_CHANNEL_ID = read_ini_file(config_filename, servername, "spelling_bee_output_channel_id")
    if exists == -1:
        return -14
    exists, SPELLING_BEE_AUTO_POST = read_ini_file(config_filename, servername, "spelling_bee_auto_post")
    if exists == -1:
        return -15
    exists, SPELLING_BEE_POST_TIME = read_ini_file(config_filename, servername, "spelling_bee_post_time")
    if exists == -1:
        return -16
    exists, SPELLING_BEE_HTML = read_ini_file(config_filename, servername, "spelling_bee_html")
    if exists == -1:
        return -17
    exists, SPELLING_BEE_CSS = read_ini_file(config_filename, servername, "spelling_bee_css")
    if exists == -1:
        return -18
    exists, SPELLING_BEE_PNG = read_ini_file(config_filename, servername, "spelling_bee_png")
    if exists == -1:
        return -19
    exists, SPRINT_BOT_COUNTER = read_ini_file(config_filename, servername, "sprint_bot_counter")
    if exists == -1:
        return -20
    exists, SPRINT_BOT_AUTOTRIGGER = read_ini_file(config_filename, servername, "sprint_bot_autotrigger")
    if exists == -1:
        return -21

    STARBOARD_OUTPUT_CHANNEL_ID = int(STARBOARD_OUTPUT_CHANNEL_ID)
    STARBOARD_REACTION_THRESHOLD = int(STARBOARD_REACTION_THRESHOLD)
    SPELLING_BEE_OUTPUT_CHANNEL_ID = int(SPELLING_BEE_OUTPUT_CHANNEL_ID)
    
    return 0

# ------------------------------------------------------------------------------------ INITIALIZATIONS #
# ==================================================================================================== #



# ==================================================================================================== #
# LOCAL FUNCTIONS ------------------------------------------------------------------------------------ #

# read_ini_file  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Read an INI configuration file
# INPUTS:
#       - (string) filename: the INI file to be read
#       - (string) section: the section to search for
#       - (string) key: the key to search for within the previously specified section
# RETURNS:
#       - (bool) exists: 0 if yes, -1 if no
#       - (string) value: the value stored at a specific section and key in an INI file
def read_ini_file(filename, section, key):
    config = configparser.ConfigParser()
    config.read(filename)
    if config[section][key]:
        return 0, config[section][key]
    else:
        return -1, -1

# time_processor - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes the user-given time value and converts it into integers that datetime can process
# INPUTS:
#       - (string) input_time: the time (formatted HH:MM:SS) in UTC
# OUTPUTS:
#       - (bool) status: returns 0 if no problem, -1 if problem
#       - (int) hour: the hour
#       - (int) minute: the minute
#       - (int) second: the second
def time_processor(input_time):
    values = str(input_time).split(":")
    status = 0
    if len(values) != 3:
        status = -1
    hour = int(values[0])
    minute = int(values[1])
    second = int(values[2])
    return status, hour, minute, second

# check_hotword  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Checks to see if a hotword is already included in the hotwords csv file
# INPUTS:
#       - (string) filename: the hotwords.csv filename
#       - (string) hotword: the hotword to search for
# RETURNS: 
#       - (bool) hotword_already_exists: returns "1" if the hotword is found.
def check_hotword(filename, hotword):
    hotword_already_exists = 0
    
    # Open the CSV file and prep it for Python parsing
    with open(filename, "r") as loaded_file:
        loaded_read = csv.reader(loaded_file, delimiter = "🍔")

        # Search for the hotword in each row
        for row in loaded_read:
            if hotword == row[0]:
                hotword_already_exists = 1
                
    return hotword_already_exists

# add_hotword  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Adds a hotword to the hotwords csv file
# INPUTS:
#       - (string) hotwords_filename: the location of the hotwords csv file
#       - (string) hotword: the trigger word to be added
#       - (string) response: the response from the bot
#       - (bool) message_sender: should the sender be @'ed? "Yes" or "No"
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
def add_hotword(hotwords_filename, hotword, response, message_sender):
    status = 0
    output_message = ""
    output_message_to_CSV = ""

    # Make sure the hotword isn't already used in the file name before continuing
    if check_hotword(hotwords_filename, hotword) == 0:
        # Open file
        with open(hotwords_filename, "a") as loaded_file:
            # Prep the CSV file for Python parsing
            loaded_write = csv.writer(loaded_file, delimiter = "🍔")

            # Build output string to be appended to the file
            if message_sender == 1:
                output_message = "Success! Trigger phrase `%s` will be responded to with the phrase `%s` and will message the sender." % (hotword, response)
                output_message_to_CSV = "%s🍔%s🍔%s\n" % (hotword, response, "Yes")
            else:
                output_message = "Success! Trigger phrase `%s` will be responded to with the phrase `%s`." % (hotword, response)
                output_message_to_CSV = "%s🍔%s🍔%s\n" % (hotword, response, "No")

            loaded_file.write(output_message_to_CSV)
    else:
        output_message = "This trigger phrase is already used. To use this trigger phrase, you can delete it with `!eb hotword delete %s` and re-add it." % (hotword)
    
    return status, output_message

# remove_hotword - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Removes a hotword from the hotwords CSV file
# INPUTS:
#       - (string) hotwords_filename: the location of the hotwords csv file
#       - (string) hotword: the trigger word to be deleted
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
def remove_hotword(hotwords_filename, hotword):
    status = 0
    output_message = ""

    # Check that the hotword even exists in the first place
    if check_hotword(hotwords_filename, hotword) == 1:
        # Generate a temporary array to store CSV data in
        temp_file = list()
        
        # Read through output file
        with open(hotwords_filename, "r") as loaded_file:
            reader = csv.reader(loaded_file, delimiter = "🍔")

            # Print to temp file while also checking for hotword to be deleted
            for row in reader:
                temp_file.append(row)
                for current_item in row:
                    if current_item == hotword:
                        # If the hotword is found, remove it from the temp file
                        temp_file.remove(row)
        
        # Print the temp file back out to the CSV file
        with open(hotwords_filename, "w") as loaded_file:
            writer = csv.writer(loaded_file, delimiter = "🍔")
            writer.writerows(temp_file)
        
        output_message = "The trigger phrase `%s` was deleted from record." % (hotword)
    
    else:
        output_message = "This trigger phrase was not found."
    
    return status, output_message

# load_external_media_config - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Opens the external media config file and searches for a given command
# INPUTS:
#       - (string) filename: the filepath to the external media configuration csv file
#       - (string) command: the command to search for within the configuration file
# RETURNS: 
#       - (bool) is_found: returns a 0 if the command was found, -1 if not
#       - (string) location_type: the type of media stored within the address at this command
#       - (string) address: the link to the media, either a URL or a local address
def load_external_media_config(filename, command):
    # This flag is triggered if the given command is found within the configuration file
    post_already_exists_flag = 0

    with open(filename, "r") as loaded_file:
        # Prep the CSV file for Python parsing
        loaded_read = csv.reader(loaded_file, delimiter = "🍔")

        # Check every value in the first column for the message ID (format of CSV file is: message_id, response_id)
        for row in loaded_file:
            if command == int(row[0]):
                # If the post already exists, flag its location, location_type, and address
                post_already_exists_flag = 1
                location_type = row[1]
                address = row[2]
                break

    # Pass response back to the main function (-1 if failure, 0 if successful)    
    if post_already_exists_flag < 1:
        return -1, -1, -1
    elif post_already_exists_flag == 1:
        return 0, location_type, address

# add_to_external_media_config - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Adds a new source to the external media configuration file.
# INPUTS:
#       - (string) filename: the location of the external media config file
#       - (string) input_string: the raw data received from the user input
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
def add_to_external_media_config(filename, input_string):
    status = 0
    output_message = ""

    # Perform input sanitization on input_string
    # Split command into parts for individual processing
    sorted_array = input_string.split()
        # sorted_array[0] = bot trigger (default: !eb)
        # sorted_array[1] = add
        # sorted_array[2] = command
        # sorted_array[3] = location_type
        # sorted_array[4] = location_link

    # Validate that the link being added isn't already included in the list
    is_found, location_type, address = load_external_media_config(filename, sorted_array[2])
    if is_found == -1:
        with open(filename, "a") as loaded_file:
            # Prep the CSV file for Python parsing
            loaded_write = csv.writer(loaded_file, delimiter = "🍔")

            # Build output string to be appended to the file
            output_message = "%s,%s,%s\n" % (sorted_array[2], sorted_array[3], sorted_array[4])
            loaded_file.write(output_message)
            output_message = "Success! Command `%s` of type `%s` located at `%s` now available for randomizing." % (sorted_array[2], sorted_array[3], sorted_array[4])
    else:
        output_message = "A file with this command already exists."

    return status, output_message

# make_pairs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Makes Markhov Chain pairs
# INPUTS:
#       - (string) corpus: a word in a string
# RETURNS:
#       - (string) corpus[i]/corpus[i+1]: the words in the same neighborhood as the selected word
def make_pairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])

# validate_filepath  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Validates that a file exists at the location provided and corrects the extension (if necessary)
# INPUTS:
#       - (string) filepath: the filepath to process
#       - (string) validation_string: the string to append to the end of the filepath if it is missing
# RETURNS:
#       - (string) filepath: filepath with corrected extension (if necessary)
def validate_filepath(filepath, validation_string):
    # Check if file exists
    if not exists(filepath):
        test = 123 # IN PROGRESS

    if (filepath.find('.txt') == -1):
        # Does not contain .txt in filepath
        filepath = filepath + validation_string
    return filepath   

# sanitize_file  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Removes blank spaces from file before counting
# INPUTS:
#       - (string) initial_filename: the location of the unprocessed file
#       - (string) processed_filename: the location of the processed file
# RETURNS:
#       - N/A
def sanitize_file(initial_filename, processed_filename):
    # Open output file
    output_file = open(processed_filename, "w")
    # Open input file and begin processing
    with open(initial_filename, "r") as input_file:
        for line in input_file:
            if not line.isspace():
                output_file.write(line)

# check_attachment_contents  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Checks message's attachment contents and determines whether the attachment is embeddable/NSFW
# INPUTS:
#       - (DISCORD CLASS) message: the message and its metadata
# RETURNS:
#       - (string) image: the URL to the image that is to be embedded
#       - (int) attachment_exists: a boolean that returns whether there is an embeddable attachment included in the starred message
def check_attachment_contents(message):
    image = None
    attachment = None
    attachment_exists = 0

    if len(message.attachments) > 0:

        # Find the first attachment in the list with a compatible file extension
        for search in message.attachments:
            if search.FILENAME.find(".jpg") or search.FILENAME.find(".jpeg") or search.FILENAME.find(".png") or search.FILENAME.find(".webp") or search.FILENAME.find(".gif"):
                attachment = search
                attachment_exists = 1
                break
        
        # Check to see if the message was sent in a NSFW channel; if so, spoiler the image/embed [[URRENTLY NOT WORKING DUE TO DISCORD LIMITATIONS]]
        # if message.channel.is_nsfw():
            # image = "|| %s ||" % (attachment.url)
        # else:
        if attachment_exists:
            image = attachment.url

    else: 
        if "https://images-ext-1.discordapp.net" in message.content or "https://tenor.com/view/" in message.content:
            # Extract only the URL from the message
            urls = re.findall(URL_REGEX, message.content)
            attachment_exists = 1

            # Finds the first Tenor/Discord URL in the message and selects it (only one message can be embedded due to Discord limitation)
            for search in urls:
                if search.find("discordapp.net") or search.find("https://tenor.com/view/"):
                    # Check to see if the message was sent in a NSFW channel; if so, spoiler the image/embed [[CURRENTLY NOT WORKING]]
                    # if message.channel.is_nsfw():
                        # image = "|| %s.gif ||" % (search)
                    # else:
                        image = "%s.gif" % (search) 

    # print(image) # Debug
    return image, attachment_exists

# find_line  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Count number of lines in a TXT file and generates a random line the selection
# INPUTS:
#       - (string) filepath: the location of the file to be processed
# RETURNS:
#       - (string) line: line to be printed
def find_line(filepath):
    # Validate filepath to ensure it has the correct extension
    filepath = validate_filepath(filepath, ".txt")

    # Open file at that filepath
    with open(filepath, "r") as working_text_document:
        # Count the number of lines in the file
        line_count = 0
        for i in working_text_document:
            line_count += 1

    # Loop through randomly selected lines within the bounds of the total line count until a non-empty line is selected
    line_is_not_empty = 1
    
    with open(filepath, "r") as working_text_document:
        while line_is_not_empty:
            #   Generate random number between 1 and that number
            selected_line_number = random.randint(1, line_count)
            count = 0

            # Make sure the line at that number is not empty (legacy code)
            for line in working_text_document:
                 count += 1
                 if(count == selected_line_number):
                    if line != "\n":
                        selected_line = line
                        line_is_not_empty = 0
                    else:
                        continue

    return selected_line

# retrieve_website_html  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Retrieves the HTML from a web page and prints it to a string.
# INPUTS: 
#       - (string) url: the webpage from which to retrieve the HTML
# OUTPUTS:
#       - (string) output: the output string of HTML
def retrieve_website_html(url):
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

    html_interim = session.get(url).content
    html = str(html_interim)
    
    return html

# process_ao3_html - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes the raw HTML text stream from an AO3 webpage and removes the unnecessary material, leaving nothing but the site content behind.
# INPUTS:
#       - (string) url: the link to the AO3 webpage to be processed
# OUTPUTS:
#       - (string array) chapter_content: the full chapter-by-chapter content of the webpage (note that chapter_content[0] is empty)
def process_ao3_html(url):
    # Make sure that the link provided includes the WHOLE text of the work
    if url.find("?view_adult=true&view_full_work=true") == -1:
        if url.find("?") != -1:
            formatted_url = url.split("?")
            url = formatted_url[0] + "?view_adult=true&view_full_work=true"
        else:
            url = url + "?view_adult=true&view_full_work=true"

    # Retrieve HTML from webpage
    html = retrieve_website_html(url)

    if html.find("<dd class=\"chapters\">1/1</dd>") == -1:
        # Begin trimming out the fat (the chosen delimiter happens to also split the work up into chapters, so that's neat)
        # NOTE: chapter_list[0] is all useless garbage
        chapter_list = html.split("<h3 class=\"landmark heading\" id=\"work\">Chapter Text</h3>\\n    <p>")

        chapter_content_interim = [None] * len(chapter_list)
        chapter_content = [None] * len(chapter_list)
        for i in range(len(chapter_list)):
            # Ignore chapter_list[0]
            if i == 0:
                continue
            chapter_content_interim[i] = chapter_list[i].split("<!--/main-->")
            chapter_content[i] = chapter_content_interim[i][0]
            chapter_content = remove_html_artifacts(chapter_content, i)
    else:
        chapter_list = html.split("<h3 class=\"landmark heading\" id=\"work\">Work Text:</h3>\\n          <div class=\"userstuff\"><p>")
        chapter_content = chapter_list[1].split("<!-- end cache -->")
        i = 0
        chapter_content = remove_html_artifacts(chapter_content, 0)

    return chapter_content

# change_configuration - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Changes a line in the configuration document.
# INPUTS:
#       - (string) config_category: the name of the key whose value is to be changed
#       - (string) new_value: the name of the value to print to config_category
# RETURNS:
#       - (int) status: the error status of the function. 0 if okay, less than 0 if not
#       - (string) output_message: the string to be printed to Discord to confirm success or failure
def change_configuration(config_category, new_value):
    # Initialize configparser
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    status = 0
    output_message = ""
    config_category_flag = 0

    for (key, val) in config.items(GUILD_ID):
        if key == config_category:
            config_category_flag = 1
            config.set(GUILD_ID, key, new_value)

            with open(CONFIG_FILENAME, 'w') as configfile:
                config.write(configfile)
            
            break

    if config_category_flag == 1:
        output_message = "Success! Configuration key `%s` has been updated with value `%s`." % (config_category, new_value)
    else:
        output_message = "ERROR - configuration key `%s` was not found. Please try again, or type `!eb config list` for a list of all configuration keys and values." % (config_category)

    return status, output_message
           
# remove_html_artifacts  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Removes all random artifacts from an HTML webpage string.
# INPUTS:
#       - (string array) chapter_content: the array of content from the HTML file, separated into separate chapters
#       - (int) i: the index used to select the chapter to process from the content array
# RETURNS:
#       - (string array) chapter_content: the post-processed chapter_content array
def remove_html_artifacts(chapter_content, i):
    chapter_content[i] = chapter_content[i].replace("\n", "")
    chapter_content[i] = chapter_content[i].replace(" </em>", "* ")
    chapter_content[i] = chapter_content[i].replace("<em> ", " *")
    chapter_content[i] = chapter_content[i].replace("<em>", "*")
    chapter_content[i] = chapter_content[i].replace("</em>", "*")
    chapter_content[i] = chapter_content[i].replace("<p>\\xc2\\xa0</p>", "")
    chapter_content[i] = chapter_content[i].replace("\\xe2\\x80\\x94", "—")
    chapter_content[i] = chapter_content[i].replace("\\xc2\\xa0</p><p>", "")
    chapter_content[i] = chapter_content[i].replace("\\xe2\\x80\\xa6", "...")
    chapter_content[i] = chapter_content[i].replace("\\", "")
    chapter_content[i] = chapter_content[i].replace("n\'t", "n't")
    chapter_content[i] = chapter_content[i].replace("<hr/>", "")
    chapter_content[i] = chapter_content[i].replace("<strong>", "")
    chapter_content[i] = chapter_content[i].replace("</strong>", "")
    chapter_content[i] = chapter_content[i].replace("</p>n<p>", "</p><p>")
    chapter_content[i] = chapter_content[i].replace("xe2x80x99", "'")
    chapter_content[i] = chapter_content[i].replace("xe2x80x9c", "\"")
    chapter_content[i] = chapter_content[i].replace("xe2x80x9d", "\"")
    chapter_content[i] = chapter_content[i].replace("</p>nn", "</p>")
    chapter_content[i] = chapter_content[i].replace("</p>n", "</p>")
    chapter_content[i] = chapter_content[i].replace("nn</p>", "</p>")
    chapter_content[i] = chapter_content[i].replace("n</p>", "</p>")
    chapter_content[i] = chapter_content[i].replace("'n  ", "")
    chapter_content[i] = chapter_content[i].replace("</p>  </div>n  '", "")
    chapter_content[i] = chapter_content[i].replace("xc2xa0", " ")
    chapter_content[i] = chapter_content[i].replace("n  <span>", "")
    chapter_content[i] = chapter_content[i].replace("</span>", "")
    chapter_content[i] = chapter_content[i].replace("n  <span>", "")
    chapter_content[i] = chapter_content[i].replace("*n    <span>", "*")
    chapter_content[i] = chapter_content[i].replace("n  *", "*")
    chapter_content[i] = chapter_content[i].replace("</p></div>n        ", "")
    chapter_content[i] = chapter_content[i].replace(" align=\"CENTER\"", "")
    chapter_content[i] = chapter_content[i].replace(" align=\"LEFT\"", "")
    chapter_content[i] = chapter_content[i].replace(" align=\"RIGHT\"", "")
    chapter_content[i] = chapter_content[i].replace("</p>  </div>", "")
    chapter_content[i] = chapter_content[i].replace("</br> ", "</p><p>") 

    return chapter_content



# sprint_bot_word_count_processor  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Retrieves usernames and word counts for each sprint and adds them to the tabulator.
# INPUTS:
#       - (string) message_contents: the contents of the message
#       - (string) sprint_bot_counter_filename: the location of the CSV file where the historical sprint data is stored 
# RETURNS:
#       - N/A
def sprint_bot_word_count_processor(message_contents, sprint_bot_counter_filename):
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
        interim2 = interim[1].split(" words**")
        current_sprinter_wc = interim2[0]
        current_sprinter_wc = current_sprinter_wc.replace(",","")

        # Retrieve username from User ID
        username = client.get_user(int(current_sprinter_id))
        split_username = str(username).split("#")
        username = split_username[0]

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
                        previous_wc = row[1]

                        # Combine the new word count with the old one
                        wc = int(previous_wc) + int(current_sprinter_wc)

                        # Print the new combo word count to the CSV
                        out = [current_sprinter_id, str(wc)]
                        # output_string += "@%s: %s words\n" % (username, str(wc))
                        temp_file.append(out)
                
            # If the user is new to the list, add them and their word count as-is
            if found_user != 1:
                out = [current_sprinter_id, current_sprinter_wc]
                # output_string += "@%s: %s words\n" % (username, current_sprinter_wc)
                temp_file.append(out)
        
        # Print the temp file back out to the CSV file
        with open(sprint_bot_counter_filename, "w") as loaded_file:
            writer = csv.writer(loaded_file, delimiter = ",")
            writer.writerows(temp_file)

    return status, output_string

    # 🏆 **CONGRATS EVERYONE**
    # `1.` <@!623595478172434432> — **394 words** (13 wpm)
    # `2.` <@!330900130997862400> — **192 words** (6 wpm)

    # `_sprint` to start another.


    
# ------------------------------------------------------------------------------------ LOCAL FUNCTIONS #
# ==================================================================================================== #



# ==================================================================================================== #
# EMBED FUNCTIONS ------------------------------------------------------------------------------------ #

# build_starboard_message  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Builds starboard message
# INPUTS:
#       - (DISCORD CLASS) payload: the message payload generated by the emoji reaction detection function
#       - (string) output_channel: the channel where the starboard is located
#       - (DISCORD CLASS) message: the discord message and its metadata, separated out of the payload for easier processing
#       - (int) count: the number of emoji reactions on the post
# RETURNS:
#       - (int) response_id: the message ID of the bot's response
async def build_starboard_message(payload, output_channel, message, count):
    # Check if there's any attachment in the file; if so, process it accordingly
    image, attachment_exists = check_attachment_contents(message)

    # Build embed
    embed = discord.Embed(title = "", description = message.content, timestamp = datetime.datetime.utcnow())
    embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
    build_post_url = "[Jump!](https://discord.com/channels/%s/%s/%s)" % (payload.guild_id, payload.channel_id, payload.message_id)
    embed.add_field(name = "Source", value = build_post_url)

    # If an attachment exists, include it in the embed build
    if attachment_exists and image:
        embed.set_image(url=image)
    embed.set_footer(text = payload.message_id)

    # Build channel structure for current post that's about to be created
    channel = client.get_channel(output_channel)

    # Find the channel the original reacted message was posted in so it can be referenced in the bot post 
    original_channel = client.get_channel(payload.channel_id)

    build_content = "%s **%d** %s" % (STARBOARD_EMOJI_DELIMITER, count, original_channel.mention)
    sent_message = await channel.send(content = build_content, embed=embed)

    return sent_message

# edit_starboard_message - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Edits starboard message to update reaction count
# INPUTS:
#       - (DISCORD CLASS) payload: the message payload generated by the emoji reaction detection function
#       - (string) output_channel: the channel where the starboard is located
#       - (DISCORD CLASS) message: the discord message and its metadata, separated out of the payload for easier processing
#       - (int) count: the number of emoji reactions on the post
#       - (int) response_id: the Discord message identifier metadata used to locate it within a server
# RETURNS:
#       - N/A
async def edit_starboard_message(payload, output_channel, message, count, response_id):
    # Check if there's any attachment in the file; if so, process it accordingly
    image, attachment_exists = check_attachment_contents(message)

    # Build embed
    embed = discord.Embed(title = "", description = message.content, timestamp = datetime.datetime.utcnow())
    embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
    build_post_url = "[Jump!](https://discord.com/channels/%s/%s/%s)" % (payload.guild_id, payload.channel_id, payload.message_id)
    embed.add_field(name = "Source", value = build_post_url)

    # If an attachment exists, include it in the embed build
    if attachment_exists and image:
        embed.set_image(url=image)
    embed.set_footer(text = payload.message_id)

    # Build channel structure for current post that's about to be edited
    channel = client.get_channel(output_channel)

    # Build message structure for the original message that was posted in the channel mentioned above
    sent_message = await channel.fetch_message(response_id)

    # Find the channel the original reacted message was posted in so it can be referenced in the bot post 
    original_channel = client.get_channel(payload.channel_id)

    build_content = "%s **%d** %s" % (STARBOARD_EMOJI_DELIMITER, count, original_channel.mention)
    await sent_message.edit(content = build_content, embed = embed)

# list_hotwords  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Lists all currently established trigger phrases that the bot is listening for.
# INPUTS:
#       - (string) hotwords_filename: the location of the hotwords csv file
#       - (DISCORD CLASS) message: the message that triggered this function and its metadata (used for printing to the right channel)
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
async def list_hotwords(hotwords_filename, message):
    status = 0
    output_message = ""
    embed_body = ""

    # Build up embed
    embed = discord.Embed(title = "EndoBot Trigger Phrases", description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)

    with open(hotwords_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = "🍔")

        # Build embed field - appends new fields to the end of the previous one to (theoretically) mean that an unlimited number of trigger phrases can be displayed 
        for row in reader:
            embed_body = "**Bot Response:** \"%s\"\n**Reply to Sender?** %s\n\n" % (row[1], row[2])
            embed.add_field(name = row[0], value = embed_body, inline = False)

    channel = message.channel
    await channel.send(embed = embed)

    return status, output_message

# bot_help - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Prints the bot's current functionality in the form of a few embed posts to the server.
# INPUTS:
#       - (DISCORD CLASS) message: the message class given by discord
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
async def bot_help(message):

    embed1 = discord.Embed(title = "EndoBot Help (Page 1)", description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)
    embed1.set_image(url = "https://i.gifer.com/7Bi.gif")
    embed1.add_field(name = "\u200b",
                     value = "```cs\n# TRIGGER PHRASES #```\nThese are words or phrases that EndoBot actively searches for and responds to with a pre-configured message.\n\n`!eb trigger add [trigger phrase] [bot response] [Message the sender? Yes/No]`\nThis command adds a trigger phrase and a bot response to the masterlist. The brackets are required!\n\n`!eb trigger delete [trigger phrase]`\nThis command removes a trigger phrase and its bot response from the masterlist.\n\n`!eb trigger list`\nThis command lists all trigger phrases and their subsequent bot responses at once.",
                     inline = False) 

    embed2 = discord.Embed(title = "EndoBot Help (Page 2)", color=0x0077ff)
    embed2.set_image(url = "https://c.tenor.com/zFE5t_rOWwYAAAAC/mononoke-yakuru.gif")
    embed2.add_field(name = "\u200b",
                     value = "```cs\n# RANDOMIZER #```\nThese are commands that allow a user to display a random line or selection from a selected text. Currently supported file formats: N/A\nFuture supported file formats: .epub, .mobi, AO3.org fanfiction, FFN.net fanfiction\n\n`!eb randomizer add [media name] [link]`\nThis command adds a document or a file to bot memory under a shorthand name, `[media name]`, that can be called upon.\n\n`!eb randomizer delete [media name]`\nThis command removes a saved file from bot memory.\n\n`!eb randomizer list`\nThis command lists all files currently loaded into memory and their associated links/filenames.\n\n`!eb randomizer [media name]`\nThis command selects a random line from the file.",
                     inline = False)  

    embed3 = discord.Embed(title = "EndoBot Help (Page 3)", color=0x0077ff)
    embed3.set_image(url = "https://media1.giphy.com/media/SYirgmIRk5hIJCuK7t/giphy.gif")
    embed3.add_field(name = "\u200b",
                     value = "```cs\n# BOT CONFIGURATION #```\nThese commands allow moderators and server owners to change bot configuration settings without having to manually adjust or change any bot files. WARNING: this can permanently damage bot functionality if not handled correctly.\n\n`!eb config list`\nThis command lists all available configuration options and their default/expected values.\n\n`!eb config [configuration option] [value]`\nThis command allows a moderator to change a configuration option. The brackets are required!\n\n`!eb reboot`\nThis restarts EndoBot and loads in any changes to the configuration file that may have been made.",
                     inline = False)

    embed4 = discord.Embed(title = "EndoBot Help (Page 4)", color=0x0077ff)
    embed4.set_image(url = "https://i.gifer.com/ns9.gif")
    embed4.add_field(name = "\u200b",
                     value = "```cs\n# MISCELLANEOUS COMMANDS #```\nCommands for various random bot features.\n\n`!eb leaderboard`\nThis command displays the current top 3 most starred users in a server.\n\n`!eb help`\nThe command used to display this message!",
                     inline = False) 

    channel = message.channel
    
    await channel.send(embed = embed1)
    await channel.send(embed = embed2)
    await channel.send(embed = embed3)
    await channel.send(embed = embed4)

    return 0, None

# leaderboard  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Counts the number of times each user has been starred on the starboard and ranks them greatest-to-least
# INPUTS:
#       - (string) receipts_filename: the location of the receipts CSV file to be processed
#       - (DISCORD CLASS) message: the message that triggered this function and its metadata (used for printing to the right channel)
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
async def leaderboard(receipts_filename, message):

    # Open the receipts file
    with open(receipts_filename, "r") as opened_file:
        opened_csv = csv.reader(opened_file, delimiter = ",")

        # Count number of unique users in the starboard
        unique_users = []
        unique_users_count = 0

        for row in opened_csv:
            if row[0] not in unique_users:
                unique_users_count += 1
                unique_users.append(row[0])

    # Re-open the receipts file to sort back through it again
    with open(receipts_filename, "r") as opened_file:
        opened_csv = csv.reader(opened_file, delimiter = ",")

        # Build an array of the same length as unique_users
        unique_users_stats = [0] * unique_users_count

        # Count number of times each unique user is seen within the starboard
        for row in opened_csv:
            cc = 0
            for user in unique_users:
                if row[0] == user:
                    unique_users_stats[cc] += 1
                cc += 1

        # Sort all users, greatest to least, by zipping the two arrays together and sorting by the second array
        zipped_pair = zip(unique_users, unique_users_stats)
        sorted_pairs = sorted(zipped_pair, key = lambda x: x[1], reverse = True)

        # Unzip the arrays so they can be re-zipped later during the embed buildup
        tuples = zip(*sorted_pairs)
        user_list, user_stats = [ list(tuple) for tuple in tuples]

        # Build up embed
        title_builder = "%s EndoBot Starboard Leaderboard %s" % (STARBOARD_EMOJI_DELIMITER, STARBOARD_EMOJI_DELIMITER)
        embed = discord.Embed(title = title_builder, description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)
        output_message = ""

        # Print out sorted results to embed
        for i, j in zip(user_list, user_stats):
            username = client.get_user(int(i))
            split_username = str(username).split("#")
            output_message_interim = "**@%s**: %d starred posts\n" % (split_username[0], int(j))
            output_message = output_message + output_message_interim

        embed.add_field(name = "\u200b", inline = False, value = output_message)

        # Print to Discord
        channel = message.channel
        await channel.send(embed = embed)

    return 0, None



async def sprint_leaderboard(sprint_counter_filename, message):
    user_id = list()
    word_count = list()

    # Open the sprint count file
    with open(sprint_counter_filename, "r") as opened_file:
        opened_csv = csv.reader(opened_file, delimiter = ",")

        for row in opened_csv:
            user_id.append(row[0])
            word_count.append(row[1])
        
        # Sort all users, greatest to least, by zipping the two arrays together and sorting by the second array
        zipped_pair = zip(user_id, word_count)
        sorted_pairs = sorted(zipped_pair, key = lambda x: x[1], reverse = False)

        # Unzip the arrays so they can be re-zipped later during the embed buildup
        tuples = zip(*sorted_pairs)
        user_list, user_stats = [ list(tuple) for tuple in tuples]

        # Build up embed
        title_builder = "✏️ @Sprinto Cumulative Word Count Totals ✏️"
        embed = discord.Embed(title = title_builder, color=0x0077ff)
        output_message = ""

        # Print out sorted results to embed
        for i, j in zip(user_list, user_stats):
            username = client.get_user(int(i))
            split_username = str(username).split("#")
            output_message_interim = "**@%s**: %d words\n" % (split_username[0], int(j))
            output_message = output_message + output_message_interim

        embed.add_field(name = "\u200b", inline = False, value = output_message)

        # Print to Discord
        channel = message.channel
        await channel.send(embed = embed)

    return 0, None




# spelling_bee_printer - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes the daily NYT Spelling Bee puzzle from the spelling bee website, converts the HTML into an image, and 
# posts the image to a specified Discord channel at a certain time of the day. Please note that this was developed
# for educational purposes only.
# INPUTS:
#       - (string) channel_id: The Discord channel where the image will be printed
# RETURNS:
#       - N/A
async def spelling_bee_printer(channel_id):
    url = SPELLING_BEE_URL

    # Read the day's HTML file
    html = retrieve_website_html(url)

    # Pull the center letter and outer letters from the HTML file by trimming it down with the split() function
    interim_values = html.split("\"centerLetter\":\"")
    interim_values2 = interim_values[1].split("\",\"outerLetters\":[\"")
    interim_values3 = interim_values2[1].split("\"],\"validLetters\":[\"")
    center_letter = interim_values2[0]
    outer_letters = interim_values3[0].split("\",\"")

    # Pull the answers to the day's puzzle from the HTML file as well
    interim_values4 = html.split("\"pangrams\":[\"")
    interim_values5 = interim_values4[1].split("\"],\"answers\":")
    answers = interim_values5[0].split("\",\"")

    # Build a new HTML file with just the spelling bee in it so it can be captured as an image
    with open("spelling_bee.html", "w") as working_html_document:
        output_string = "<!DOCTYPE html><html ><head ><link rel=\"stylesheet\" type=\"text/css\" href=\""
        working_html_document.write(output_string)
        working_html_document.write(SPELLING_BEE_CSS)
        output_string = "\" ><style> @font-face { font-family: 'nyt-franklin'; src: url(\"franklin.ttf\"); } #container { max-width: 261px; max-height: 271.23px; max-block-size: 261px; font-family: 'nyt-franklin';} </style ></head ><body style=\"background:white;\"><div id=\"container\"><svg class=\"hive-cell center\" viewBox=\"0 0 120 103.96152422706631\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\" ></polygon><text class=\"heavy\" x=\"50%\" y=\"50%\" dx=\"-.30em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\">"
        working_html_document.write(output_string)
        working_html_document.write(center_letter.upper())
        output_string = "</text></svg ><svg class=\"hive-cell outer\" viewBox=\"0 0 120 103.92304845413263\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\"></polygon ><text class=\"cell-letter\" x=\"50%\" y=\"50%\" dx=\"-0.25em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\"eb>"
        working_html_document.write(output_string)
        working_html_document.write(outer_letters[0].upper())
        output_string = "</text></svg ><svg class=\"hive-cell outer\" viewBox=\"0 0 120 103.92304845413263\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\"></polygon ><text class=\"cell-letter\" x=\"50%\" y=\"50%\" dx=\"-0.25em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\">"
        working_html_document.write(output_string)
        working_html_document.write(outer_letters[1].upper())
        output_string = "</text></svg ><svg class=\"hive-cell outer\" viewBox=\"0 0 120 103.92304845413263\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\"></polygon ><text class=\"cell-letter\" x=\"50%\" y=\"50%\" dx=\"-0.25em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\">"
        working_html_document.write(output_string)
        working_html_document.write(outer_letters[2].upper())
        output_string = "</text></svg ><svg class=\"hive-cell outer\" viewBox=\"0 0 120 103.92304845413263\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\"></polygon ><text class=\"cell-letter\" x=\"50%\" y=\"50%\" dx=\"-0.25em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\">"
        working_html_document.write(output_string)
        working_html_document.write(outer_letters[3].upper())
        output_string = "</text></svg ><svg class=\"hive-cell outer\" viewBox=\"0 0 120 103.92304845413263\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\"></polygon ><text class=\"cell-letter\" x=\"50%\" y=\"50%\" dx=\"-0.25em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\">"
        working_html_document.write(output_string)
        working_html_document.write(outer_letters[4].upper())
        output_string = "</text></svg ><svg class=\"hive-cell outer\" viewBox=\"0 0 120 103.92304845413263\" ><polygon class=\"cell-fill\" points=\"0,51.96152422706631 30,0 90,0 120,51.96152422706631 90,103.92304845413263 30,103.92304845413263\" stroke=\"white\" stroke-width=\"7.5\"></polygon ><text class=\"cell-letter\" x=\"50%\" y=\"50%\" dx=\"-0.25em\" dy=\"0.35em\" font-family=\"Helvetica\" font-size=\"1.875em\">"
        working_html_document.write(output_string)
        working_html_document.write(outer_letters[5].upper())
        output_string = "</text></svg ></div ></body></html>"
        working_html_document.write(output_string)

    # Convert the generated HTML into a PNG
    hti = Html2Image()
    hti.screenshot(html_file=SPELLING_BEE_HTML, css_file=SPELLING_BEE_CSS, save_as=SPELLING_BEE_PNG, size=(305, 300))

    # Prepare the local file so it can be output via Discord
    file = discord.File(SPELLING_BEE_PNG)

    # Build the embed
    embed = discord.Embed(title = "NYT DAILY SPELLING BEE", color=0x0077ff)
    
    # Build the embed's image and footer strings
    today = datetime.date.today()
    footer_string = "Day of " + today.strftime("%d %B %Y") + "\n" + url
    image_string = "attachment://" + SPELLING_BEE_PNG
    embed.set_image(url = image_string)
    embed.set_footer(text = footer_string)

    # Print the puzzle solutions, regardless of however many there may be
    output_string_interim = ""
    count = 1
    for i in answers:
        output_string_interim = output_string_interim + "(" + str(count) + "): ||" + i + "||\n"
        count += 1
    output_string = "```cs\n# PUZZLE SOLUTIONS #```\n" + output_string_interim

    embed.add_field(name = "\u200b", value = output_string, inline = False)

    channel = client.get_channel(int(channel_id))

    await channel.send(file = file, embed = embed)

# find_ao3_line  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Selects a random line number from an AO3 HTML dump and prints it to Discord.
# INPUTS:
#       - (string array) chapter_content: the entirety of the AO3 webpage, broken up into chapters (skipping index 0 in the list), and processed to remove HTML artifacts
#       - (DISCORD CLASS) message: the metadata of the trigger message, used to respond in the same channel
#       - (string) url: the site URL, used as a backup in event of failed processing
# RETURNS:
#       - N/A
async def find_ao3_line(chapter_content, message, url):
    # Check to see if the AO3 site being processed is a oneshot or chaptered - if chaptered, continue
    if int(len(chapter_content) - 1) > 1:
        # Randomly pick a chapter to pull a line from
        selected_chapter_number = 1000000
        while selected_chapter_number > (len(chapter_content) - 1):
            selected_chapter_number = random.randint(1, len(chapter_content) - 1)

        # Verify that there isn't a problem with chapter_content
        if chapter_content is not None:
            # Process all lines in that chapter
            line_choices = chapter_content[selected_chapter_number - 1].split("</p><p>") 
        # If there is, start over with another line
        else:
            process_ao3_html(url)
    # If a oneshot, continue
    else:
        # Verify that there isn't a problem with chapter_content
        if chapter_content is not None:
            line_choices = chapter_content[0].split("</p><p>")
        # If there is, start over with another line
        else:
            process_ao3_html(url)

    # Randomly select a line from the generated list
    selected_line_number = 1000000
    while selected_line_number > (len(line_choices) - 1):
        selected_line_number = random.randint(0, len(line_choices) - 1)

    # Retrieve the channel name of the location where the command message was sent
    channel = message.channel

    # Post result to Discord
    await channel.send(line_choices[selected_line_number]) 

# list_all_metadata  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Displays all configuration keys and their currently assigned values to the user.
# INPUTS:
#       - (DISCORD CLASS) message: the sender's original message with all of its metadata (used for printing to the same channel)
# RETURNS:
#       - N/A
async def list_configuration(message):
    # Initialize configparser
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    output_message = ""

    # Build up embed
    embed = discord.Embed(title = "EndoBot - Current Configuration", description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)

    for (key, val) in config.items(GUILD_ID):
        output_message = output_message + "%s: `%s`\n" % (key, val)

    embed.add_field(name = "\u200b", inline = False, value = output_message)

    channel = message.channel
    await channel.send(embed = embed)

# ------------------------------------------------------------------------------------ EMBED FUNCTIONS #
# ==================================================================================================== #



# ==================================================================================================== #
# !EB BOT COMMANDS ----------------------------------------------------------------------------------- #

# bot_command_processor  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# A function that specifically processes through !eb prefixed messages and sorts out respondable prompts from the following line items
# INPUTS:
#       - (DISCORD CLASS) message: the raw input message with metadata and preserved capitalcase
#       - (DISCORD CLASS) command_string: the all-lowercase copy of the original message, specifically to make parsing command strings easier
# RETURNS:
#       N/A 
async def bot_command_processor(message, command_string):
    channel = message.channel

    start_0 = 0 
    end_0 = 0 

    status = 0
    response = "There was a problem with your command. Please consult `!eb help` for more information."

    mod = False

    # Check if the user is a moderator/has admin privileges
    if message.author.guild_permissions.administrator:
        mod = True
    else:
        mod = False

    # Keeps the original message string and the formatted (all lowercase) message string intact but separates them out with a delimiter
    command_array = command_string.split()

    number_of_elements = len(command_array)

    if number_of_elements > 1:
        if command_array[1] == "trigger":
            if number_of_elements > 2:
                if command_array[2] == "add":
                    if mod == True:
                        if message.content.count("[") == 3 and message.content.count("]") == 3:
                            # Process message string for bracket notation and filter out inputs
                            new_string = message.content.split("] [")
                            if new_string[0].find(" [") != -1:
                                start_0 = new_string[0].find(" [") + len(" [")
                            else:
                                start_0 = -1
                            end_0 = len(new_string[0])
                            
                            # Make sure there's not a problem with and of the "find"s - aka there was a problem with the input string
                            if start_0 == -1 or end_0 == 0:
                                # Send an error message to the user 
                                status = -1
                            else:
                                # Finish constructing command list
                                command = new_string[0][start_0:end_0]

                                bot_response = new_string[1]

                                # Check to see if the author should be tagged or not and convert the response from a string to a boolean   
                                tag_author = 0
                                if new_string[2].find("Yes") or new_string[2].find("yes"): 
                                    tag_author = 1

                                # If all information is properly constructed, add the hotword
                                status, response = add_hotword(HOTWORDS_FILENAME, command, bot_response, tag_author)
                                await channel.send(response)
                        else:
                            status = -1
                    else:
                        status = -1
                        response = "Sorry, you lack the necessary permissions to use this command."
                elif command_array[2] == "delete":
                    if mod == True:
                        if message.content.find("["):
                            # Process message string for bracket notation and filter out inputs
                            new_string_partiallyprocessed = message.content.split(" [")
                            new_string = new_string_partiallyprocessed[1].split("]") # new_string[0] is the phrase to be deleted

                            status, response = remove_hotword(HOTWORDS_FILENAME, new_string[0])
                            await channel.send(response)
                    else:
                        status = -1
                        response = "Sorry, you lack the necessary permissions to use this command."
                elif command_array[2] == "list":
                    status, response = await list_hotwords(HOTWORDS_FILENAME, message)
        elif command_array[1] == "leaderboard":
            status, response = await leaderboard(RECEIPTS_FILENAME, message)
        elif command_array[1] == "sprintstats":
            status, response = await sprint_leaderboard(SPRINT_BOT_COUNTER, message)
        elif command_array[1] == "help":
            status, response = await bot_help(message)
        elif command_array[1] == "randomizer":
            if number_of_elements > 2:
                status = 0
                chapter_content = process_ao3_html(command_array[2])
                await find_ao3_line(chapter_content, message, command_array[2])
            else:
                status = -1
                response = "You're missing a URL!"
        elif command_array[1] == "spellingbee":
            await spelling_bee_printer(int(message.channel.id))
        elif command_array[1] == "reveal":
            if mod == True:
                output_string = "**[[DEBUG]]**\n------> Message metadeta: %s\n\n------> Current channel: %s" % (message, message.channel.id)
                await message.channel.send(output_string)
            else:
                status = -1
                response = "Sorry, you lack the necessary permissions to use this command."
        elif command_array[1] == "debug":
            ## PLACE COMMANDS UNDER DEVELOPMENT HERE ##
            test = 123

        elif command_array[1] == "reboot":
            if mod == True:
                await channel.send("Rebooting EndoBot....")
                await on_ready()
                await channel.send("EndoBot rebooted!")
            else:
                status = -1
                response = "Sorry, you lack the necessary permissions to use this command."
        elif command_array[1] == "config":
            if mod == True:
                if number_of_elements > 2:
                    # Check to see if user wants to list all metadata
                    if command_array[2] == "list":
                        await list_configuration(message)

                    # Otherwise, check to see if the user is trying to change a metadata
                    else:
                        if number_of_elements > 3:
                            if message.content.count("[") == 2 and message.content.count("]") == 2:
                                # Process message string for bracket notation and filter out inputs
                                new_string = message.content.split("] [")
                                if new_string[0].find(" [") != -1:
                                    start_0 = new_string[0].find(" [") + len(" [")
                                else:
                                    start_0 = -1
                                end_0 = len(new_string[0])
                                
                                # Make sure there's not a problem with and of the "find"s - aka there was a problem with the input string
                                if start_0 == -1 or end_0 == 0:
                                    # Send an error message to the user 
                                    status = -1
                                else:
                                    # Finish constructing command list
                                    config_category = new_string[0][start_0:end_0]
                                    new_value = new_string[1].replace("]","")

                                    status, response = change_configuration(config_category, new_value)
                                    await channel.send(response)
                            else:
                                status = -1
                        else:
                            status = -1

            else:
                status = -1
                response = "Sorry, you lack the necessary permissions to use this command."
        else:
            status = -1
    else:
        status = -1

    if status == -1:
        await channel.send(response)

# ----------------------------------------------------------------------------------- !EB BOT COMMANDS #
# ==================================================================================================== #



# ==================================================================================================== #
# ACTIVE DISCORD ASYNC FUNCTIONS --------------------------------------------------------------------- #

# Startup  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_ready():
    # Initialize ini reader
    config = configparser.ConfigParser()

    # Load in configuration file
    configuration_file = config.read(CONFIG_FILENAME)
    if not configuration_file:
        print("INITIALIZATION ERROR: %s file not found." % (CONFIG_FILENAME))
        quit()
    else:
        # Initialize the bot and bot variables
        error = initialize_bot(CONFIG_FILENAME, GUILD_ID)
        if error != 0:
            print("INITIALIZATION ERROR: loading of %s exited with Error Code %d." % (CONFIG_FILENAME, error))
            quit()

        # Begin scheduler timer
        client.loop.create_task(background_task())

        # Print message stating that the bot has connected to Discord
        print(f'{client.user.name} has connected to Discord!')

# Message Detection Wrapper  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_message(message):
    # Print debug line to console
    print(f'Message detected: @{message.author} in #{message.channel}: {message.content}')

    # Convert message to all lower-case for easier sorting (if set to do so in configuration file)
    if(RESPONSE_FLAG_CASE_SENSITIVE == "No"):
        formatted_message = message.content.lower()
    else:
        formatted_message = message.content
    
    # Ignore all bot messages
    if not message.author.bot:
        # Search for response flags
        if formatted_message.startswith("!eb"):
            await bot_command_processor(message, formatted_message)

        # Check for response flag contents if they are the entirety of the text - if so, do not @ the poster
        elif formatted_message == RESPONSE_FLAG.lower() and RESPONSE_FLAG_CASE_SENSITIVE != "Yes":
            # parse_gdoc()

            # sanitize_file(initial_filename, filename)

            line = find_line(FILENAME)
            await message.channel.send(line)

        elif formatted_message == RESPONSE_FLAG and RESPONSE_FLAG_CASE_SENSITIVE == "Yes":
            line = find_line(FILENAME)
            await message.channel.send(line)

        # Check for response flag contents if they are anywhere within the content of the text - if so, @ the poster
        elif formatted_message.find(RESPONSE_FLAG.lower()) != -1 and RESPONSE_FLAG_MATCH_EXACT_CASE != "Yes":
            # Assign spoken username to variable
            user = message.author

            line = find_line(FILENAME)
            await message.channel.send('{0.author.mention} '.format(message) + line)
        
        # Generate a machine learning response based on the starboard file
        elif formatted_message == MACHINE_LEARNING_RESPONSE_FLAG:
            machine_learning = open(FILENAME, encoding='utf8').read()
            machine_learning_wordsplit = machine_learning.split()

            pairs = make_pairs(machine_learning_wordsplit)

            word_dict = {}

            for word_1, word_2 in pairs:
                if word_1 in word_dict.keys():
                    word_dict[word_1].append(word_2)
                else:
                    word_dict[word_1] = [word_2]
                    
            first_word = np.random.choice(machine_learning_wordsplit)
            chain = [first_word]
            n_words = random.randint(30,50)

            for i in range(n_words):
                chain.append(np.random.choice(word_dict[chain[-1]]))

            await message.channel.send(' '.join(chain))
        
        else:
            with open(HOTWORDS_FILENAME, "r") as hotwords_file:
                # Read in hotwords_file CSV
                hotwords_read = csv.reader(hotwords_file, delimiter = '🍔')

                # Check each row in the CSV for the trigger word (in any format)
                for row_split in hotwords_read:
                    # row_split = row[0].split("🍔")
                    if formatted_message.find(row_split[0]) != -1:
                        # If the word is found, check to see if the bot should @ the user or not
                        if row_split[2] == "Yes" or row_split[2] == "yes":
                            await message.channel.send('{0.author.mention} '.format(message) + row_split[1])
                        else:
                            await message.channel.send(row_split[1])
                        
                        break

    # Check to see if @Sprinto was the tweeter          
    if message.author.id == int("421646775749967872"):
        # Check message to see if it is an end-of-sprint message
        if message.content.find("🏆 **CONGRATS EVERYONE**") != -1:
            # Process sprint values and add to total counter
            status, response = sprint_bot_word_count_processor(message.content, SPRINT_BOT_COUNTER)
            # If there were no problems, also print out the current leaderboard
            if status == 0 and (SPRINT_BOT_AUTOTRIGGER == "Yes" or SPRINT_BOT_AUTOTRIGGER == "yes"):
                await sprint_leaderboard(SPRINT_BOT_COUNTER, message)
        



# Starboard Emoji Reaction Parser  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_raw_reaction_add(payload):
    # if payload.channel_id == [[some channel id]]:
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = get(message.reactions, emoji = payload.emoji.name)

    output_channel = STARBOARD_OUTPUT_CHANNEL_ID 

    if payload.emoji.name == STARBOARD_EMOJI_DELIMITER:
        count = reaction.count
        if count > (int(STARBOARD_REACTION_THRESHOLD) - 1):

            # Verify that a receipts file exists; if one doesn't, create it
            if not exists(RECEIPTS_FILENAME):
                with open(RECEIPTS_FILENAME, "w") as receipts_file:
                    receipts_write = csv.writer(receipts_file)

            # Check the receipts file to see if there's already an auto-generated response message created for that reacted discord message
            post_already_exists_flag = 0

            with open(RECEIPTS_FILENAME, "r") as receipts_file:
                # Process receipts file using the CSV library
                receipts_read = csv.reader(receipts_file)

                # Check every value in the first column for the message ID (format of CSV file is: message_id, response_id)
                for row in receipts_read:
                    if payload.message_id == int(row[1]):
                        post_already_exists_flag = 1
                        response_id = row[2]
                        break

            # If the post already exists, then edit the message rather than create a new one
            if post_already_exists_flag == 1:
                await edit_starboard_message(payload, output_channel, message, count, response_id)
            else:
                response_id = await build_starboard_message(payload, output_channel, message, count)

                # Export the message_id and the response_id to receipts.csv
                with open(RECEIPTS_FILENAME, "a") as receipts_file:
                    receipts_write = csv.writer(receipts_file)
                    receipts_write.writerow([message.author.id, payload.message_id, response_id.id])
                
                # Put the sin in the sin bin (if there's actually content in the message)
                if message.content:
                    with open(FILENAME, "a") as sinbin:
                        output_message = "%s\n" % (message.content)
                        sinbin.write(output_message)

# Post Scheduler - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@tasks.loop(hours=24)
async def called_once_a_day():
    await client.wait_until_ready()
    await spelling_bee_printer(SPELLING_BEE_OUTPUT_CHANNEL_ID)

async def background_task():
    # Build up the daily message time value from numbers acquired in the configuration.ini file
    sb_status, sb_hour, sb_minute, sb_second = time_processor(SPELLING_BEE_POST_TIME)
    if sb_status == 0:
        DAILY_MESSAGE_TIME = datetime.time(sb_hour, sb_minute, sb_second)      

    # Run in a continuous loop
    while True:
        # Obtain the current time
        now = datetime.datetime.utcnow()

        # Calculate how long it will be until the next trigger time
        target_time = datetime.datetime.combine(now.date(), DAILY_MESSAGE_TIME)
        seconds_until_target = (target_time - now).total_seconds()

        # If the trigger time is the next calendar day, add in a full day of seconds to the timer
        if seconds_until_target <= 0:
            seconds_until_target = 86400 + seconds_until_target

        print("SCHEDULER FUNCTION: the current time is %s. The scheduled time is %s, which is in appx. %s seconds." % (now, DAILY_MESSAGE_TIME, str(seconds_until_target)))

        # Tell the bot to wait that many seconds
        await asyncio.sleep(seconds_until_target)

        # Once waited, execute the daily scheduled function - with an added check to make sure that it's not an accidental misfire
        now_validate = datetime.datetime.utcnow()
        target_time_validate = datetime.datetime.combine(now_validate.date(), DAILY_MESSAGE_TIME)
        seconds_until_target_validate = (target_time_validate - now_validate).total_seconds()
        if abs(seconds_until_target_validate - seconds_until_target) < 100:
            await called_once_a_day()

        # A ten-second delay after execution to give the scheduled function enough time to parse through large HTML files
        await asyncio.sleep(10)

# INIT - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
if __name__ == "__main__":
    client.run(TOKEN)

# --------------------------------------------------------------------- ACTIVE DISCORD ASYNC FUNCTIONS #
# ==================================================================================================== #
