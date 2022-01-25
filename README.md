<div class="header">
  <img align="right" style="display: inline;" src="https://i.imgur.com/QFi1kNw.png" alt="Yakul" />
  <h1 style="display: inline;">EndoBot</h1>
 </div>

A chat-oriented Discord bot built in Python. Designed around the functionality and featureset of other more popular bots, but with more granularity and server-specific features that might be useful for other users!

## Dependencies
Install the following Python dependencies on your system before running EndoBot:
 * `discord.py`
 * `httplib2`
 * `numpy`
 * `oauth2client`
 * `opencv-python`
 * `html2image`
 * `requests`

## Bot Setup
#### IDEs and Hosting the Bot Locally
To host EndoBot locally, first follow the instructions found <a href="https://realpython.com/how-to-make-a-discord-bot-python/">here</a> for how to build and run a Discord bot on your machine. A development environment (IDE) like <a href="https://code.visualstudio.com/">Microsoft Visual Studio Code</a> is recommended if you're planning on running EndoBot on your local machine. 

#### Configuring the Bot for Startup
After receiving a Token from the Discord Developer Portal (as outlined in the tutorial above), navigate to `configuration.ini` and replace the text labeled `YOUR TOKEN HERE` with the bot's Token. 

Pull your server's Guild ID from Discord (process detailed <a href="https://poshbot.readthedocs.io/en/latest/guides/backends/setup-discord-backend/#find-your-guild-id-server-id">here</a>) and replace the text labeled `YOUR GUILD ID HERE` with the Guild ID. (Be sure to leave the brackets!)

Determine which channel you would like to be your Starboard channel, or create a new one. Pull the channel's ID by right-clicking on it and selecting `Copy ID`. Replace the text labeled `YOUR STARBOARD ID HERE` with this channel ID. 

Congratulations! EndoBot will now run.

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/su9T0r3.gif">
</p>
<p>
  
## Current Implementations

#### STARBOARD
 * Frame your favorite posts in a Hall of Fame (or Hall of Shame) based on emoji reactions
 * Customize the reaction emoji and the reaction emoji threshold
 * EndoBot handles updating number of emoji reactions
 * With a custom trigger phrase, EndoBot will repeat a random pinned Starboard message, so you can relive the majesty (or disgrace) all over again
  
<p align="center">
  <img src="https://i.imgur.com/V9YBQI3.png">
</p>

#### LEADERBOARD
 * Want to see who leads the server in most Starboard pins? EndoBot has you covered!
 * Lists all server member's contributions in order from most pinned posts to least pinned posts

<p align="center">
  <img src="https://i.imgur.com/xvH3g2t.png">
</p>

#### TRIGGER PHRASES
 * Set certain words or phrases as triggers to prompt a pre-determined bot reply
 * Configure trigger phrases in-line from Discord

<p align="center">
  <img src="https://i.imgur.com/RtWa2pv.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/9tr7JvQ.png">
</p>

For a complete list of available commands, type `!eb help`.

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/n57XXWN.gif">
</p>
<p>

## Future Implementations

#### EXTERNAL MEDIA QUOTE RANDOMIZER BOT
 * Pull a random line from websites (like AO3) or from files (like ebooks or pdfs) to get an out-of-context quote from that media
#### AUTOMATIC BOT INITIALIZATION
 * Do nothing but run EndoBot from startup for it to initialize itself and set default values.
#### FULL BOT CONFIGURATION THROUGH THE DISCORD CHAT WINDOW
 * Allow moderators to configure the bot directly through Discord - no configuration of ini files required!

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/70nYbRk.gif">
</p>
<p>

## Commands
Please note that upon initial release, some of these functions are not yet operational.

#### TRIGGER PHRASES
These are words or phrases that EndoBot actively searches for and responds to with a pre-configured message.

 * `!eb trigger add [trigger phrase] [bot response] [Message the sender? Yes/No]`: This command adds a trigger phrase and a bot response to the masterlist. The brackets are required!
 * `!eb trigger delete [trigger phrase]`: This command removes a trigger phrase and its bot response from the masterlist.
 * `!eb trigger list`: This command lists all trigger phrases and their subsequent bot responses at once.

#### QUOTE RANDOMIZER BOT
These are commands that allow a user to display a random line or selection from a selected text. Currently supported file formats: N/A
Future supported file formats: .epub, .mobi, AO3.org fanfiction, FFN.net fanfiction

 * `!eb randomizer add [media name] [link]`: This command adds a document or a file to bot memory under a shorthand name, [media name], that can be called upon.
 * `!eb randomizer delete [media name]`: This command removes a saved file from bot memory.
 * `!eb randomizer list`: This command lists all files currently loaded into memory and their associated links/filenames.
 * `!eb randomizer [media name]`: This command selects a random line from the file.

#### BOT CONFIGURATION
These commands allow moderators and server owners to change bot configuration settings without having to manually adjust or change any bot files. WARNING: this can permanently damage bot functionality if not handled correctly.

 * `!eb config`: This command lists all available configuration options and their default/expected values.
 * `!eb config [configuration option] [value]`: This command allows a moderator to change a configuration option. The brackets are required!

#### MISCELLANEOUS COMMANDS
Commands for various random bot features.

 * `!eb leaderboard`: This command displays the currently top-starred users in a server.
 * `!eb help`: This command displays all active commands to the user in-line.

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/9J7FNCU.gif">
</p>
<p>
  
## Support the Bot
If you found any of this useful, I have a tip jar - thank you for your support!
  
<a href='https://ko-fi.com/A704NU8' target='_blank'><img align="center" height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Support me on Ko-Fi!' /></a>
