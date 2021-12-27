########################################################################################################
# ENDOBOT ============================================================================================ #
#
# Built using the Discord.py Python API
# Written by JA Mann
# 
# Future implementation plans:
# - AO3 fic scrubber/random line repeater
# - More general abstraction of the code into functions, classes, and scripts
# - Fix Gdocs API credentials problem
# - Add .mobi/.epub readability
# - Add ingress pipeline with ability to handle various different file types
# - Add configuration file that can be updated manually or through a command
# - Spoiler all images originally posted in a NSFW channel
# - Add new server initialization function
# - Handle case of burger emoji delimiter being used organically in message
#
# Current implementations:
# - Random line generator (read from a .txt file imported from a Google Doc)
# - Fixed for the chance that a Tenor gif might cause the bot to embed any link instead of just the Tenor gif
# - Import all global variables from configuration file
# - Added ability to choose specific flag in the configuration file
# - Starboard leaderboard (added more rigorous data storage in the receipts.csv file)
#
# ============================================================================================ ENDOBOT #
########################################################################################################




# ==================================================================================================== #
# IMPORTS AND GLOBAL VARIABLES ----------------------------------------------------------------------- #

from __future__ import print_function
from discord.audit_logs import _transform_verification_level

from oauth2client import client
from os.path import exists

import random
import os
import discord
import numpy as np
import datetime
import csv
import re

import AO3

import configparser

from discord.utils import get

URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""

# Initialize Global Variables (temporary implementation)
TOKEN = ""
FILENAME = ""
RECEIPTS_FILENAME = ""
STARBOARD_OUTPUT_CHANNEL_ID = ""
STARBOARD_REACTION_THRESHOLD = ""
STARBOARD_EMOJI_DELIMITER = ""
RESPONSE_FLAG = ""
RESPONSE_FLAG_CASE_SENSITIVE = ""
RESPONSE_FLAG_MATCH_EXACT_CASE = ""

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# ----------------------------------------------------------------------- IMPORTS AND GLOBAL VARIABLES #
# ==================================================================================================== #



# ==================================================================================================== #
# INITIALIZATIONS ------------------------------------------------------------------------------------ #

# read_ini_file  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Read an INI configuration file
# INPUTS:
#       - (string) filename: the INI file to be read
#       - (string) section: the section to search for
#       - (string) key: the key to search for within the previously specified section
# RETURNS:
#       - (string) value: the value stored at a specific section and key in an INI file
def read_ini_file(filename, section, key):
    config = configparser.ConfigParser()
    config.read(filename)
    
    return config[section][key]

# initialize_bot - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Initializes the bot with configuration information read from an INI file
# INPUTS:
#       - (string) config_filename: the master configuration file name
#       - (string) servername: the name of the server to search for in the configuration file INI structure
# RETURNS:
#       - (string) token: the server token used to initialize the connection with the Discord API
#       - (string) starboard_filename: the filename where the starboarded messages are stored
#       - (string) starboard_receipts: the filename where the starboard message metadata is stored
#       - (string) starboard_output_channel_id: the Discord-side token for the selected starboard channel
#       - (string) starboard_reaction_threshold: minimum number of react emojis needed to trigger bot response
#       - (string) starboard_emoji_delimiter: emoji that the bot searches for when a post is reacted upon
#       - (string) response_flag: the trigger phrase used to generate a bot-selected starboard response message
#       - (string) response_flag_case_sensitive: whether or not the bot should search for a case-sensitive match of the response flag ("Yes"/"No")
#       - (string) response_flag_match_exact_case: whether or not the bot should search for an exact case match of the response flag ("Yes","No")
#       - (string) loaded_external_media_config_filename: location of the server's external media configuration file
#       - (string) hotwords_filename: location of the server's hotwords configuration file
def initialize_bot(config_filename, servername):
    token = read_ini_file(config_filename, servername, "token")
    starboard_filename = read_ini_file(config_filename, servername, "starboard_filename")
    starboard_receipts = read_ini_file(config_filename, servername, "starboard_receipts")
    starboard_output_channel_id = read_ini_file(config_filename, servername, "starboard_output_channel_id")
    starboard_reaction_threshold = read_ini_file(config_filename, servername, "starboard_reaction_threshold")
    starboard_emoji_delimiter = read_ini_file(config_filename, servername, "starboard_emoji_delimiter")
    response_flag = read_ini_file(config_filename, servername, "response_flag")
    response_flag_case_sensitive = read_ini_file(config_filename, servername, "response_flag_case_sensitive")
    response_flag_match_exact_case = read_ini_file(config_filename, servername, "response_flag_match_exact_case")
    loaded_external_media_config_filename = read_ini_file(config_filename, servername, "loaded_external_media_config_filename")
    hotwords_filename = read_ini_file(config_filename, servername, "hotwords_filename")

    return token, starboard_filename, starboard_receipts, starboard_output_channel_id, starboard_reaction_threshold, starboard_emoji_delimiter, response_flag, response_flag_case_sensitive, response_flag_match_exact_case, loaded_external_media_config_filename, hotwords_filename

TOKEN, FILENAME, RECEIPTS_FILENAME, STARBOARD_OUTPUT_CHANNEL_ID, STARBOARD_REACTION_THRESHOLD, STARBOARD_EMOJI_DELIMITER, RESPONSE_FLAG, RESPONSE_FLAG_CASE_SENSITIVE, RESPONSE_FLAG_MATCH_EXACT_CASE, LOADED_EXTERNAL_MEDIA_CONFIG_FILENAME, HOTWORDS_FILENAME = initialize_bot("configuration.ini", "489245389854343170")
STARBOARD_OUTPUT_CHANNEL_ID = int(STARBOARD_OUTPUT_CHANNEL_ID)
STARBOARD_REACTION_THRESHOLD = int(STARBOARD_REACTION_THRESHOLD)

# ------------------------------------------------------------------------------------ INITIALIZATIONS #
# ==================================================================================================== #



# ==================================================================================================== #
# LOCAL FUNCTIONS ------------------------------------------------------------------------------------ #

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
# Removes a hotword to the hotwords CSV file
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
                     value = "```cs\n# BOT CONFIGURATION #```\nThese commands allow moderators and server owners to change bot configuration settings without having to manually adjust or change any bot files. WARNING: this can permanently damage bot functionality if not handled correctly.\n\n`!eb config`\nThis command lists all available configuration options and their default/expected values.\n\n`!eb config [configuration option] [value]`\nThis command allows a moderator to change a configuration option. The brackets are required!",
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
                    unique_users_stats[cc] += 10
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
            output_message_interim = "**@%s**: %d starred posts\n" % (split_username[0], int(j/10))
            output_message = output_message + output_message_interim

        embed.add_field(name = "\u200b", inline = False, value = output_message)

        # Print to Discord
        channel = message.channel
        await channel.send(embed = embed)

    return 0, None
    
# ------------------------------------------------------------------------------------ EMBED FUNCTIONS #
# ==================================================================================================== #



# ==================================================================================================== #
# !EB BOT COMMANDS ----------------------------------------------------------------------------------- #

# bot_command_processor  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# A function that specifically processes through !eb prefixed messages and sorts out respondable prompts from the following line items
# INPUTS:
#       - (DISCORD CLASS) message: the raw input message with metadata and preserved capitalcase
#       - (DISCORD CLASS) command_string: the all-lowercase copy of the original message, specifically to make parsing command strings easier
# OUTPUTS:
#       N/A 
async def bot_command_processor(message, command_string):
    channel = message.channel

    start_0 = 0 
    end_0 = 0 

    status = 0
    response = "There was a problem with your command. Please consult `!eb help` for more information."

    mod = False

    # Check if the user is a moderator/has admit privileges
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
                        if message.content.find("["):
                            # Process message string for bracket notation and filter out inputs
                            new_string = message.content.split("] [")
                            if new_string[0].find(" [") != -1:
                                start_0 = new_string[0].find(" [") + len(" [")
                            else:
                                start_0 = -1
                            end_0 = len(new_string[0])
                            
                            # Make sure there's not a problem with and of the "find"s - aka there was a problem with the input string
                            if start_0 == -1 or end_0 == -1:
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
        elif command_array[1] == "help":
            status, response = await bot_help(message)
        elif command_array[1] == "randomizer":
            status = -1
            response = "This command has not yet been implemented!"

    if status == -1:
        await channel.send(response)




# ----------------------------------------------------------------------------------- !EB BOT COMMANDS #
# ==================================================================================================== #



# ==================================================================================================== #
# ACTIVE DISCORD ASYNC FUNCTIONS --------------------------------------------------------------------- #

# Startup  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_ready():
    # Check and Build New Configuration Files

    print(f'{client.user.name} has connected to Discord!')

# Message detection wrapper  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
@client.event
async def on_message(message):
    # Print debug line to console
    print(f'Message detected: @{message.author} in #{message.channel}: {message.content}\n')

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

        elif formatted_message == 'eb_test':
            output_string = "**[[DEBUG]]**\n------> ..."
            await message.channel.send(output_string)

        elif formatted_message == 'eb_reveal': 
            output_string = "**[[DEBUG]]**\n------> Message metadeta: %s\n\n------> Current channel: %s" % (message, message.channel.id)
            await message.channel.send(output_string)

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
        
        elif formatted_message == 'honque':
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


client.run(TOKEN)
# --------------------------------------------------------------------- ACTIVE DISCORD ASYNC FUNCTIONS #
# ==================================================================================================== #






