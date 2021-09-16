# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image

from io import BytesIO

intents = discord.Intents.default()
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)
bot.delete = 0.0
bot.hat_size = (200, 200)


@bot.command(name='getpfp', help='gets url to your profile picture')
async def getpfp(ctx):
    await ctx.send(ctx.author.avatar_url)


@bot.command(name='hat', help=f'attaches a hat to your avatar. Two optional arguments to specify percent. !hat .5 .5 '
                              f'will put the middle of the hat 50% across, 50% down.')
async def hat(ctx, x: float = 0.0, y: float = 0.0):
    asset = ctx.author.avatar_url_as()
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    width, height = pfp.size
    xmas_hat = Image.open(r'images/christmas_hat.png')
    xmas_hat = xmas_hat.resize(bot.hat_size)
    if x == 0.0:
        #print(f'width: {width / 4.0}\ny: {y}')
        pfp.paste(xmas_hat, (int(width / 4.0), int(y)), mask=xmas_hat)
    else:
        pfp.paste(xmas_hat, (int(float(x) * float(width) - bot.hat_size[0]/2), int(float(y) * float(height) -
                                                                                   bot.hat_size[1]/2)), mask=xmas_hat)
        # pfp.paste(xmas_hat, (int(x), int(y)), mask=xmas_hat)
    pfp.save('images/pfp.png', 'PNG')
    if bot.delete:
        # print('del is num')
        await ctx.send(file=discord.File('images/pfp.png'), delete_after=bot.delete)
    else:
        # print('del is 0.0')
        await ctx.send(file=discord.File('images/pfp.png'))


# stretchy hat
@bot.command(name='resize_stretch', help='resize the hat to x pixels by x pixels')
async def resize_stretch(ctx, x: int, y: int):
    if x == 0 or y == 0:
        await ctx.send('pls don\'t kill hat ):')
        return
    bot.hat_size = (x, y)
    await ctx.send(f'hat size set to {bot.hat_size[0]} by {bot.hat_size[1]}')


# square hat
@bot.command(name='resize_square', help='resize the hat to x pixels by x pixels')
async def resize_square(ctx, x: int):
    if x == 0:
        await ctx.send('pls don\'t kill hat ):')
        return
    bot.hat_size = (x, x)
    await ctx.send(f'hat size set to {bot.hat_size[0]} by {bot.hat_size[0]}')


@bot.command(name='delete_after', help='enter a number \'x\' to delete bot images after x seconds')
async def delete_after(ctx, x: float):
    bot.delete = x
    if bot.delete <= 0.0:
        await ctx.send(f'Images will no longer delete')
    else:
        await ctx.send(f'Images will now delete after {x} seconds')


# error catch
@bot.event
async def on_error(event, *args, **kwargs):
    with open('hatbot_err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for the command.')


bot.run(TOKEN)
