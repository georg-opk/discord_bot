from sqlalchemy import MetaData
import sqlalchemy
import discord
from discord.ext import commands, tasks
import youtube_dl
from datetime import datetime
import asyncio
from random import choice

DISCORD_TOKEN = "OTU1Njc5ODAzMzAwNzk4NDc3.YjlMLA.aj88Fc6vhlBWdApqwiQXmV8ZU_Y"
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='-', intents=intents)
youtube_dl.utils.bug_reports_message = lambda: ''


def merge(message):
    s = ''

    for i in message:
        s += i + ' '

    return s


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
    'source_address': '0.0.0.0'
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
    giff = ['Bon_jiorno', 'cowboy bepop', 'hellsing', 'minion', 'ora', 'reich']
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "test1":
                ember = discord.Embed(title='Состояние')
                ember.add_field(name='состояние бота', value='Бот активирован!!')
                ember.add_field(name='Привествую пользователей!', value='HELLO!')
                await channel.send(embed=ember)
                await channel.send(file=discord.File(choice(giff) + '.gif'))
        print('Active in {}\n Member Count : {}'.format(guild.name, guild.member_count))


class social_interact(commands.Cog):
    """данные команды предназначены для взаимодействий с пользователями"""

    def __init__(self, bot):
        self.bot = bot

    @bot.command(help="Prints details of Server")
    @commands.has_permissions(administrator=True)
    async def where_am_i(ctx):
        owner = str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc = ctx.guild.description

        embed = discord.Embed(
            title=ctx.guild.name + " Server Information",
            description=desc,
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=guild_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=memberCount, inline=True)
        await ctx.send(embed=embed)
        members = []
        async for member in ctx.guild.fetch_members(limit=150):
            await ctx.send(
                'Name : {}\t Status : {}\n Joined at {}'.format("@" + member.display_name, str(member.status),
                                                                str(member.joined_at)))

    @bot.command()
    async def tell_me_about_yourself(ctx):
        text = ""
        await ctx.send(text)

    # moderation - start

    @bot.command(name='ping', help='Проверка подключения бота к серверу')
    @commands.has_permissions(administrator=True)
    async def ping(ctx):
        embed = discord.Embed(title='Состояние бота')
        embed.add_field(name='Состояние', value='Бот подключён!')
        await ctx.send(embed=embed)

    @bot.command(name='stop_bot', help='Доступно только создателю. Принудительная остановка бота')
    @commands.has_permissions(administrator=True)
    @commands.is_owner()
    async def stop_bot(ctx):
        voice_client = ctx.message.guild.voice_client
        try:
            if voice_client.is_connected():
                await voice_client.disconnect()
            embed = discord.Embed(title='Состояние бота')
            embed.add_field(name='Состояние', value='Бот был останвлён!')
            await ctx.send(embed=embed)
            exit(0)
        except:
            embed = discord.Embed(title='Состояние бота')
            embed.add_field(name='Состояние', value='Бот был останвлён!')
            await ctx.send(embed=embed)
            exit(0)

    @bot.command(name='kick', help='Выгнать участника')
    @commands.has_permissions(administrator=True)
    async def kick(ctx, member: discord.Member, *reason):
        if len(reason) > 0:
            await member.send(f"Вы были кикнуты по причине: {merge(reason)}")
            await ctx.reply(f"{member} был кикнут по причине: {merge(reason)}")
        else:
            await member.send(f"Вы были кикнуты")
            await ctx.reply(f"{member} был кикнут")
        await member.kick(reason=merge(reason))

    @bot.command(name='ban', help='Забанить участника')
    @commands.has_permissions(administrator=True)
    async def ban(ctx, member: discord.Member, *reason):
        if len(reason) > 0:
            await ctx.reply(f"{member} был забанен по причине: {merge(reason)}")
            try:
                await member.send(f"Вы были забанены по причине: {merge(reason)}")
            except:
                pass
        else:
            try:
                await member.send(f"Вы были забанены")
            except:
                pass
            await ctx.reply(f"{member} был забанен")
        await member.ban(reason=merge(reason))

    @bot.command(name='unban', help='Разбанить участника через ID')
    @commands.has_permissions(administrator=True)
    async def unban(ctx, id):
        id = int(id)
        user = await bot.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.reply(f"Был разбанен")

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(ctx, member: discord.Member = None, amout: str = None, *, reason=None):
        times_start = datetime.today()
        emb_user = discord.Embed(title='**Уведомление - Mute**')
        emb_user.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
        emb_user.add_field(name='**Причина:**', value=reason, inline=False)
        emb_user.add_field(name='**Длительность:**', value=amout, inline=False)
        emb_user.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
        emb_user.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        emb_user_stop = discord.Embed(title='**Уведомление - Unmute**')
        emb_user_stop.add_field(name='**Снял:**', value=ctx.author.mention, inline=False)
        emb_user_stop.add_field(name='**Сервер:**', value=ctx.guild.name, inline=False)
        emb_user_stop.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        mute_role = discord.utils.get(ctx.message.guild.roles, id=964590670369153064)

        if member is None:
            emb = discord.Embed(title='[ERROR] Mute', description=f'{ctx.author.mention}, Укажите пользователя!')
            emb.add_field(name='Пример:', value=f'-mute [@участник] <время(с, м, ч, д)> [причина]',
                          inline=False)
            emb.add_field(name='Пример 1:', value=f'-mute @Xpeawey 1ч пример')
            emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

            await ctx.send(embed=emb)
        else:
            end_time = amout[-1:]
            time = int(amout[:-1])
            if time <= 0:
                emb = discord.Embed(title='[ERROR] Mute',
                                    description=f'{ctx.author.mention}, Время не может быть меньше 1!')
                emb.add_field(name='Пример:', value=f'-mute [@участник] <время> [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'-mute @Xpeawey 1ч пример')
                emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

                await ctx.send(embed=emb)
            else:
                if end_time == 'с':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                elif end_time == 'м':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value='Не указано', inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                elif end_time == 'ч':
                    if reason is None:
                        if time == '1':

                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                            emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                            emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                            emb.add_field(name='Причина:', value='Не указано', inline=False)
                            emb.add_field(name='Длительность:', value='{} час'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.send(embed=emb)
                            await member.send(embed=emb_user)
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                        elif time == '4' or time == '3' or time == '2':
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                            emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.send(embed=emb)
                            await member.send(embed=emb_user)
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                        elif time >= '5':
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:', value=member.id, inline=False)
                            emb.add_field(name='**Причина:', value='Не указано', inline=False)
                            emb.add_field(name='**Длительность:', value='{} часов'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.send(embed=emb)
                            await member.send(embed=emb_user)
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                    else:
                        if time == '1':
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value=reason, inline=False)
                            emb.add_field(name='**Длительность:**', value='{} час'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.send(embed=emb)
                            await member.send(embed=emb_user)
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                        elif time == '4' or time == '3' or time == '2':
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value=reason, inline=False)
                            emb.add_field(name='**Длительность:**', value='{} часа'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.send(embed=emb)
                            await member.send(embed=emb_user)
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                        elif time >= '5':
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value=reason, inline=False)
                            emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                            await member.add_roles(mute_role)
                            await ctx.send(embed=emb)
                            await member.send(embed=emb_user)
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            await member.send(embed=emb_user_stop)
                elif time == 'д':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        await member.send(embed=emb_user)
                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)
                    else:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time), inline=False)
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        await member.add_roles(mute_role)
                        await ctx.send(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.remove_roles(mute_role)
                        await member.send(embed=emb_user_stop)


class music(commands.Cog):
    """данные команды предназначены для взаимодействий с музыкой, которую воспроизводит бот"""

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='join', help='присоединяется к voice канналу, в котором находится пользователь')
    async def join(ctx):
        if not ctx.message.author.voice:
            await ctx.send("{} я не присоединён к каналу".format(ctx.message.author.name))
            return
        else:
            channel = ctx.message.author.voice.channel
            await ctx.send("Присоединение прошло успешно")
        await channel.connect()

    @bot.command(name='leave', help='отключает бота от каннала')
    async def leave(ctx):
        try:
            leav = ['Отключаюсь', "я работать?", "Всем пока", "Я устал, я ухожу", "всем до скорого!", "Adios"]
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected():
                await voice_client.disconnect()
                await ctx.send(choice(leav))
            else:
                await ctx.send("Данный бот не был присоеденён к канналу")
        except:
            await ctx.send("Данный бот не был присоеденён к канналу")

    @bot.command(name='play', help='играет песню из ссылки youtube которую прикрепил пользователь')
    async def play(ctx, url):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            embedVar = discord.Embed(title="music", )
            embedVar.add_field(name="**сейчас играет**", value=filename, inline=False)
            await ctx.send(embed=embedVar)
        except:
            await ctx.send("бот не подключён к канналу")

    @bot.command(name='playlist', help='играет плейлист ссылок')
    async def playlist(ctx, *url):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            for urls in url:
                async with ctx.typing():
                    filename = await YTDLSource.from_url(urls, loop=bot.loop)
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
                embedVar = discord.Embed(title="music", )
                embedVar.add_field(name="**сейчас играет**", value=filename, inline=False)
                await ctx.send(embed=embedVar)
                while ctx.message.guild.voice_client.is_playing() or ctx.message.guild.voice_client.is_paused():
                    await asyncio.sleep(3)
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
            await ctx.send("Бот ничего не играл")

    @bot.command(name='stop', help='останавливает песню и удаляет очередь')
    async def stop(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()

        else:
            await ctx.send("бот ничего не играет")

    @bot.command(name='skip', help='останавливает песню и удаляет её из очереди')
    async def skip(ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("бот ничего не играет")


##@bot.event
##async def on_message(ctx):
##    channel = bot.get_channel(962780544490438666)
##    if ctx.channel == channel and not ctx.author.bot:
##        print(ctx.author)


# КРАШ КОМАНДЫ
@bot.command(name='flood', help='Команда для циклической отправки однотипных сообщений')
@commands.is_owner()
async def flood(ctx, number_of_repetitions, *message):
    s = ''
    number_of_repetitions = int(number_of_repetitions)
    for i in message:
        s = s + i + " "
    while number_of_repetitions > 0:
        await ctx.send(s)
        number_of_repetitions -= 1


@bot.command(name='rename_channels', help='Переименовывает все каналы в заданное название(название канала в кавычках)')
@commands.is_owner()
async def ran_channels(ctx, channel: discord.VoiceChannel, *, new_name):
    await channel.edit(name=new_name)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
