import discord
from discord import default_permissions

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

intent = discord.Intents.all()
intent.messages = True

bot = discord.Bot(intents=discord.Intents(reactions=True))

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.id != bot.user.id:
        return

    guild = await bot.fetch_guild(payload.guild_id)
    bot_member = await guild.fetch_member(bot.user.id)
    member = await guild.fetch_member(payload.user_id)

    for role in bot_member.roles:
        if payload.emoji.name == role.name:
            await member.add_roles(role)
            break

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if message.author.id != bot.user.id:
        return

    guild = await bot.fetch_guild(payload.guild_id)
    bot_member = await guild.fetch_member(bot.user.id)
    member = await guild.fetch_member(payload.user_id)

    for role in bot_member.roles:
        if payload.emoji.name == role.name:
            await member.remove_roles(role)
            break


@bot.command(name="rolemanager")
@default_permissions(manage_roles=True)
async def rolemanager(ctx: discord.ApplicationContext):
    await ctx.respond("ロール管理botです\nこのメッセージに所定のリアクションを付けると隠されたチャンネルを見ることができるようになります\nリアクションを取り消すとキャンセルされます")

@bot.event
async def on_ready():
    print("ロール管理botが起動しました")

bot.run(TOKEN)