import discord
from discord import default_permissions
import os
from dotenv import load_dotenv

# 外部環境変数ファイル読み込み
load_dotenv()
TOKEN = os.getenv("TOKEN")


bot = discord.Bot()


# ビュー定義
class RoleManagerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # 取得ボタン
    @discord.ui.button(label="取得", custom_id="button-grant", style=discord.ButtonStyle.blurple)
    async def grant_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # もしロールが見つからなければ終了
        role = await self.serch_role(interaction)
        if role == None:
            role_name = interaction.message.embeds[0].title
            print(f"ロール[{role_name}]が存在せず付与できませんでした")
            await interaction.response.send_message(f"ロール[{role_name}]が存在せず付与できませんでした", ephemeral=True)
            return

        # userがmemberじゃなければ終了（念のため）
        member = interaction.user
        if type(member) != discord.Member:
            print(f"不明なメンバーに付与できませんでした")
            return

        # ロール処理＆レスポンス＆ログ出力
        await member.add_roles(role)
        await interaction.response.send_message(f"ロール[{role.name}]を付与しました", ephemeral=True)
        print(f"{member.name}にロール[{role.name}]を付与しました")

    # 取り消しボタン
    @discord.ui.button(label="取り消し", custom_id="button-revoke", style=discord.ButtonStyle.red)
    async def revoke_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        # もしロールが見つからなければ終了
        role = await self.serch_role(interaction)
        if role == None:
            role_name = interaction.message.embeds[0].title
            print(f"ロール[{role_name}]が存在せず剥奪できませんでした")
            await interaction.response.send_message(f"ロール[{role_name}]が存在せず剥奪できませんでした", ephemeral=True)
            return

        # userがmemberじゃなければ終了（念のため）
        member = interaction.user
        if type(member) != discord.Member:
            print(f"不明なメンバーに剥奪できませんでした")
            return

        # ロール処理＆レスポンス＆ログ出力
        await member.remove_roles(role)
        await interaction.response.send_message(f"ロール[{role.name}]を取り消しました", ephemeral=True)
        print(f"{member.name}からロール[{role.name}]を剥奪しました")

    # ロール特定
    async def serch_role(self, interaction: discord.Interaction) -> discord.Role|None:
        role_name = interaction.message.embeds[0].title
        guild = await bot.fetch_guild(interaction.guild_id)
        role = discord.utils.get(guild.roles, name=role_name)
        return role

    # 起動時処理＆起動アナウンス
    @bot.event
    async def on_ready():
        bot.add_view(RoleManagerView())
        print("ロール管理botが起動しました")


# コマンド登録
@bot.command(name="rolemanager")
@default_permissions(manage_roles=True)
async def rolemanager(ctx: discord.ApplicationContext, message: discord.Option(discord.SlashCommandOptionType.string), role: discord.Option(discord.SlashCommandOptionType.string)):
    embed = discord.Embed(title=role, description=message)
    await ctx.respond(embed=embed, view=RoleManagerView())

# bot起動
bot.run(TOKEN)