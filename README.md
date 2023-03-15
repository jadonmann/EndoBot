<div class="header">
  <img align="right" style="display: inline;" src="https://i.imgur.com/QFi1kNw.png" alt="Yakul" />
  <h1 style="display: inline;">EndoBot</h1>
 </div>

A chat-oriented Discord bot built in Python. Designed around the functionality and featureset of other more popular bots, but with more granularity and server-specific features that might be useful for other users!

## Dependencies
All dependencies for EndoBot are listed in the `requirements.txt` file. If you have pip installed (and you should), run `pip install -r requirements.txt` to install all necessary dependencies to your Python instance. 

## Bot Setup
#### IDEs and Hosting the Bot Locally
To host EndoBot locally, first follow the instructions found <a href="https://realpython.com/how-to-make-a-discord-bot-python/">here</a> for how to build and run a Discord bot on your machine. A development environment (IDE) like <a href="https://code.visualstudio.com/">Microsoft Visual Studio Code</a> is recommended if you're planning on running EndoBot on your local machine. 

#### Configuring the Bot for Startup
After receiving a Token from the Discord Developer Portal (as outlined in the tutorial above), open the file called `token.txt` and paste the token inside. Save the file and close it; EndoBot will take care of the rest. 

Congratulations! EndoBot will now run. On first start-up, EndoBot will acquire your server's ID, #general channel, and other basic information in order to build an internal directory for your server. Note that by default, all automated server communications that the bot will generate will use your #general (or equivalent) channel to do so. You can change the output channel for each EndoBot feature by running the `!eb config` command within your server with moderator privileges.

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
 * With a custom trigger phrase, EndoBot will repeat a random pinned Starboard message, so you can relive the majesty (or disgrace) all over again:
  
<p align="center">
  <img src="https://i.imgur.com/V9YBQI3.png">
</p>

#### LEADERBOARD
 * Want to see who leads the server in most Starboard pins? EndoBot has you covered!
 * Lists all server member's contributions in order from most pinned posts to least pinned posts:

<p align="center">
  <img src="https://i.imgur.com/xvH3g2t.png">
</p>

#### TRIGGER PHRASES
 * Set certain words or phrases as triggers to prompt a pre-determined bot reply
 * Configure trigger phrases in-line from Discord
 * List all current commands in one place using `!eb trigger list`

<p align="center">
  <img src="https://i.imgur.com/RtWa2pv.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/9cPNsCj.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/9tr7JvQ.png">
</p>

#### SPRINTO SPRINTBOT SCOREKEEPER
 * Works with <a href="https://discord.bots.gg/bots/421646775749967872">Sprinto</a>, a popular writing sprint bot
 * Keeps track of your words written during sprints
 * Logs words written per day, per week, per month, per year, and all-time
 * View who has sprinted the most in your server over time in a yearly leaderboard

<p align="center">
  <img src="https://i.imgur.com/iBoFtNU.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/iS8nhM3.png">
</p>

#### NANOWRIMO SCOREKEEPER
 * Want to run a NaNoWriMo (National Novel Writing Month) challenge with a specific word count goal for the month? EndoBot has got you covered
 * Set whatever word count you'd like - the challenge will run to the end of the current calendar month
 * View current completion percentage, words to write per day to meet the deadline, and current number of words written that month

<p align="center">
  <img src="https://i.imgur.com/3LphWso.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/JJorHZO.png">
</p>

#### NYT DAILY SPELLING BEE
 * An optional feature that pulls the day's NYT Spelling Bee puzzle and displays it in-chat
 * Displays solutions behind a spoiler tag so you can check your work

<p align="center">
  <img src="https://i.imgur.com/P30hMZF.png">
</p>

#### DAILY MESSAGES
 * A highly-customizable daily announcements bulletin that compiles sprint totals, NaNoWriMo leaderboards, and the NYT Spelling Bee into one post
 * Post can be scheduled at any time during the day
 * Including the NYT Spelling Bee in the daily messages also includes a link to the day's Wordle, Quordle, and Weaver
 * Can be set to only post whenever there are updates to the daily sprint totals/NaNoWriMo leaderboards

<p align="center">
  <img src="https://i.imgur.com/y6MlzJ3.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/xXdExPq.png">
</p>

#### CONFIGURATION EDITOR
 * View, edit, and reconfigure EndoBot's settings for your server without hard-rebooting the bot

<p align="center">
  <img src="https://i.imgur.com/52e4DMZ.png">
</p>
<p align="center">
  <img src="https://i.imgur.com/EXqrhva.png">
</p>

#### EXTERNAL MEDIA PARSER (EXPERIMENTAL)
 * Pulls a random quote from AO3 and reads it back

<p align="center">
  <img src="https://i.imgur.com/W28gj7a.png">
</p>

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/n57XXWN.gif">
</p>
<p>

## Full Commands List
 * To view the full list of commands at any time while using Discord, type `!eb help`
 * Some commands require moderator privileges, or require brackets to be used within the command itself in order for the bot to read more nuanced messages with spaces or other delimiters. The following image lists the restrictions or requirements for each command:

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/VIqJ3XH.png">
</p>
<p>

#### TRIGGER PHRASES
These are words or phrases that EndoBot actively searches for and responds to with a pre-configured message.

 * `!eb trigger add [trigger phrase] [bot response] [Message the sender? Yes/No]`: This command adds a trigger phrase and a bot response to the masterlist. The brackets are required!
 * `!eb trigger delete [trigger phrase]`: This command removes a trigger phrase and its bot response from the masterlist. Requires brackets.
 * `!eb trigger list`: This command lists all trigger phrases and their subsequent bot responses at once.
  
#### SPRINT STATS
These are commands that can be used to view, change, or force an update to sprint stats.
  
 * `!eb sprintstats edit [+/-value] [Discord ID or @]`: change the total sprint number for a user. Requires brackets.
 * `!eb sprintstats forceupdate`: Forces the bot to reset the daily counter and "begin" a new day. (Primarily used for debugging)
 * `!eb sprintstats leaderboard`: View the current sprint stats leaderboard.
  
#### NANOWRIMO
These commands allow a user to join, leave, create, or disable a monthly NaNoWriMo competition, as well as view current leaderboards.
  
 * `!eb nanowrimo enable`: Enables a NaNoWriMo competition. Must be done before joining!
 * `!eb nanowrimo disable`: Disables the current NaNoWriMo competition. Requires moderator permissions.
 * `!eb nanowrimo enroll [number]`: Enrolls the user in the current NaNoWriMo competition with a specified word count goal. Brackets not required!
 * `!eb nanowrimo withdraw`: Withdraws the user from the current NaNoWriMo competition.
 * `!eb nanowrimo check`: Checks to see what the user's NaNoWriMo word count goal is set to, if they are enrolled in the current NaNoWrimo competition.
 * `!eb nanowrimo leaderboard`: Displays the current NaNoWriMo leaderboard.

#### QUOTE RANDOMIZER BOT
These are commands that allow a user to display a random line or selection from a selected text. Currently supported sites: AO3
 * `!eb randomizer [media link]`: This command selects a random line from the file. Does not require brackets.

#### BOT CONFIGURATION
These commands allow moderators and server owners to change bot configuration settings without having to manually adjust or change any bot files. WARNING: this can permanently damage bot functionality if not handled correctly.

 * `!eb config`: This command lists all available configuration options and their default/expected values.
 * `!eb config [configuration option] [value]`: This command allows a moderator to change a configuration option. Requires brackets.

#### MISCELLANEOUS COMMANDS
Commands for various random bot features.

 * `!eb leaderboard`: This command displays the currently top-starred users in a server.
 * `!eb spellingbee`: This command displays the current day's NYT spelling bee and solutions.
 * `!eb help`: This command displays all active commands to the user in-line.
 * `!eb welcome`: This command reposts the initial welcome message that is generated upon joining a new server.
 * `!eb admin forcemorningmessages`: This command forces the morning messages, which is critical for daily sprint count rollovers.
 * `!eb reboot`: This command reboots EndoBot.

<p>
<p align="center">
  <img width="498" src="https://i.imgur.com/9J7FNCU.gif">
</p>
<p>
  
## Support the Bot
If you found any of this useful, I have a tip jar - thank you for your support!
  
<a href='https://ko-fi.com/A704NU8' target='_blank'><img align="center" height='36' style='border:0px;height:36px;' src='https://cdn.ko-fi.com/cdn/kofi1.png?v=3' border='0' alt='Support me on Ko-Fi!' /></a>
