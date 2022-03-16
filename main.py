from datetime import datetime
from discord.ext import commands, tasks
import auth
import discord
import trakt

global ctx
global media_type

NAME = 'Your Discord App Name'
COMMAND_PREFIXES = ['tb ', 'tB ', 'Tb ', 'TB ']
CLEAR_COMMAND_ALIASES = ['clear', 'erase']
TREND_COMMAND_ALIASES = ['trend', 'trends', 'trending']
STOP_COMMAND_ALIASES = ['stop', 'break']

client = commands.Bot(command_prefix=COMMAND_PREFIXES, case_insensitive=True)
client.remove_command('help')


# Notifies user that the discord bot is online
@client.event
async def on_ready():
    print(f'{NAME} online')


# Clear a specified amount of messages from a channel
@client.command(aliases=CLEAR_COMMAND_ALIASES)
async def _clear(context, amount=5):
    await context.channel.purge(limit=amount)


# Custom help command
@client.command(aliases=['help', 'about'])
async def _help(context):
    embed = discord.Embed(
        title=f"{NAME} Help Menu",
        color=discord.Colour.orange()
    )
    embed.add_field(
        name='clear',
        value="Removes unwanted messages from the channel\n`tb clear <number of posts>`",
        inline=False
    )
    embed.add_field(name='help', value="Guide to use this bot\n`tb help`", inline=False)
    embed.add_field(
        name='trend',
        value="Displays trending movies and shows from trakt api automatically:\n"
              + "`tb trend movies 60`\n\n"
              + "For trending movies:\n"
              + "`tb trend movies <seconds between posts>`\n"
              + "For trending shows:\n"
              + "`tb trend shows <seconds between posts>`\n",
        inline=False
    )
    embed.add_field(name='stop', value="Stops automatic posting\n`tb stop`", inline=False)
    embed.set_footer(text=f"Created by: Leon De Montana")
    await context.send(embed=embed)


# Posts top 10 trending shows or movies for a specified location
@client.command(aliases=TREND_COMMAND_ALIASES)
async def _trend(context, *, option='movies 60'):
    try:
        global ctx
        global media_type
        ctx = context
        options = option.lower().split(' ')
        media_type = options[0].lower()
        post_trending.change_interval(seconds=int(options[1].strip()))
        post_trending.start()
    except Exception as e:
        await context.send('Something went wrong. Check your command and try again.')


# Runs a background task that posts trending data at a specified time interval
@tasks.loop(seconds=10)
async def post_trending():
    global ctx
    global media_type
    trending = trakt.get_trakt_trending(media_type)
    embed = create_trend_embed(trending)
    await ctx.send(embed=embed)


# Cancels the trend background task
@client.command(aliases=STOP_COMMAND_ALIASES)
async def _stop(context):
    post_trending.cancel()
    await context.send(f'{NAME} will discontinue automatic posting')


# Creates discord embed message to be sent
def create_trend_embed(post):
    global media_type
    dt = datetime.now().strftime('%Y-%m-%d %I:%M %p').split(' ')
    embed = discord.Embed(
        title=f"TraktTV Trending {media_type.title()}",
        description=post,
        color=discord.Colour.orange()
    )
    embed.set_footer(text=f"{dt[0]} at {dt[1]} {dt[2]}")
    return embed


client.run(auth.DISCORD_TOKEN)