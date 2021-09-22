# bot.py
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from PIL import Image
from PIL import ImageOps

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
bot.flip = False
bot.rotate = 0


@bot.command(name='getpfp', help='gets url to your profile picture')
async def getpfp(ctx):
    asset = ctx.author.avatar_url_as()
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    await ctx.send(ctx.author.avatar_url)
    width, height = pfp.size
    await ctx.send(f'Your hat is {width} by {height}')


@bot.command(name='xmashat')
async def xmashat(ctx, x: float, y: float):
    await hat(ctx, x, y, 'xmashat')


@bot.command(name='witchhat')
async def witchhat(ctx, x: float, y: float):
    await hat(ctx, x, y, 'witchhat')


@bot.command(name='sunglasses')
async def sunglasses(ctx, x: float, y: float):
    await hat(ctx, x, y, 'sunglasses')


@bot.command(name='hat', help=f'attaches a hat to your avatar. Two optional arguments to specify percent. !hat .5 .5 '
                              f'will put the middle of the hat 50% across, 50% down.')
async def hat(ctx, x: float = 0.0, y: float = 0.0, hattype: str = 'xmashat'):
    asset = ctx.author.avatar_url_as()
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    width, height = pfp.size
    hat_image = Image.open(fr'images/{hattype}.png')
    hat_image = hat_image.resize(bot.hat_size)
    if bot.flip:
        hat_image = ImageOps.mirror(hat_image)
    if bot.rotate:
        hat_image = hat_image.rotate(bot.rotate)
    if x == 0.0:
        #print(f'width: {width / 4.0}\ny: {y}')
        pfp.paste(hat_image, (int(width / 4.0), int(y)), mask=hat_image)
    else:
        pfp.paste(hat_image, (int(float(x) * float(width) - bot.hat_size[0] / 2), int(float(y) * float(height) -
                                                                                      bot.hat_size[1] / 2)), mask=hat_image)
        # pfp.paste(hat_image, (int(x), int(y)), mask=hat_image)
    pfp.save('images/pfp.png', 'PNG')
    if bot.delete:
        # print('del is num')
        await ctx.send(file=discord.File('images/pfp.png'), delete_after=bot.delete)
    else:
        # print('del is 0.0')
        await ctx.send(file=discord.File('images/pfp.png'))


# stretchy hat
@bot.command(name='resize_stretch', help='resize the hat to x pixels by y pixels')
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


@bot.command(name='flip', help='flips hat horizontally')
async def flip(ctx):
    bot.flip = not bot.flip
    await ctx.send(f'Flipped hat')


@bot.command(name='rotate', help='rotate hat x degrees')
async def rotate(ctx, x: int):
    bot.rotate = x
    await ctx.send(f'Rotated image {bot.rotate} degrees')


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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        arg = error.param.name
        await ctx.send(f'Missing argument: {arg}')


@bot.listen('on_message')
async def v(message):
    if not message.author.bot and message.content == 'v':
        await message.channel.send('YOU SUCK AT PASTE')


bot.run(TOKEN)
