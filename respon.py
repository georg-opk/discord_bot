import discord
from discord.ext import commands,tasks
import os
import youtube_dl
# Get the API token from the .env file.
DISCORD_TOKEN = "OTU1Njc5ODAzMzAwNzk4NDc3.YjlMLA.MRlbTKoYsVVKA6A9ZsoSfkAcLlw"
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='-',intents=intents)
#music - start
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
@bot.event
async def on_ready():
    print("updated and ready")
@bot.command(name='join', help='присоединяется к voice канналу, в котором находится пользователь')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} я не присоединён к каналу".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
@bot.command(name='leave', help='отключает бота от каннала')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("Данный бот не был присоеденён к канналу")


@bot.command(name='play', help='играет песню из ссылки youtube которую прикрепил пользователь')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**сейчас играет** {}'.format(filename))
    except:
        await ctx.send("бот не подключён к канналу")


@bot.command(name='pause', help='ставит песню на паузу')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("бот ничего не играет")


@bot.command(name='resume', help='возобновляет песню')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")


@bot.command(name='stop', help='останавливает песню и удаляет её из очереди')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("бот ничего не играет")
#music end



# moderation - start
@bot.command(name='ping', help='Проверка подключения бота к серверу')
async def ping(ctx):
    await ctx.reply('Бот подключён!')


@bot.command(name='stop_bot', help='Доступно только создателю. Принудительная остановка бота')
async def stop_bot(ctx):
    await ctx.reply("Бот был остановлен")
    exit(0)


# МОДЕРАЦИЯ
@bot.command(name='mute', help='Запретить писать участнику')  # КОМАНДА НЕ ГОТОВА
@commands.has_any_role(962779141457997844, 962779845455142912)
async def mute(ctx, member, during, reason=''):
    if reason is not None:
        await ctx.reply(f"{member} был замучен на {during} по причине: {reason}")
    else:
        await ctx.reply(f"{member} был замучен на {during}")


@bot.command(name='unmute', help='Разрешить писать участнику')  # КОМАНДА НЕ ГОТОВА
@commands.has_any_role(962779141457997844, 962779845455142912)
async def unmute(ctx, member):
    await ctx.reply(f"{member} был размучен")


@bot.command(name='kick', help='Выгнать участника')  # КОМАНДА НЕ ГОТОВА
@commands.has_any_role(962779141457997844, 962779845455142912)
async def kick(ctx, member, reason=''):
    if reason is not None:
        await ctx.reply(f"{member} был изгнан по причине: {reason}")
    else:
        await ctx.reply(f"{member} был изгнан")


@bot.command(name='bun', help='Забанить участника')  # КОМАНДА НЕ ГОТОВА
@commands.has_any_role(962779141457997844, 962779845455142912)
async def bun(ctx, member, during, reason=''):
    await ctx.reply(f"{member} был забанен на {during} по причине: {reason}")


@bot.command(name='unbun', help='Разбанить участника')  # КОМАНДА НЕ ГОТОВА
@commands.has_any_role(962779141457997844, 962779845455142912)
async def unbun(ctx, member):
    await ctx.reply(f"{member} был разбанен")


# КРАШ КОМАНДЫ
@bot.command(name='flood', help='Команда для циклической отправки однотипных сообщений')
async def flood(ctx, number_of_repetitions, *message):
    s = ''
    number_of_repetitions = int(number_of_repetitions)
    for i in message:
        s = s + i + " "
    while number_of_repetitions > 0:
        await ctx.send(s)
        number_of_repetitions -= 1
if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)