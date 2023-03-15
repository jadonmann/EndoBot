########################################################################################################
# ENDOBOT ============================================================================================ #
#
# Built using the Discord.py Python API
# Written by JA Mann
# 
# ============================================================================================ ENDOBOT #
########################################################################################################




# ==================================================================================================== #
# IMPORTS AND GLOBAL VARIABLES ----------------------------------------------------------------------- #

from __future__ import print_function
from cgi import test
from xmlrpc.server import CGIXMLRPCRequestHandler
#from asyncio.windows_events import NULL
from async_timeout import asyncio
from cv2 import estimateChessboardSharpness, line
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
import shutil
import os
import threading

import requests
import configparser
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # pip install webdriver-manager

import nanowrimo
import dataprocessing
import wordsprints

# Enables ability to check member IDs within a server (used for Leaderboard functionality)
# This requires a specific permission through Discord's API and will need to be renewed periodically
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

TOKEN = None

# SYSTEM FILEPATHS - DO NOT MODIFY
TOKEN_FILENAME = "token.txt"
CONFIG_FILENAME = "configuration.ini"
DEFAULTS_FOLDER = "Init"
SERVERS_FOLDER = "Servers"

GUILD_ID = list()
SYSTEM_CHANNEL = list()
STARBOARD_FUNCTION_ENABLE = list()
STARBOARD_FILENAME = list()
STARBOARD_RECEIPTS_FILENAME = list()
STARBOARD_OUTPUT_CHANNEL_ID = list()
STARBOARD_REACTION_THRESHOLD = list()
STARBOARD_EMOJI_DELIMITER = list()
RESPONSE_FLAG = list()
RESPONSE_FLAG_CASE_SENSITIVE = list()
RESPONSE_FLAG_MATCH_EXACT_CASE = list()
LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME = list()
HOTWORDS_FILENAME = list()
HOTWORDS_DELIMITER = list()
MACHINE_LEARNING_RESPONSE_FLAG = list()
SPELLING_BEE_URL = list()
SPELLING_BEE_OUTPUT_CHANNEL_ID = list()
SPELLING_BEE_AUTO_POST = list()
SPELLING_BEE_POST_TIME = list()
SPELLING_BEE_HTML = list()
SPELLING_BEE_CSS = list()
SPELLING_BEE_PNG = list()
SPRINT_BOT_COUNTER = list()
SPRINT_BOT_INDIVIDUAL_COUNTER_FOLDER = list()
SPRINT_BOT_AUTOTRIGGER = list()
SPRINT_BOT_SKIP_ZERO_DAYS = list()
SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY = list()
NANOWRIMO_MODE_ENABLED = list()
SCHEDULER_FILENAME = list()
COMMAND_LIST_FILENAME = list()

# This variable tells the Bot if a server's scheduler is running or not
DAILY_MESSAGE_SCHEDULER_CURRENT_STATE = list()

REBOOT_SCHEDULER_FLAG = None

# This variable tells the Bot whether or not it has run initial scheduler setup or not
MESSAGE_SCHEDULER_INIT_FLAG = None

# Global Clock - current UTC time, taken every second
GLOBAL_CLOCK = None

# ----------------------------------------------------------------------- IMPORTS AND GLOBAL VARIABLES #
# ==================================================================================================== #



# ==================================================================================================== #
# INITIALIZATIONS ------------------------------------------------------------------------------------ #

# load_bot_token - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Grabs bot token from tokens file
# INPUTS:
#       - (string) token_filename: the filename where the token is stored
# RETURNS:
#       - (string) token: returns the token
def load_bot_token(token_filename):
    with open(token_filename, "r") as loaded_file:
        for line in loaded_file:
            return line

# set_scheduler  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Runs at first startup and sets the variable MESSAGE_SCHEDULER_INIT_FLAG as a global variable with integer value 0.
# This only runs once per bot startup. It is used to verify whether the scheduler has been initialized as intended,
# as the bot will "re-initialize" itself if it loses internet connectivity or locks up for some reason, and we don't
# want new scheduler functions to run in those circumstances.
# INPUTS:
#       - (bool) value: the value to set the scheduler state to: 1 if already on, 0 if off
# RETURNS:
#       - N/A
def set_scheduler(value):
    global MESSAGE_SCHEDULER_INIT_FLAG
    MESSAGE_SCHEDULER_INIT_FLAG = value

def set_scheduler_reboot_flag(value):
    global REBOOT_SCHEDULER_FLAG
    REBOOT_SCHEDULER_FLAG = value
    
def set_global_clock(value):
    global GLOBAL_CLOCK
    GLOBAL_CLOCK = value

def global_clock():
    threading.Timer(1, global_clock).start()

    now = datetime.datetime.utcnow()

    current_time = now.strftime("%H:%M:%S")
    set_global_clock(current_time)
    
    
# initialize_bot_globals - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Initializes the bot with configuration information read from an INI file and populates the global variable lists
# INPUTS:
#       - (string) config_filename: the master configuration file name
#       - (string) servername: the name of the server to search for in the configuration file INI structure
# RETURNS:
#       - (int) error: returns an error code if there's a problem, 0 otherwise
def initialize_bot_globals(config_filename, servername):
    global GUILD_ID
    global SYSTEM_CHANNEL
    global STARBOARD_FUNCTION_ENABLE
    global STARBOARD_FILENAME
    global STARBOARD_RECEIPTS_FILENAME
    global STARBOARD_OUTPUT_CHANNEL_ID
    global STARBOARD_REACTION_THRESHOLD
    global STARBOARD_EMOJI_DELIMITER
    global RESPONSE_FLAG
    global RESPONSE_FLAG_CASE_SENSITIVE
    global RESPONSE_FLAG_MATCH_EXACT_CASE
    global LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME
    global HOTWORDS_FILENAME
    global HOTWORDS_DELIMITER
    global MACHINE_LEARNING_RESPONSE_FLAG
    global SPELLING_BEE_URL
    global SPELLING_BEE_OUTPUT_CHANNEL_ID
    global SPELLING_BEE_AUTO_POST
    global SPELLING_BEE_POST_TIME
    global SPELLING_BEE_HTML
    global SPELLING_BEE_CSS
    global SPELLING_BEE_PNG
    global SPRINT_BOT_COUNTER
    global SPRINT_BOT_INDIVIDUAL_COUNTER_FOLDER
    global SPRINT_BOT_AUTOTRIGGER
    global SPRINT_BOT_SKIP_ZERO_DAYS
    global SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY
    global NANOWRIMO_MODE_ENABLED
    global SCHEDULER_FILENAME
    global COMMAND_LIST_FILENAME

    global DAILY_MESSAGE_SCHEDULER_CURRENT_STATE
    
    exists = 0
    
    GUILD_ID.append(servername)

    # Only initialize the scheduler init flag on the very first run after the bot is rebooted
    if MESSAGE_SCHEDULER_INIT_FLAG == 0:
        DAILY_MESSAGE_SCHEDULER_CURRENT_STATE.append(int(0))

    exists, current_value = read_ini_file(config_filename, servername, "starboard_function_enable")
    if exists == -1:
        return -1
    STARBOARD_FUNCTION_ENABLE.append(current_value)   

    exists, current_value = read_ini_file(config_filename, servername, "system_channel")
    if exists == -1:
        return -2
    SYSTEM_CHANNEL.append(int(current_value)) 

    exists, current_value = read_ini_file(config_filename, servername, "starboard_filename")
    if exists == -1:
        return -3
    STARBOARD_FILENAME.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "starboard_receipts_filename")
    if exists == -1:
        return -4
    STARBOARD_RECEIPTS_FILENAME.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "starboard_output_channel_id")
    if exists == -1:
        return -5
    STARBOARD_OUTPUT_CHANNEL_ID.append(int(current_value))

    exists, current_value = read_ini_file(config_filename, servername, "starboard_reaction_threshold")
    if exists == -1:
        return -6
    STARBOARD_REACTION_THRESHOLD.append(int(current_value))

    exists, current_value = read_ini_file(config_filename, servername, "starboard_emoji_delimiter")
    if exists == -1:
        return -7
    STARBOARD_EMOJI_DELIMITER.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "response_flag")
    if exists == -1:
        return -8
    RESPONSE_FLAG.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "response_flag_case_sensitive")
    if exists == -1:
        return -9
    RESPONSE_FLAG_CASE_SENSITIVE.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "response_flag_match_exact_case")
    if exists == -1:
        return -10
    RESPONSE_FLAG_MATCH_EXACT_CASE.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "loaded_external_media_config_filename")
    if exists == -1:
        return -11
    LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "hotwords_filename")
    if exists == -1:
        return -12
    HOTWORDS_FILENAME.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "hotwords_delimiter")
    if exists == -1:
        return -13
    HOTWORDS_DELIMITER.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "machine_learning_response_flag")
    if exists == -1:
        return -14
    MACHINE_LEARNING_RESPONSE_FLAG.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_url")
    if exists == -1:
        return -15
    SPELLING_BEE_URL.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_output_channel_id")
    if exists == -1:
        return -16
    SPELLING_BEE_OUTPUT_CHANNEL_ID.append(int(current_value))

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_auto_post")
    if exists == -1:
        return -17
    SPELLING_BEE_AUTO_POST.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_post_time")
    if exists == -1:
        return -18
    SPELLING_BEE_POST_TIME.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_html")
    if exists == -1:
        return -19
    SPELLING_BEE_HTML.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_css")
    if exists == -1:
        return -20
    SPELLING_BEE_CSS.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "spelling_bee_png")
    if exists == -1:
        return -21
    SPELLING_BEE_PNG.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "sprint_bot_counter")
    if exists == -1:
        return -22
    SPRINT_BOT_COUNTER.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "sprint_bot_individual_counter_folder")
    if exists == -1:
        return -23
    SPRINT_BOT_INDIVIDUAL_COUNTER_FOLDER.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "sprint_bot_autotrigger")
    if exists == -1:
        return -24
    SPRINT_BOT_AUTOTRIGGER.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "sprint_bot_skip_zero_days")
    if exists == -1:
        return -28
    SPRINT_BOT_SKIP_ZERO_DAYS.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "sprint_bot_force_all_sprint_history")
    if exists == -1:
        return -29
    SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "nanowrimo_mode_enabled")
    if exists == -1:
        return -25
    NANOWRIMO_MODE_ENABLED.append(current_value)

    exists, current_value = read_ini_file(config_filename, servername, "scheduler_filename")
    if exists == -1:
        return -26
    SCHEDULER_FILENAME.append("Servers/" + str(servername) + "/" + current_value)

    exists, current_value = read_ini_file(config_filename, servername, "command_list_filename")
    if exists == -1:
        return -27
    COMMAND_LIST_FILENAME.append(current_value)
    
    return 0

# clear_global_variables - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Resets the global variable lists so they can be repopulated.
# INPUTS:
#       - N/A
# RETURNS:
#       - N/A
def clear_global_variables():
    GUILD_ID.clear()
    SYSTEM_CHANNEL.clear()
    STARBOARD_FUNCTION_ENABLE.clear()
    STARBOARD_FILENAME.clear()
    STARBOARD_RECEIPTS_FILENAME.clear()
    STARBOARD_OUTPUT_CHANNEL_ID.clear()
    STARBOARD_REACTION_THRESHOLD.clear()
    STARBOARD_EMOJI_DELIMITER.clear()
    RESPONSE_FLAG.clear()
    RESPONSE_FLAG_CASE_SENSITIVE.clear()
    RESPONSE_FLAG_MATCH_EXACT_CASE.clear()
    LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME.clear()
    HOTWORDS_FILENAME.clear()
    HOTWORDS_DELIMITER.clear()
    MACHINE_LEARNING_RESPONSE_FLAG.clear()
    SPELLING_BEE_URL.clear()
    SPELLING_BEE_OUTPUT_CHANNEL_ID.clear()
    SPELLING_BEE_AUTO_POST.clear()
    SPELLING_BEE_POST_TIME.clear()
    SPELLING_BEE_HTML.clear()
    SPELLING_BEE_CSS.clear()
    SPELLING_BEE_PNG.clear()
    SPRINT_BOT_COUNTER.clear()
    SPRINT_BOT_INDIVIDUAL_COUNTER_FOLDER.clear()
    SPRINT_BOT_AUTOTRIGGER.clear()
    SPRINT_BOT_SKIP_ZERO_DAYS.clear()
    SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY.clear()
    NANOWRIMO_MODE_ENABLED.clear()
    SCHEDULER_FILENAME.clear()
    COMMAND_LIST_FILENAME.clear()

# initialize_new_server  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Initializes a newly-connected Discord server by building its filepaths within the server's storage.
# INPUTS:
#       - (int) new_guild_id: the Discord guild ID for the new guild
# RETURNS:
#       - N/A
def initialize_new_server(new_guild_id):
    # Build filepaths for files to be duplicated - this part isn't strictly necessary, but to ensure nothing acts strangely from missing files before they're properly generated, this part is included
    default_external_media_file = DEFAULTS_FOLDER + "/external_media.csv"
    default_hotwords_file = DEFAULTS_FOLDER + "/hotwords.csv"
    default_receipts_file = DEFAULTS_FOLDER + "/receipts.csv"
    default_sprint_counter_file = DEFAULTS_FOLDER + "/sprint_counter.csv"
    default_starboard_file = DEFAULTS_FOLDER + "/starboard.txt"

    # Build new server's file directory
    interim_string = SERVERS_FOLDER + "/" + str(new_guild_id)
    os.mkdir(interim_string)

    # Build destination filepaths for copied files
    new_external_media_file = SERVERS_FOLDER + "/" + str(new_guild_id) + "/external_media.csv"
    new_hotwords_file = SERVERS_FOLDER + "/" + str(new_guild_id) + "/hotwords.csv"
    new_receipts_file = SERVERS_FOLDER + "/" + str(new_guild_id) + "/receipts.csv"
    new_sprint_counter_file = SERVERS_FOLDER + "/" + str(new_guild_id) + "/sprint_counter.csv"
    new_starboard_file = SERVERS_FOLDER + "/" + str(new_guild_id) + "/starboard.txt"

    # Copy files
    shutil.copyfile(default_external_media_file, new_external_media_file)
    shutil.copyfile(default_hotwords_file, new_hotwords_file)
    shutil.copyfile(default_receipts_file, new_receipts_file)
    shutil.copyfile(default_sprint_counter_file, new_sprint_counter_file)
    shutil.copyfile(default_starboard_file, new_starboard_file)

    # Build user sprint totals folder
    interim_string = SERVERS_FOLDER + "/" + str(new_guild_id) + "/" + "User_Sprint_Totals"
    os.mkdir(interim_string)

    # Initialize configparser
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    with open(CONFIG_FILENAME, "a") as config_file:
        interim_string = "\n[" + str(new_guild_id) + "]"
        print(interim_string, file=config_file)

    all_keys = list()
    all_vals = list()
    iterator = 0

    # Copy over default values to the new section
    for (key, val) in config.items("DEFAULT_VALUES"):
        all_keys.append(key)
        all_vals.append(val)

        with open(CONFIG_FILENAME, "a") as config_file:
            interim_string = all_keys[iterator] + " = " + all_vals[iterator]
            print(interim_string, file=config_file) 
        
        iterator += 1

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

# find_guild_position_number - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Finds the position in the configuration storage array 
# INPUTS:
#       - (int) current_id: the current guild ID
# RETURNS:
#       - (int) position: returns the position in the stored global variables array if successful, -1 if failure
def find_guild_position_number(current_id):
    position = 0
    for i in GUILD_ID:
        if int(i) == int(current_id):
            return position
        else:
            position += 1
    return -1


# time_processor - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes the user-given time value and converts it into integers that datetime can process
# INPUTS:
#       - (string) input_time: the time (formatted HH:MM:SS) in UTC
# RETURNS:
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
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS: 
#       - (bool) hotword_already_exists: returns "1" if the hotword is found.
def check_hotword(filename, hotword, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    hotword_already_exists = 0
    
    # Open the CSV file and prep it for Python parsing
    with open(filename, "r") as loaded_file:
        loaded_read = csv.reader(loaded_file, delimiter = HOTWORDS_DELIMITER[f])

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
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
def add_hotword(hotwords_filename, hotword, response, message_sender, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    status = 0
    output_message = ""
    output_message_to_CSV = ""

    # Make sure the hotword isn't already used in the file name before continuing
    if check_hotword(hotwords_filename, hotword) == 0:
        # Open file
        with open(hotwords_filename, "a") as loaded_file:
            # Prep the CSV file for Python parsing
            loaded_write = csv.writer(loaded_file, delimiter = HOTWORDS_DELIMITER[f])

            # Build output string to be appended to the file
            if message_sender == 1:
                output_message = "Success! Trigger phrase `%s` will be responded to with the phrase `%s` and will message the sender." % (hotword, response)
                output_message_to_CSV = "%s␝%s␝%s\n" % (hotword, response, "Yes")
            else:
                output_message = "Success! Trigger phrase `%s` will be responded to with the phrase `%s`." % (hotword, response)
                output_message_to_CSV = "%s␝%s␝%s\n" % (hotword, response, "No")

            loaded_file.write(output_message_to_CSV)
    else:
        output_message = "This trigger phrase is already used. To use this trigger phrase, you can delete it with `!eb hotword delete %s` and re-add it." % (hotword)
    
    return status, output_message

# remove_hotword - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Removes a hotword from the hotwords CSV file
# INPUTS:
#       - (string) hotwords_filename: the location of the hotwords csv file
#       - (string) hotword: the trigger word to be deleted
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
def remove_hotword(hotwords_filename, hotword, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    status = 0
    output_message = ""

    # Check that the hotword even exists in the first place
    if check_hotword(hotwords_filename, hotword, current_guild_id) == 1:
        # Generate a temporary array to store CSV data in
        temp_file = list()
        
        # Read through output file
        with open(hotwords_filename, "r") as loaded_file:
            reader = csv.reader(loaded_file, delimiter = HOTWORDS_DELIMITER[f])

            # Print to temp file while also checking for hotword to be deleted
            for row in reader:
                temp_file.append(row)
                for current_item in row:
                    if current_item == hotword:
                        # If the hotword is found, remove it from the temp file
                        temp_file.remove(row)
        
        # Print the temp file back out to the CSV file
        with open(hotwords_filename, "w") as loaded_file:
            writer = csv.writer(loaded_file, delimiter = HOTWORDS_DELIMITER[f])
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
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS: 
#       - (bool) is_found: returns a 0 if the command was found, -1 if not
#       - (string) location_type: the type of media stored within the address at this command
#       - (string) address: the link to the media, either a URL or a local address
def load_external_media_config(filename, command, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    # This flag is triggered if the given command is found within the configuration file
    post_already_exists_flag = 0

    with open(filename, "r") as loaded_file:
        # Prep the CSV file for Python parsing
        loaded_read = csv.reader(loaded_file, delimiter = HOTWORDS_DELIMITER[f])

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
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: -1 if failed, 0 if successful
#       - (string) output_message: the message given back to the bot to be printed to the user in-line (if necessary)
def add_to_external_media_config(filename, input_string, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

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
    is_found, location_type, address = load_external_media_config(filename, sorted_array[2], current_guild_id)
    if is_found == -1:
        with open(filename, "a") as loaded_file:
            # Prep the CSV file for Python parsing
            loaded_write = csv.writer(loaded_file, delimiter = HOTWORDS_DELIMITER[f])

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
# RETURNS:
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
# RETURNS:
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
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (int) status: the error status of the function. 0 if okay, less than 0 if not
#       - (string) output_message: the string to be printed to Discord to confirm success or failure
def change_configuration(config_category, new_value, current_guild_id):
    # Initialize configparser
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME)

    status = 0
    output_message = ""
    config_category_flag = 0

    for (key, val) in config.items(current_guild_id):
        if key == config_category:
            config_category_flag = 1
            config.set(current_guild_id, key, new_value)

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
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - N/A
def sprint_bot_word_count_processor(message_contents, sprint_bot_counter_filename, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

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

        # Print user's contribution into their respective sprint stats csv
        status = dataprocessing.dump_to_user_file(SPRINT_BOT_INDIVIDUAL_COUNTER_FOLDER[f], current_sprinter_id, today_dateformatted, current_sprinter_wc)

    return status, output_string

# sprint_counter_daily_cleanup - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Every day, resets the daily sprint count cumulative total for each sprinter to zero
# INPUTS:
#       - (string) sprint_bot_counter_filename: the location of the sprint data CSV file
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (int) status: 0 if no errors, <0 otherwise
async def sprint_counter_daily_cleanup(sprint_bot_counter_filename, current_guild_id):
    today = datetime.datetime.now()

    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    # Generate a temporary array to store CSV data in
    temp_file = list()
    
    # Declare variables
    week_set = 0
    month_set = 0
    year_set = 0
    nano_set = 0

    # Read through counter file
    with open(sprint_bot_counter_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = ",")

         # Modify each line item and print to temp file
        for row in reader:
            # Check if it's the beginning of a new month and/or the beginning of a new year; if so, reset the monthly and/or yearly counters
            if today.day == 1:
                month_set = 0
                nano_set = 0

                if today.month == 1:
                    year_set = 0
                else:
                    year_set = int(row[4])

            else:
                month_set = int(row[3])
                year_set = int(row[4])
                nano_set = int(row[6])
            
            # Check if it's a Monday (0); if so, reset the weekly counter
            if datetime.date.today().weekday() == 0:
                week_set = 0
            else:
                week_set = int(row[2])

            out = [row[0], int(0), week_set, month_set, year_set, int(row[5]), nano_set]
            temp_file.append(out)

    # Print the temp file back out to the CSV file
    with open(sprint_bot_counter_filename, "w") as loaded_file:
        writer = csv.writer(loaded_file, delimiter = ",")
        writer.writerows(temp_file)

    if today.day == 1 and NANOWRIMO_MODE_ENABLED[f] == "Yes":
        change_configuration("nanowrimo_mode_enabled", "No", current_guild_id)
        await on_ready()

    return 0
    
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

    # Find current guild position within stored global variables
    current_guild_id = int(message.guild.id)
    f = find_guild_position_number(current_guild_id)

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

    build_content = "%s **%d** %s" % (STARBOARD_EMOJI_DELIMITER[f], count, original_channel.mention)
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

    # Find current guild position within stored global variables
    current_guild_id = int(message.guild.id)
    f = find_guild_position_number(current_guild_id)

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

    build_content = "%s **%d** %s" % (STARBOARD_EMOJI_DELIMITER[f], count, original_channel.mention)
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

    # Find current guild position within stored global variables
    current_guild_id = int(message.guild.id)
    f = find_guild_position_number(current_guild_id)

    # Build up embed
    embed = discord.Embed(title = "EndoBot Trigger Phrases", description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)

    with open(hotwords_filename, "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = HOTWORDS_DELIMITER[f])

        # Build embed field - appends new fields to the end of the previous one to (theoretically) mean that an unlimited number of trigger phrases can be displayed 
        for row in reader:
            embed_body = "**Bot Response:** \"%s\"\n**Reply to Sender?** %s\n\n" % (row[1], row[2])
            embed.add_field(name = row[0], value = embed_body, inline = False)

    channel = message.channel
    await channel.send(embed = embed)

    return status, output_message

# bot_fullhelp - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Prints the bot's current functionality in the form of a few embed posts to the server.
# INPUTS:
#       - (DISCORD CLASS) message: the message class given by discord
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
async def bot_fullhelp(message):

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

# bot_help - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Prints the bot's current functionality in the form of a condensed list to the server.
# INPUTS:
#       - (DISCORD CLASS) message: the message class given by discord
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
async def bot_help(message):
    channel = message.channel

    # Find current guild position within stored global variables
    current_guild_id = int(message.guild.id)
    f = find_guild_position_number(current_guild_id)

    output_string = "```cs\n# ENDOBOT FULL COMMAND LIST #```\n**Command | Brackets Required? | Moderator Privileges Required?**\n\n"

    with open(COMMAND_LIST_FILENAME[f], "r") as loaded_file:
        reader = csv.reader(loaded_file, delimiter = HOTWORDS_DELIMITER[f])
        for row in reader:
            embed1 = discord.Embed(title = "EndoBot Quick Help", description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)
            output_string = output_string + row[0] + " | " + row[1] + " | " + row[2] + "\n"

    embed1.add_field(name = "\u200b",
                     value = output_string,
                     inline = False)

    await channel.send(embed = embed1)
    return 0, None

# leaderboard  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Counts the number of times each user has been starred on the starboard and ranks them greatest-to-least
# INPUTS:
#       - (string) receipts_filename: the location of the receipts CSV file to be processed
#       - (DISCORD CLASS) message: the message that triggered this function and its metadata (used for printing to the right channel)
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
async def leaderboard(receipts_filename, message, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

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
        title_builder = "%s EndoBot Starboard Leaderboard %s" % (STARBOARD_EMOJI_DELIMITER[f], STARBOARD_EMOJI_DELIMITER[f])
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

# sprint_leaderboard - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Generates a Discord embed that lists and sorts all users' word count totals (both daily and cumulative)
# INPUTS:
#       - (string) sprint_counter_filename: the location of the sprint counter CSV file to be processed
#       - (int) channel_id: the message that triggered this function and its metadata (used for printing to the right channel)
#       - (bool) print_message: 0 = No, 1 = Yes, 2 = force override of limited sprint lists.
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (bool) status: -1 if there's a problem, 0 if okay (if necessary)
#       - (string) output_message: an output message to print (if necessary)
async def sprint_leaderboard(sprint_counter_filename, channel_id, print_message, current_guild_id):
    user_id = list()
    day_word_count = list()
    week_word_count = list()
    month_word_count = list()
    year_word_count = list()
    lifetime_word_count = list()

    total_day_count_across_all_users = 0

    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

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
        
        # Sort all users, greatest to least, by zipping the two arrays together and sorting by the second array
        zipped_list = zip(user_id, day_word_count, week_word_count, month_word_count, year_word_count, lifetime_word_count)

        # If generating message on command, sort by yearly total (column 4). Otherwise, sort by daily total (column 1) 
        if print_message != 0:
            sorted_list = sorted(zipped_list, key = lambda x: x[4], reverse = True)
        else:
            sorted_list = sorted(zipped_list, key = lambda x: x[1], reverse = True)

        # Unzip the arrays so they can be re-zipped later during the embed buildup
        tuples = zip(*sorted_list)
        user_list, day_wc, week_wc, month_wc, year_wc, lifetime_wc  = [list(tuple) for tuple in tuples]

        output_message = ""

        iterator = 1

        # Print out sorted results to embed
        for i, j, k, l, m, n in zip(user_list, day_wc, week_wc, month_wc, year_wc, lifetime_wc):
            # Reset output_message_interim
            output_message_interim = ""

            # Get current user based on User ID
            username = client.get_user(int(i))
            split_username = str(username).split("#")

            # Build output string for either the daily messages (print_message == TRUE) or for individual sprints/a la carte leaderboard requests (print_message == FALSE)
            if print_message != 0:
                if SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY[f] == "Yes" or print_message == 2:
                    output_message_interim = "`%d.` **@%s**: %d words today; %d words YTD; %d words lifetime\n" % (iterator, split_username[0], int(j), int(m), int(n))
                    iterator += 1
                elif SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY[f] == "No":
                    if int(j) != 0:
                        output_message_interim = "`%d.` **@%s**: %d words today; %d words YTD; %d words lifetime\n" % (iterator, split_username[0], int(j), int(m), int(n))
                        iterator += 1
            else:
                if SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY[f] == "Yes":
                    output_message_interim = "`%d.` **@%s**: %d words yesterday; %d words YTD; %d words lifetime\n" % (iterator, split_username[0], int(j), int(m), int(n))
                    iterator += 1
                elif SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY[f] == "No":
                    if int(j) != 0:
                        output_message_interim = "`%d.` **@%s**: %d words yesterday; %d words YTD; %d words lifetime\n" % (iterator, split_username[0], int(j), int(m), int(n))
                        iterator += 1

            total_day_count_across_all_users += int(j)
            output_message = output_message + output_message_interim

        # Build up embed, but only if print_message is true
        if print_message:
            # If the bot is not supposed to print anything when no users have sprinted that day, change the output message to reflect that
            if SPRINT_BOT_FORCE_ALL_SPRINT_HISTORY[f] == "No" and total_day_count_across_all_users == 0:
                output_message = "No words have been sprinted yet today!"

            second_output_message = "⚡ **ENDOBOT @SPRINTO ASSISTANT** ⚡\n" + output_message

            # Print to Discord
            channel = client.get_channel(int(channel_id))
            await channel.send(second_output_message)

            return 0, None
        # Otherwise, prepare a report for the morning messages
        else:
            second_output_message = "Yesterday, %d new words were written. Here are the totals:\n\n%s" % (total_day_count_across_all_users, output_message)
            if total_day_count_across_all_users == 0:
                return -20, second_output_message
            else:
                return 0, second_output_message

# spelling_bee_builder - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes the daily NYT Spelling Bee puzzle from the spelling bee website, converts the HTML into an image, and 
# posts the image to a specified Discord channel. Please note that this was developed
# for educational purposes only.
# INPUTS:
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - (string) spelling_bee_solutions: the formatted dataset for the solution to the daily NYT Spelling Bee.
def spelling_bee_builder(current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    url = SPELLING_BEE_URL[f]

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
        working_html_document.write(SPELLING_BEE_CSS[f])
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
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    abs_path = os.path.abspath(SPELLING_BEE_HTML[f])
    abs_path_with_header = "file://" + abs_path
    driver.get(abs_path_with_header)

    driver.set_window_size(width=302, height=290)
    driver.get_screenshot_as_file("spelling_bee.png")

    # Print the puzzle solutions, regardless of however many there may be
    output_string_interim = ""
    count = 1
    for i in answers:
        output_string_interim = output_string_interim + "(" + str(count) + "): ||" + i + "||\n"
        count += 1
    spelling_bee_solutions = "```cs\n# Today's Spelling Bee Solutions #```Remember that all letters must be used at least once in the day's winning word(s) - that means letters can be repeated as many times as necessary!\n\n" + output_string_interim
    return spelling_bee_solutions

# spelling_bee_printer - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Takes the daily NYT Spelling Bee puzzle from the spelling bee website, converts the HTML into an image, and 
# posts the image to a specified Discord channel. Please note that this was developed
# for educational purposes only.
# INPUTS:
#       - (string) channel_id: The Discord channel where the image will be printed
#       - (string) spelling_bee_solutions: solutions for that day's spelling bee 
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# RETURNS:
#       - N/A
async def spelling_bee_printer(channel_id, spelling_bee_solutions, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    url = SPELLING_BEE_URL[f]

    # Prepare the local file so it can be output via Discord
    file = discord.File(SPELLING_BEE_PNG[f])

    # Build the embed
    embed = discord.Embed(title = "NYT Daily Spelling Bee", color=0x0077ff)
    
    # Build the embed's image and footer strings
    today = datetime.date.today()
    footer_string = "Day of " + today.strftime("%d %B %Y") + "\n" + url
    image_string = "attachment://" + SPELLING_BEE_PNG[f]
    embed.set_image(url = image_string)
    embed.set_footer(text = footer_string)

    embed.add_field(name = "\u200b", value = spelling_bee_solutions, inline = False)

    channel = client.get_channel(int(channel_id))

    await channel.send(file = file, embed = embed)

# find_ao3_line  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Selects a random line number from an AO3 HTML dump and prints it to Discord.
# INPUTS:
#       - (string array) chapter_content: the entirety of the AO3 webpage, broken up into chapters (skipping index 0 in the list), and processed to remove HTML artifacts
#       - (DISCORD CLASS) message: the message metadata containing the ID of the channel to post the response
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

    channel = message.channel

    # Post result to Discord
    await channel.send(line_choices[selected_line_number]) 

# list_configuration - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Displays all configuration keys and their currently assigned values to the user.
# INPUTS:
#       - (DISCORD CLASS) message: the sender's original message with all of its metadata (used for printing to the same channel)
# RETURNS:
#       - N/A
async def list_configuration(message, current_guild_id):
    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)
    
    # Initialize configparser
    config = configparser.ConfigParser()
    config.read(CONFIG_FILENAME[f])

    output_message = ""

    # Build up embed
    embed = discord.Embed(title = "EndoBot - Current Configuration", description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)

    for (key, val) in config.items(current_guild_id):
        output_message = output_message + "%s: `%s`\n" % (key, val)

    embed.add_field(name = "\u200b", inline = False, value = output_message)

    channel = message.channel
    await channel.send(embed = embed)

# morning_messages - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Builds an embed with a morning digest, including the day's spelling bee, yesterday's sprint reports, and more
# INPUTS:
#       - (int) channel_id: the channel that this message will be posted in
#       - (int) reset_flag: 0 if the daily sprint counter(s) are to be reset, 1 if not
#       - (int) current_guild_id: the ID for the current guild. Used for global variable parsing.
# OUTPUTS:
#       - N/A

async def morning_messages(channel_id, current_guild_id, force_flag):
    today = datetime.datetime.now()

    words_written = False

    # Find current guild position within stored global variables
    f = find_guild_position_number(current_guild_id)

    url = SPELLING_BEE_URL[f]

    # Create embed and title it with the server's ASCII name
    title_builder = "%s Morning Announcements" % (client.get_guild(int(current_guild_id)))
    embed = discord.Embed(title = title_builder, description = "*For more information, visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot).*", color=0x0077ff)
    
    # If a NaNoWriMo event is going on, include the current/final word count tallies in the morning announcements
    if NANOWRIMO_MODE_ENABLED[f] == "Yes":
        if today.day == 1:
            tuples = nanowrimo.nano_leaderboard(SPRINT_BOT_COUNTER[f])
            status, output_message = nanowrimo.nano_final_leaderboard_postprocessing(tuples, client)
            output_message = "```cs\n# Final NaNoWriMo Results #```" + output_message
            embed.add_field(name = "\u200b", inline = False, value = output_message)
        else:
            tuples = nanowrimo.nano_leaderboard(SPRINT_BOT_COUNTER[f])
            status, output_message = nanowrimo.nano_leaderboard_postprocessing(tuples, client)
            output_message = "```cs\n# Current NaNoWriMo Standings #```" + output_message
            embed.add_field(name = "\u200b", inline = False, value = output_message)

    # Calculate and print the sprint leaderboard
    status, sprint_output = await sprint_leaderboard(SPRINT_BOT_COUNTER[f], int(channel_id), 0, current_guild_id)
    output_message = "```cs\n# Yesterday's Sprint Totals #```%s" % sprint_output
    embed.add_field(name = "\u200b", inline = False, value = output_message)

    if status == -20:
        # No words were written in the previous day
        words_written = False
    else:
        words_written = True

    # If forced, do not reset the daily counter (allows for morning messages at any time of the day)
    if force_flag == 0:
        # Reset the daily sprint counter for each user
        status = await sprint_counter_daily_cleanup(SPRINT_BOT_COUNTER[f], current_guild_id)

    if SPELLING_BEE_AUTO_POST[f] == "Yes":
        # Print the link to the day's Wordle
        output_message = "```cs\n# Today's Online Puzzles #```The Wordle of the Day can be found [here!](https://www.nytimes.com/games/wordle/index.html)\nThe Quordle of the Day can be found [here!](https://www.quordle.com/#/)\nThe Weaver of the Day can be found [here!](https://wordwormdormdork.com/)"
        embed.add_field(name = "\u200b", inline = False, value = output_message)

        # Print details about the day's NYT Spelling Bee
        spelling_bee_solutions = spelling_bee_builder(current_guild_id)
        spelling_bee_solutions += "\n[Spelling Bee source](%s)" % url
        embed.add_field(name = "\u200b", inline = False, value = spelling_bee_solutions)

        # Prepare the locally-hosted image generated by spelling_bee_builder for use in Discord embeds
        file = discord.File(SPELLING_BEE_PNG[f])
        image_string = "attachment://" + SPELLING_BEE_PNG[f]
        embed.set_image(url = image_string)
    
    # Build the embed's footer string
    today = datetime.date.today()
    footer_string = "Day of %s" % (today.strftime("%d %B %Y"))
    embed.set_footer(text = footer_string)

    # If the server is configured not to post when there have been no sprints that day, then skip the morning messages
    if words_written == True and SPRINT_BOT_SKIP_ZERO_DAYS[f] == "Yes":
        # Print embed to Discord
        channel = client.get_channel(int(channel_id))
        if SPELLING_BEE_AUTO_POST[f] == "Yes":
            await channel.send(file = file, embed = embed)
        else:
            await channel.send(embed = embed)
    elif words_written == False and SPRINT_BOT_SKIP_ZERO_DAYS[f] == "No":
        # Print embed to Discord
        channel = client.get_channel(int(channel_id))
        if SPELLING_BEE_AUTO_POST[f] == "Yes":
            await channel.send(file = file, embed = embed)
        else:
            await channel.send(embed = embed)

# bot_command_processor  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# A function that specifically processes through !eb prefixed messages and sorts out respondable prompts from the following line items
# INPUTS:
#       - (int) standard_channel: the standard "#General" channel where the welcome message will be posted.
# RETURNS:
#       N/A 
async def new_server_welcome_message(standard_channel):
    embed = discord.Embed(title = "Welcome to EndoBot!", description = "", color=0x0077ff)
    embed.add_field(name = "\u200b",
                     value = "```cs\n# WELCOME TO ENDOBOT! #```\nEndoBot is a multi-function Discord bot written and developed in Python by JA Mann.\n\n```cs\n# BASIC OVERVIEW #```\n • **Sprinto Bot Tools**: record sprint results and compile daily/monthly/yearly leaderboards\n • **Monthly NaNoWriMo**: choose a monthly writing goal - EndoBot will keep track of your word count, your progress, and how many words per day you have to write to finish in time\n • **Starboard**: frame posts in a hall of fame (or hall of shame) after a certain number of reaction emojis are added to a post\n • **Trigger Phrases**: set certain words or phrases as triggers to prompt a pre-determined bot reply\n • **AO3 Randomizer**: pull a random line from an AO3 fic with just a link\n```cs\n# HELP AND COMMAND LIST #```\nTry `!eb help` for more information - or visit the bot's [GitHub page](https://github.com/jadonmann/EndoBot) for a full breakdown of each feature!",
                     inline = False)

    # Prepare the locally-hosted image generated by the welcome message for use in Discord embeds
    embed.set_image(url = "https://i.gifer.com/7Bi.gif")

    # Print embed to Discord
    channel = client.get_channel(int(standard_channel))
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

    if message.author.id == int("330900130997862400"):
        mod = True
    else:
        mod = False

    # Find server ID
    current_guild_id = int(message.guild.id)
    f = find_guild_position_number(current_guild_id)

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
                            
                            # Make sure there's not a problem with any of the "find"s - aka there was a problem with the input string
                            if start_0 == -1 or end_0 == 0:
                                # Send an error message to the user 
                                status = -1
                            else:
                                # Finish constructing command list
                                command = new_string[0][start_0:end_0]

                                bot_response = new_string[1]

                                # Check to see if the author should be tagged or not and convert the response from a string to a boolean   
                                tag_author = 0
                                if new_string[2].find("Yes") != -1 or new_string[2].find("yes") != -1: 
                                    tag_author = 1

                                # If all information is properly constructed, add the hotword
                                status, response = add_hotword(HOTWORDS_FILENAME[f], command, bot_response, tag_author, current_guild_id)
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

                            status, response = remove_hotword(HOTWORDS_FILENAME[f], new_string[0])
                            await channel.send(response)
                    else:
                        status = -1
                        response = "Sorry, you lack the necessary permissions to use this command."
                elif command_array[2] == "list":
                    status, response = await list_hotwords(HOTWORDS_FILENAME[f], message)

        elif command_array[1] == "leaderboard":
            status, response = await leaderboard(STARBOARD_RECEIPTS_FILENAME[f], message)

        elif command_array[1] == "sprintstats":
            if number_of_elements > 2:
                if command_array[2] == "edit":
                    if number_of_elements > 4:
                        # Remove brackets, in the event the user is using the same bracket notation as other commands
                        command_array[3] = command_array[3].replace("[","")
                        command_array[3] = command_array[3].replace("]","")
                        command_array[4] = command_array[4].replace("[","")
                        command_array[4] = command_array[4].replace("]","")
                        
                        # Filter out user ID from command array
                        if command_array[4].find("@") != -1:
                            user_id_interim = command_array[4].split("<@!")
                            user_id_interim_2 = user_id_interim[1].split(">")
                            user_id_interim_3 = user_id_interim_2[0]
                        else:
                            user_id_interim_3 = command_array[4]

                        if user_id_interim_3.isdigit():
                            user_id = int(user_id_interim_3)

                            # Filter out valid integer value from command array
                            command_array[3] = command_array[3].replace("+","")
                            value_to_pass = command_array[3].replace("-","")

                            if value_to_pass.isdigit():
                                value_to_pass = int(value_to_pass)

                                if command_array[3].find("-") != -1:
                                    value_to_pass = -abs(value_to_pass)
                                else:
                                    value_to_pass = abs(value_to_pass)

                                wordsprints.adjust_sprintstats(value_to_pass, user_id, SPRINT_BOT_COUNTER[f])
                                await channel.send("Sprint leaderboard updated!")
                                status, response = await sprint_leaderboard(SPRINT_BOT_COUNTER[f], int(message.channel.id), 1, current_guild_id)
                            
                            else:
                                status = -1
                                response = "Sorry, that is an invalid number!"
                        else:
                            status = -1
                elif command_array[2] == "forceupdate" or command_array[2] == "force_update":
                    if mod == True:
                        status = await sprint_counter_daily_cleanup(SPRINT_BOT_COUNTER[f], current_guild_id)
                        status = 0
                        await channel.send("Sprint Counter daily counter update forced!")
                    else:
                        status = -1
                        response = "Sorry, you lack the necessary permissions to use this command."
                elif command_array[2] == "leaderboard":
                    status, response = await sprint_leaderboard(SPRINT_BOT_COUNTER[f], int(message.channel.id), 1, current_guild_id)
                elif command_array[2] == "fullleaderboard":
                    status, response = await sprint_leaderboard(SPRINT_BOT_COUNTER[f], int(message.channel.id), 2, current_guild_id)

        elif command_array[1] == "fullhelp":
            status, response = await bot_fullhelp(message)

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
            spelling_bee_solutions = spelling_bee_builder(current_guild_id)
            await spelling_bee_printer(int(message.channel.id), spelling_bee_solutions, current_guild_id)

        elif command_array[1] == "reboot":
            if mod == True:
                await channel.send("Rebooting EndoBot....")
                await on_ready()
                await asyncio.sleep(2)
                await channel.send("EndoBot rebooted!")
            else:
                status = -1
                response = "Sorry, you lack the necessary permissions to use this command."

        elif command_array[1] == "config":
            if mod == True:
                if number_of_elements > 2:
                    # Check to see if user wants to list all metadata
                    if command_array[2] == "list":
                        await list_configuration(message, current_guild_id)

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

                                    status, response = change_configuration(config_category, new_value, str(current_guild_id))
                                    await channel.send(response)
                                    await on_ready()
                            else:
                                status = -1
                        else:
                            status = -1
            else:
                status = -1
                response = "Sorry, you lack the necessary permissions to use this command."
        
        elif command_array[1] == "nanowrimo":
            if number_of_elements > 2:
                if command_array[2] == "enroll":
                    if NANOWRIMO_MODE_ENABLED[f] == "Yes":
                        if number_of_elements > 3:
                            if command_array[3].isdigit():
                                nanowrimo.set_nano_goal(SPRINT_BOT_COUNTER[f], int(message.author.id), command_array[3])
                                output = "Success! You have been enrolled in NaNoWriMo word count tracking with a goal of %s words." % (command_array[3])
                                await channel.send(output)
                            else: 
                                status = -1
                                response = "Please enter a valid word count!"
                        else:
                            status = -1
                            response = "Please enter a valid word count!"
                    else:
                        await channel.send("There currently isn't a NaNoWriMo challenge running! Type `!eb nanowrimo enable` to enable it and begin the competition!")

                if command_array[2] == "withdraw":
                    if NANOWRIMO_MODE_ENABLED[f] == "Yes":
                        nanowrimo.delete_nano_goal(SPRINT_BOT_COUNTER[f], int(message.author.id))
                        await channel.send("NaNoWriMo participation withdrawn!")
                    else:
                        await channel.send("There currently isn't a NaNoWriMo challenge running!")
                
                if command_array[2] == "check":
                    if NANOWRIMO_MODE_ENABLED[f] == "Yes":
                        goal, progress = nanowrimo.see_nano_goal(SPRINT_BOT_COUNTER[f], int(message.author.id))
                        output = "This month, you have written a total of %s words. Your goal is %s." % (progress, goal)
                        delta_wc = int(progress) - int(goal)
                        if delta_wc < 0:
                            output = output + "\n You've beaten your goal by %s words. Congrats!" % abs(delta_wc)
                        else:
                            output = output + "\nYou still have %s words to go!" % abs(delta_wc)
                        await channel.send(output)
                    else:
                        await channel.send("There currently isn't a NaNoWriMo challenge running! Type `!eb nanowrimo enable` to enable it and begin the competition!")
                
                if command_array[2] == "enable":
                    if NANOWRIMO_MODE_ENABLED[f] == "No":
                        change_configuration("nanowrimo_mode_enabled", "Yes", str(current_guild_id))
                        await channel.send("A NaNoWriMo competition has been enabled! Enter your word count goal with `!eb nanowrimo enroll [number]` (without brackets).")
                        await on_ready()
                    else:
                        await channel.send("A NaNoWriMo challenge is already running!")
                    
                if command_array[2] == "disable":
                    if NANOWRIMO_MODE_ENABLED[f] == "Yes":
                        change_configuration("nanowrimo_mode_enabled", "No", str(current_guild_id))
                        await channel.send("The NaNoWriMo competition has been called off!")
                        await on_ready()
                    else:
                        await channel.send("There currently isn't a NaNoWriMo challenge running!")

                if command_array[2] == "leaderboard":
                    if NANOWRIMO_MODE_ENABLED[f] == "Yes":
                        tuples = nanowrimo.nano_leaderboard(SPRINT_BOT_COUNTER[f])
                        status, output_message = nanowrimo.nano_leaderboard_postprocessing(tuples, client)

                        embed = discord.Embed(title = "⚡ EndoBot @Sprinto Assistant ⚡", color=0x0077ff)
                        embed.add_field(name = "NaNoWriMo Word Count Totals", inline = False, value = output_message)
                        embed.set_footer(text = "`!eb nanowrimo enroll [wordcount]` (without brackets) to join!")

                        # Print to Discord
                        await channel.send(embed = embed)
                    else:
                        await channel.send("There currently isn't a NaNoWriMo challenge running!")

        elif command_array[1] == "admin":
            if command_array[2] == "forcemorningmessages":
                if mod == True:
                    await morning_messages(int(channel.id), current_guild_id, 1)
                else:
                    status = -1
                    response = "Sorry, you lack the necessary permissions to use this command."

        elif command_array[1] == "welcome":
            await new_server_welcome_message(int(channel.id))
        
        elif command_array[1] == "dev1":
            if message.author.id != int("330900130997862400"):
                status = -1
                response = "Sorry, you lack the necessary permissions to use this command."
            else:
                ## PLACE COMMANDS UNDER DEVELOPMENT HERE ##
                output_graph = "output_graph.png"
                status = dataprocessing.test_graph("Servers", current_guild_id, str(command_array[2]), output_graph)
                if status != -1:
                    embed = discord.Embed(title = "User Sprint Graph Over Time", color=0x0077ff)
                    
                    file = discord.File(output_graph)
                    image_string = "attachment://" + output_graph
                    embed.set_image(url = image_string)

                    await channel.send(file = file, embed = embed)

        elif command_array[1] == "dev2":
            result = wordsprints.test_script(client, command_array[2])
            await channel.send(result)
                
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

# Guild First Run  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_guild_join(new_guild):
    # Initialize ini reader
    config = configparser.ConfigParser()

    # Load in configuration file
    configuration_file = config.read(CONFIG_FILENAME)
    sections = config.sections()
    
    sys_channel = new_guild.system_channel  

    # If the configuration file is missing for some reason, throw an error
    if not configuration_file:
        print("INITIALIZATION ERROR: %s file not found." % (CONFIG_FILENAME))
        quit()
    else:
        # Check to see if the current guild has configuration data stored
        guild_is_found = 0
        for current_id in sections:
            if current_id == int(new_guild.id):
                guild_is_found = 1
            else:
                continue

        if guild_is_found == 1:
            # If the guild is found, do nothing
            print("NEW GUILD: This guild was already stored in EndoBot's configuration files!")
        else:
            # If the guild is not found, generate new configuration data
            print("NEW GUILD: This guild was NOT already stored in EndoBot's configuration files!\nGenerating relevant files...")
            initialize_new_server(int(new_guild.id))
            await on_ready()

            # Replace the default server IDs in the server's configuration file with the system channel
            change_configuration("system_channel", str(sys_channel.id), str(new_guild.id))
            change_configuration("starboard_output_channel_id", str(sys_channel.id), str(new_guild.id))
            change_configuration("spelling_bee_output_channel_id", str(sys_channel.id), str(new_guild.id))
            await on_ready()

            # Try to post welcome message in the system (#general) channel
            if sys_channel.permissions_for(new_guild.me).send_messages:
                await new_server_welcome_message(int(sys_channel.id))
            # If that doesn't work, try and find the first channel that will allow a message to be posted
            else:
                for channel in new_guild.text_channels:
                    if channel.permissions_for(new_guild.me).send_messages:
                        await new_server_welcome_message(int(sys_channel.id))
                        break

# Startup  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_ready():
    # Clear the global variable buffers
    clear_global_variables()

    # Initialize ini reader
    config = configparser.ConfigParser()

    # Load in configuration file
    configuration_file = config.read(CONFIG_FILENAME)
    sections = config.sections()

    # If the configuration file is missing for some reason, throw an error
    if not configuration_file:
        print("INITIALIZATION ERROR: %s file not found." % (CONFIG_FILENAME))
        quit()
    else:
        # Initialize the bot and bot variables
        for current_id in sections:
            # Skip the example and default_values sections, as they are purely informational
            if current_id != "DEFAULT_VALUES" and current_id != "EXAMPLE":
                error = initialize_bot_globals(CONFIG_FILENAME, current_id)
                if error != 0:
                    print("INITIALIZATION ERROR: loading of %s exited with Error Code %d." % (CONFIG_FILENAME, error))
                    quit()

                f = find_guild_position_number(current_id)
                
                if MESSAGE_SCHEDULER_INIT_FLAG == 0:
                    client.loop.create_task(background_task(0, SPELLING_BEE_OUTPUT_CHANNEL_ID[f], current_id))
                elif MESSAGE_SCHEDULER_INIT_FLAG == 1:
                    print("[SCHEDULER] The scheduler has already been initialized. Skipping re-initialization.")

        # ---- DEBUG
        # DM me that the bot has started or restarted
        at_endo = await client.fetch_user(330900130997862400)
        if MESSAGE_SCHEDULER_INIT_FLAG == 0:
            await at_endo.send("The bot has booted!")
        elif MESSAGE_SCHEDULER_INIT_FLAG == 1:
            await at_endo.send("The bot has rebooted!")

        # After this function runs for the first time, set the scheduler global to 1 so it is not reinitialized accidentally upon bot reconnection
        set_scheduler(1)


        # Print message stating that the bot has connected to Discord
        print("\n\n\n\n\n\n\n\n\n")
        print(f'{client.user.name} has connected to Discord!')
        print("=========================================================================")


# # On Bot Disconnect - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# @client.event
# async def on_disconnect():
#     # Print message stating that the bot has connected to Discord
#     print("=========================================================================")
#     print(f'{client.user.name} has disconnected from Discord!')

#     # Enable the trigger that kills each thread
#     set_scheduler_reboot_flag(1)

#     # Wait until each thread has gone through its one second cycle
#     await asyncio.sleep(2)

#     # Disable the trigger that kills each thread
#     set_scheduler_reboot_flag(0)

#     # Tell the Bot that the scheduler can be reset again 
#     set_scheduler(0)
    
#     print("DISCONNECTED - rebooting EndoBot....")
#     os.execv(sys.argv[0], sys.argv)
    

# Message Detection Wrapper  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_message(message):
    # Print debug line to console
    print(f'[{message.guild}] #{message.channel} | @{message.author}: {message.content}')

    # Find server ID
    if not isinstance(message.channel, discord.channel.DMChannel):
        current_guild_id = int(message.guild.id)
        f = find_guild_position_number(current_guild_id)

        # Validate that this server's configuration files already exists by validating that "f" != -1, which is a hardcoded error state for a server ID that's not in record
        if f == -1:
            print("ERROR: server with ID %s has not been initialized." % (current_guild_id))
            # quit() - eventually replace with on_guild_join(message.guild)
            f = 0

        # Convert message to all lower-case for easier sorting (if set to do so in configuration file)
        if(RESPONSE_FLAG_CASE_SENSITIVE[f] == "No"):
            formatted_message = message.content.lower()
            interim_ML_RF = MACHINE_LEARNING_RESPONSE_FLAG[f].lower()
        else:
            formatted_message = message.content
            interim_ML_RF = MACHINE_LEARNING_RESPONSE_FLAG[f]
        
        # Ignore all bot messages
        if not message.author.bot:
            # Search for response flags
            if formatted_message.startswith("!eb"):
                await bot_command_processor(message, formatted_message)

            # Check for response flag contents if they are the entirety of the text - if so, do not @ the poster
            elif formatted_message == RESPONSE_FLAG[f].lower() and RESPONSE_FLAG_CASE_SENSITIVE[f] != "Yes":
                # parse_gdoc()

                # sanitize_file(initial_filename, filename)

                line = find_line(STARBOARD_FILENAME[f])
                await message.channel.send(line)

            elif formatted_message == RESPONSE_FLAG[f] and RESPONSE_FLAG_CASE_SENSITIVE[f] == "Yes":
                line = find_line(STARBOARD_FILENAME[f])
                await message.channel.send(line)

            # Check for response flag contents if they are anywhere within the content of the text - if so, @ the poster
            elif formatted_message.find(RESPONSE_FLAG[f].lower()) != -1 and RESPONSE_FLAG_MATCH_EXACT_CASE[f] != "Yes":
                # Assign spoken username to variable
                user = message.author

                line = find_line(STARBOARD_FILENAME[f])
                await message.channel.send('{0.author.mention} '.format(message) + line)
            
            # Generate a machine learning response based on the starboard file
            elif formatted_message == interim_ML_RF:
                machine_learning = open(STARBOARD_FILENAME[f], encoding='utf8').read()
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
                with open(HOTWORDS_FILENAME[f], "r") as hotwords_file:
                    # Read in hotwords_file CSV
                    hotwords_read = csv.reader(hotwords_file, delimiter = HOTWORDS_DELIMITER[f])

                    # Check each row in the CSV for the trigger word (in any format)
                    for row_split in hotwords_read:
                        # row_split = row[0].split(HOTWORDS_DELIMITER)
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
                status, response = sprint_bot_word_count_processor(message.content, SPRINT_BOT_COUNTER[f], current_guild_id)
                # If there were no problems, also print out the current leaderboard
                if status == 0 and (SPRINT_BOT_AUTOTRIGGER[f] == "Yes" or SPRINT_BOT_AUTOTRIGGER[f] == "yes"):
                    print("[WORD SPRINT PROCESSOR] Sprint results processed.")
                    await sprint_leaderboard(SPRINT_BOT_COUNTER[f], int(message.channel.id), 1, current_guild_id)
                    # If NaNo is enabled, then also output a NaNo embed
                    if(NANOWRIMO_MODE_ENABLED[f] == "Yes" or NANOWRIMO_MODE_ENABLED[f] == "Yes"):
                        tuples = nanowrimo.nano_leaderboard(SPRINT_BOT_COUNTER[f])
                        status, output_message = nanowrimo.nano_leaderboard_postprocessing(tuples, client)

                        embed = discord.Embed(title = "⚡ EndoBot @Sprinto Assistant ⚡", color=0x0077ff)
                        embed.add_field(name = "NaNoWriMo Word Count Totals", inline = False, value = output_message)
                        embed.set_footer(text = "`!eb nanowrimo enroll [wordcount]` (without brackets) to join!")

                        # Print to Discord
                        await message.channel.send(embed = embed)
                
# Starboard Emoji Reaction Parser  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_raw_reaction_add(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = get(message.reactions, emoji = payload.emoji.name)

    # Find server ID
    current_guild_id = int(message.guild.id)
    f = find_guild_position_number(current_guild_id)

    output_channel = STARBOARD_OUTPUT_CHANNEL_ID[f] 

    if payload.emoji.name == STARBOARD_EMOJI_DELIMITER[f] and STARBOARD_FUNCTION_ENABLE[f] == "Yes":
        count = reaction.count
        if count > (int(STARBOARD_REACTION_THRESHOLD[f]) - 1):

            # Verify that a receipts file exists; if one doesn't, create it
            if not exists(STARBOARD_RECEIPTS_FILENAME[f]):
                with open(STARBOARD_RECEIPTS_FILENAME[f], "w") as receipts_file:
                    receipts_write = csv.writer(receipts_file)

            # Check the receipts file to see if there's already an auto-generated response message created for that reacted discord message
            post_already_exists_flag = 0

            with open(STARBOARD_RECEIPTS_FILENAME[f], "r") as receipts_file:
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
                with open(STARBOARD_RECEIPTS_FILENAME[f], "a") as receipts_file:
                    receipts_write = csv.writer(receipts_file)
                    receipts_write.writerow([message.author.id, payload.message_id, response_id.id])
                
                # Put the sin in the sin bin (if there's actually content in the message)
                if message.content:
                    with open(STARBOARD_FILENAME[f], "a") as sinbin:
                        output_message = "%s\n" % (message.content)
                        sinbin.write(output_message)

# # Post Scheduler - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# async def post_scheduler(output_channel, current_guild_id):
#     while True:
#         if REBOOT_SCHEDULER_FLAG == 0:
#             f = find_guild_position_number(current_guild_id)
#             if GLOBAL_CLOCK == SPELLING_BEE_POST_TIME[f]:
#                 interim_string = "[SCHEDULER] SUCCESS - server %s printed the daily message as expected." % str(current_guild_id)
#                 print(interim_string)
#                 # await morning_messages(output_channel, current_guild_id)
#         else:
#             break
    
@tasks.loop(hours=24)
async def called_once_a_day(output_channel, current_guild_id):
    await client.wait_until_ready()
    print("Posting a scheduled post!")
    await morning_messages(output_channel, current_guild_id, 0)

async def background_task(force_flag, output_channel, current_guild_id):
    DELAY = 15
    DAY_SECONDS = 86400

    f = find_guild_position_number(current_guild_id)
    
    # Build up the daily message time value from numbers acquired in the configuration.ini file
    sb_status, sb_hour, sb_minute, sb_second = time_processor(SPELLING_BEE_POST_TIME[f])
    if sb_status == 0:
        DAILY_MESSAGE_TIME = datetime.time(sb_hour, sb_minute, sb_second)      

    if DAILY_MESSAGE_SCHEDULER_CURRENT_STATE[f] == 0 or force_flag == 1:
        # Set current_state flag to 1 so the bot knows if there's already a schedule running
        DAILY_MESSAGE_SCHEDULER_CURRENT_STATE[f] == 1

        # Run in a continuous loop
        while REBOOT_SCHEDULER_FLAG == 0:
            # Obtain the current time
            now = datetime.datetime.utcnow()

            # Calculate how long it will be until the next trigger time
            target_time = datetime.datetime.combine(now.date(), DAILY_MESSAGE_TIME)
            seconds_until_target = (target_time - now).total_seconds()

            # If the trigger time is the next calendar day, add in a full day of seconds to the timer
            if seconds_until_target <= 0:
                seconds_until_target = DAY_SECONDS + seconds_until_target

            print("[%s] SCHEDULER: the current time is %s. The scheduled time is %s, which is in appx. %s seconds." % (client.get_guild(int(current_guild_id)), now, DAILY_MESSAGE_TIME, str(seconds_until_target)))

            if force_flag == 0:
                # Tell the bot to wait that many seconds
                await asyncio.sleep(seconds_until_target)

            await called_once_a_day(output_channel, current_guild_id)

            if force_flag == 1:
                break
    
        if force_flag == 0:
            # if the bot gets out of its loop for some reason, set the scheduler back to 0
            DAILY_MESSAGE_SCHEDULER_CURRENT_STATE[f] = 0
            interim_string = "[%s] SCHEDULER: the scheduler reached its terminus. Resetting back to 0." % (client.get_guild(int(current_guild_id)))
            print(interim_string)
    
    else:
        interim_string = "[%s] SCHEDULER: the scheduler is already running. Duplicate schedule removed." % (client.get_guild(int(current_guild_id)))
        print(interim_string)
    

# INIT - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
if __name__ == "__main__":
    # Load bot token
    TOKEN = load_bot_token(TOKEN_FILENAME)

    # Initialize scheduler
    set_scheduler(0)
    set_scheduler_reboot_flag(0)

    # Begin Global Clock
    # global_clock()

    # Begin Bot
    client.run(TOKEN)

# --------------------------------------------------------------------- ACTIVE DISCORD ASYNC FUNCTIONS #
# ==================================================================================================== #
