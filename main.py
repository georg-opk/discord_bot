import discord
from discord.ext import commands


def token():
    return ""


bot = commands.Bot(command_prefix='!')


@bot.command(name='ping', help='Проверка подключения бота к серв    еру')
async def ping(ctx):
    await ctx.reply('Бот подключён!')


@bot.command(name='stop_bot', help='Доступно только создателю. Принудительная остановка бота')
@commands.is_owner()
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
@commands.is_owner()
async def flood(ctx, number_of_repetitions, *message):
    s = ''
    number_of_repetitions = int(number_of_repetitions)
    for i in message:
        s = s + i + " "
    while number_of_repetitions > 0:
        await ctx.send(s)
        number_of_repetitions -= 1


bot.run(token())
