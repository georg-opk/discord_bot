import random
import discord
from discord.ext import commands, tasks
import youtube_dl
from datetime import datetime
import asyncio
from random import choice
import requests
###### DELETE
###### DELETE
###### DELETE
###### DELETE
DISCORD_TOKEN = "delete_OTU1Njc5ODAzMzAwNzk4NDc3._delete_YjlMLA.oa3O2hSlEKmY4yysF4v93u-0RuE_delete"
###### DELETE
###### DELETE
###### DELETE
###### DELETE
###### DELETE
intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='-', intents=intents)
youtube_dl.utils.bug_reports_message = lambda: ''


def merge(message):
    str = ''

    for i in message:
        str += i + ' '

    return str


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
@bot.event
async def on_ready():
    help_command = commands.DefaultHelpCommand(No_Category='Commands')
    giff = ['Bon_jiorno', 'cowboy bepop', 'hellsing', 'minion', 'ora', 'reich']
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if str(channel) == "test1":
                ember = discord.Embed(title='Состояние')
                ember.add_field(name='Состояние бота:', value='Бот активирован!')
                ember.add_field(name='Привествую пользователей!', value='HELLO!')
                await channel.send(embed=ember)
                await channel.send(file=discord.File(choice(giff) + '.gif'))
        print('Подключён к {}\n Количество участников : {}'.format(guild.name, guild.member_count))


class social_interact(commands.Cog):
    """Данные команды предназначены для взаимодействий с пользователями"""

    def __init__(self, bot):
        self.bot = bot

    @bot.command(help="Статистика сервера")
    @commands.has_permissions(administrator=True)
    async def server(ctx):
        owner = str(ctx.guild.owner)
        region = str(ctx.guild.region)
        guild_id = str(ctx.guild.id)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        desc = " *Информация о сервере*"
        embed = discord.Embed(
            title=ctx.guild.name, description=desc)
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Создатель:", value=owner, inline=True)
        embed.add_field(name="ID сервера:", value=guild_id, inline=True)
        embed.add_field(name="Регион:", value=region, inline=True)
        embed.add_field(name="Количество участников:", value=memberCount, inline=True)
        await ctx.send(embed=embed)
        members = []
        async for member in ctx.guild.fetch_members(limit=150):
            await ctx.send(
                'Ник : {}\t Зашёл {}'.format(member.display_name, str(member.joined_at)))

    @bot.command(help="Краткая информация о боте")
    async def about_me(ctx):
        # оформить в виде вложения
        text = "Создан пользователями cascader13#2153 и Georg_opk#1488"
        embed = discord.Embed(title="Я бот", description=f"{text}")
        await ctx.reply(embed=embed)

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
            await ctx.reply(embed=embed)
            exit(0)
        except:
            embed = discord.Embed(title='Состояние бота')
            embed.add_field(name='Состояние', value='Бот был останвлён!')
            await ctx.reply(embed=embed)
            exit(0)

    @bot.command(name='kick', help='Выгоняет участника с сервера')
    @commands.has_permissions(administrator=True)
    async def kick(ctx, member: discord.Member, *reason):
        times_start = datetime.today()

        if len(reason) > 0:
            emb = discord.Embed(title=f'**Кик**')
            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
            emb.add_field(name='**Причина:**', value=merge(reason), inline=False)
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await member.send(embed=emb)
            await ctx.reply(embed=emb)
        else:
            emb = discord.Embed(title=f'** Кик **')
            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await member.send(embed=emb)
            await ctx.reply(embed=emb)

        await member.kick(reason=merge(reason))

    @bot.command(name='ban', help='Банит участника сервера')
    @commands.has_permissions(administrator=True)
    async def ban(ctx, member: discord.Member, *reason):
        times_start = datetime.today()

        if len(reason) > 0:
            emb = discord.Embed(title=f'**Бан**')
            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
            emb.add_field(name='**Причина:**', value=merge(reason), inline=False)
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await ctx.reply(embed=emb)
            try:
                await member.send(embed=emb)
            except:
                pass
        else:
            emb = discord.Embed(title=f'** Бан **')
            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await ctx.reply(embed=emb)
            try:
                await member.send(embed=emb)
            except:
                pass

        await member.ban(reason=merge(reason))

    @bot.command(name='unban', help='Разбанить участника через ID')
    @commands.has_permissions(administrator=True)
    async def unban(ctx, id):
        times_start = datetime.today()
        emb = discord.Embed(title=f'**Разбан**')
        emb.add_field(name='Действие:', value='Участник был разбанен', inline=False)
        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        id = int(id)
        user = await bot.fetch_user(id)

        await ctx.guild.unban(user)
        await ctx.reply(embed=emb)

    @bot.command(help="Котики")
    async def cat(ctx):
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        await ctx.reply(response.json()[0]["url"])

    @bot.command(help="Пёсики")
    async def dog(ctx):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        await ctx.reply(response.json()["message"])

    @bot.command(help="Запрещает пользователю писать сообщение")
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

            await ctx.reply(embed=emb)
        else:
            end_time = amout[-1:]
            time = int(amout[:-1])
            if time <= 0:
                emb = discord.Embed(title='[ERROR] Mute',
                                    description=f'{ctx.author.mention}, Время не может быть меньше 1!')
                emb.add_field(name='Пример:', value=f'-mute [@участник] <время> [причина]', inline=False)
                emb.add_field(name='Пример 1:', value=f'-mute @Xpeawey 1ч пример')
                emb.add_field(name='Время:', value=f'с - секунды\nм - минуты\nч - часы\nд - дни')

                await ctx.reply(embed=emb)
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
                        await ctx.reply(embed=emb)
                        try:
                            await member.send(embed=emb_user)
                        except:
                            pass
                        await asyncio.sleep(time)
                        await member.remove_roles(mute_role)
                        try:
                            await member.send(embed=emb_user_stop)
                        except:
                            pass
                    else:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} секунд'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.reply(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time)
                        await member.remove_roles(mute_role)
                        try:
                            await member.send(embed=emb_user_stop)
                        except:
                            pass
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
                        await ctx.reply(embed=emb)
                        try:
                            await member.send(embed=emb_user)
                        except:
                            pass
                        await asyncio.sleep(time * 60)
                        await member.remove_roles(mute_role)
                        try:
                            await member.send(embed=emb_user_stop)
                        except:
                            pass
                    else:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                        emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                        emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                        emb.add_field(name='Причина:', value=reason, inline=False)
                        emb.add_field(name='Длительность:', value='{} минут'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                        await member.add_roles(mute_role)
                        await ctx.reply(embed=emb)
                        try:
                            await member.send(embed=emb_user)
                        except:
                            pass
                        await asyncio.sleep(time * 60)
                        await member.remove_roles(mute_role)
                        try:
                            await member.send(embed=emb_user_stop)
                        except:
                            pass
                elif end_time == 'ч':
                    if reason is None:
                        if time == 1:
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='Выдал:', value=ctx.author.mention, inline=False)
                            emb.add_field(name='Нарушитель:', value=member.mention, inline=False)
                            emb.add_field(name='ID нарушителя:', value=member.id, inline=False)
                            emb.add_field(name='Причина:', value='Не указано', inline=False)
                            emb.add_field(name='Длительность:', value='{} час'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.reply(embed=emb)
                            try:
                                await member.send(embed=emb_user)
                            except:
                                pass
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            try:
                                await member.send(embed=emb_user_stop)
                            except:
                                pass
                        elif time == 4 or time == 3 or time == 2:
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                            emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.reply(embed=emb)
                            try:
                                await member.send(embed=emb_user)
                            except:
                                pass
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            try:
                                await member.send(embed=emb_user_stop)
                            except:
                                pass
                        elif time >= 5:
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:', value=member.id, inline=False)
                            emb.add_field(name='**Причина:', value='Не указано', inline=False)
                            emb.add_field(name='**Длительность:', value='{} часов'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.reply(embed=emb)
                            try:
                                await member.send(embed=emb_user)
                            except:
                                pass
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            try:
                                await member.send(embed=emb_user_stop)
                            except:
                                pass
                    else:
                        if time == 1:
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value=reason, inline=False)
                            emb.add_field(name='**Длительность:**', value='{} час'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.reply(embed=emb)
                            try:
                                await member.send(embed=emb_user)
                            except:
                                pass
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            try:
                                await member.send(embed=emb_user_stop)
                            except:
                                pass
                        elif time == 4 or time == 3 or time == 2:
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value=reason, inline=False)
                            emb.add_field(name='**Длительность:**', value='{} часа'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                            await member.add_roles(mute_role)
                            await ctx.reply(embed=emb)
                            try:
                                await member.send(embed=emb_user)
                            except:
                                pass
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            try:
                                await member.send(embed=emb_user_stop)
                            except:
                                pass
                        elif time >= 5:
                            emb = discord.Embed(title=f'**System - Mute**')
                            emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                            emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                            emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                            emb.add_field(name='**Причина:**', value=reason, inline=False)
                            emb.add_field(name='**Длительность:**', value='{} часов'.format(time))
                            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                            await member.add_roles(mute_role)
                            await ctx.reply(embed=emb)
                            try:
                                await member.send(embed=emb_user)
                            except:
                                pass
                            await asyncio.sleep(time * 60 * 60)
                            await member.remove_roles(mute_role)
                            try:
                                await member.send(embed=emb_user_stop)
                            except:
                                pass
                elif time == 'д':
                    if reason is None:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value='Не указано', inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time))
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        try:
                            await member.send(embed=emb_user)
                        except:
                            pass
                        await member.add_roles(mute_role)
                        await ctx.reply(embed=emb)
                        await member.send(embed=emb_user)
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.remove_roles(mute_role)
                        try:
                            await member.send(embed=emb_user_stop)
                        except:
                            pass
                    else:
                        emb = discord.Embed(title=f'**System - Mute**')
                        emb.add_field(name='**Выдал:**', value=ctx.author.mention, inline=False)
                        emb.add_field(name='**Нарушитель:**', value=member.mention, inline=False)
                        emb.add_field(name='**ID нарушителя:**', value=member.id, inline=False)
                        emb.add_field(name='**Причина:**', value=reason, inline=False)
                        emb.add_field(name='**Длительность:**', value='{} день(ей)'.format(time), inline=False)
                        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

                        await member.add_roles(mute_role)
                        await ctx.reply(embed=emb)
                        try:
                            await member.send(embed=emb_user)
                        except:
                            pass
                        await asyncio.sleep(time * 60 * 60 * 24)
                        await member.remove_roles(mute_role)
                        try:
                            await member.send(embed=emb_user_stop)
                        except:
                            pass

    @bot.command(name='random', help='Рандомное число в диапазоне, который задал пользователь')
    async def join(ctx, a, b):
        ember = discord.Embed(title='Рандомное число от {} до {}'.format(a,b), inline=False)
        ember.add_field(name="Ответ", value=random.randrange(int(a), int(b)))
        await ctx.reply(embed=ember)



class music(commands.Cog):
    """Данные команды предназначены для взаимодействий с музыкой, которую воспроизводит бот"""

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='join', help='Присоединяется к voice каналу, в котором находится пользователь')
    async def join(ctx):
        times_start = datetime.today()
        emb = discord.Embed(title=f'**Я присоединился**')
        emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        emb1 = discord.Embed(title=f'**Вы не в голосовом канале**')
        emb1.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        if not ctx.message.author.voice:
            await ctx.reply(embed=emb1)
            return
        else:
            channel = ctx.message.author.voice.channel
            await ctx.reply(embed=emb)
        await channel.connect()

    @bot.command(name='leave', help='Отключает бота от канала')
    async def leave(ctx):
        times_start = datetime.today()
        emb_error = discord.Embed(title=f'**Я не был присоединён к каналу**')
        emb_error.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        try:
            leav = ['Отключаюсь', "Я работать?", "Всем пока", "Я устал, я... ухожу", "Всем до скорого!", "Adios"]
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected():
                emb = discord.Embed(title=f'**{choice(leav)}**')
                emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
                await voice_client.disconnect()
                await ctx.reply(embed=emb)
            else:
                await ctx.reply(embed=emb_error)
        except:
            await ctx.reply(embed=emb_error)

    @bot.command(name='play', help='Играет песню из ссылки youtube которую прикрепил пользователь')
    async def play(ctx, url):
        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            embedVar = discord.Embed(title="music", )
            embedVar.add_field(name="**сейчас играет**", value=filename, inline=False)
            await ctx.reply(embed=embedVar)
        except:
            emb_error = discord.Embed(title="Бот не подключён к канналу")
            await ctx.reply(embed=emb_error)

    @bot.command(name='playlist', help='Играет плейлист ссылок')
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
                await ctx.reply(embed=embedVar)
                while ctx.message.guild.voice_client.is_playing() or ctx.message.guild.voice_client.is_paused():
                    await asyncio.sleep(3)
        except:
            emb_error = discord.Embed(title="Бот не подключён к канналу")
            await ctx.reply(embed=emb_error)

    @bot.command(name='pause', help='Ставит песню на паузу')
    async def pause(ctx):
        times_start = datetime.today()
        emb_error = discord.Embed(title=f'**Я ничего не проигрываю**')
        emb_error.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            emb = discord.Embed(title=f'**Приостановил проигрывание композиции**')
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await ctx.reply(embed=emb)
            await voice_client.pause()
        else:
            await ctx.reply(embed=emb_error)

    @bot.command(name='resume', help='Возобновляет песню')
    async def resume(ctx):
        times_start = datetime.today()
        emb_error1 = discord.Embed(title=f'**Я ничего не проигрываю**')
        emb_error1.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        emb_error2 = discord.Embed(title=f'**Песня не стоит на паузе**')
        emb_error2.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            emb = discord.Embed(title=f'**Продолжаю проигрывание композиции**')
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await ctx.reply(embed=emb)
            await voice_client.resume()
        if voice_client.is_playing():
            await ctx.reply(embed=emb_error2)
        else:
            await ctx.reply(embed=emb_error1)

    @bot.command(name='stop', help='Останавливает песню и удаляет очередь')
    async def stop(ctx):
        times_start = datetime.today()
        emb_error = discord.Embed(title=f'**Я ничего не проигрываю**')
        emb_error.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            emb = discord.Embed(title=f'**Композиция больше не играет**')
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await ctx.reply(embed=emb)
            await voice_client.stop()
        else:
            await ctx.reply(embed=emb_error)

    @bot.command(name='skip', help='Останавливает песню и удаляет её из очереди')
    async def skip(ctx):
        times_start = datetime.today()
        emb_error = discord.Embed(title=f'**Я ничего не проигрываю**')
        emb_error.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            emb = discord.Embed(title=f'**Композиция больше не играет**')
            emb.set_footer(text=f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
            await ctx.reply(embed=emb)
            await voice_client.stop()
        else:
            await ctx.reply(embed=emb_error)


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


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
