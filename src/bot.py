from discord.ext import commands
from logger.ownlogger import log


bot = commands.Bot(command_prefix="mt!")  # Create a Bot with Prefix 'mt!'

# If a file token.txt exists: Run the bot. If not: Ask for the token to be stored in the file, and create the file.
try:
    with open('./config/token.txt') as token_file:
        __token__ = token_file.read()

        # Load all the cogs
        bot.load_extension("commands.utility")

        bot.run(__token__)
except FileNotFoundError:

    log("Please enter your Bot Token. It will be stored in './config/token.txt', which is ignored by .gitignore.", 'red')
    # Getting the input as a variable BEFORE creating the file means, that the created file cannot be empty if the program aborts at this point.
    token = input()
    tokenfile = open('./config/token.txt', 'w')
    tokenfile.write(token)
    tokenfile.close()
    log("Token stored. Please restart the bot.")
