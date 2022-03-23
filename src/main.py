from unicodedata import name
from discord.ext import commands

bot = commands.Bot(command_prefix="mt!")

# Decorator, that converts below defined function into a "discord"-Command


@bot.command(name="hello")
# Setting the name-Attr is optional, as per default, the command will inherit its' name from the function name, if no name has been defined.
# Defines function that takes ctx-Argument, which is a Context object, passed with EVERY command.
async def hello_world(ctx: commands.Context):
    # Makes an API Call to Discord to send a mesage to the channel the command was run in with the message content.
    await ctx.send("Hello, world :)")
    # For all intents and purposes, ctx.send() and ctx.channel.send() function exactly the same, with the first option simply being more concise.

try:
    with open('./config/token.txt') as token_file:
        __token__ = token_file.read()
        bot.run(__token__)
except FileNotFoundError:
    print("Please enter your Bot Token. It will be stored in './config/token.txt', which is ignored by .gitignore.")
    __tokenfile__ = open('./config/token.txt', 'x')
    __tokenfile__.write(input())
    print("Token stored. You can now restart the bot.")
