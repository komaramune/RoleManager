import discord
from discord import default_permissions
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = discord.Bot()



class RoleManagerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(label="取得", custom_id="button-grant", style=discord.ButtonStyle.blurple)
    async def grant_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = await self.serch_role(interaction)
        if role == None:
            return

        member = interaction.user
        if type(member) != discord.Member:
            return

        await member.add_roles(role)
        await interaction.response.send_message(f"ロール[{role.name}]を付与しました", ephemeral=True)
        print(f"{member.name}にロール[{role.name}]を付与しました")


    @discord.ui.button(label="取り消し", custom_id="button-revoke", style=discord.ButtonStyle.red)
    async def revoke_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        role = await self.serch_role(interaction)
        if role == None:
            return

        member = interaction.user
        if type(member) != discord.Member:
            return

        await member.remove_roles(role)
        await interaction.response.send_message(f"ロール[{role.name}]を取り消しました", ephemeral=True)
        print(f"{member.name}からロール[{role.name}]を剥奪しました")


    async def serch_role(self, interaction: discord.Interaction) -> discord.Role:
        role_name = interaction.message.embeds[0].title
        guild = await bot.fetch_guild(interaction.guild_id)
        role = discord.utils.get(guild.roles, name=role_name)
        return role


    @bot.event
    async def on_ready():
        bot.add_view(RoleManagerView())
        print("ロール管理botが起動しました")



@bot.command(name="rolemanager")
@default_permissions(manage_roles=True)
async def rolemanager(ctx: discord.ApplicationContext, message: discord.Option(discord.SlashCommandOptionType.string), role: discord.Option(discord.SlashCommandOptionType.string)):
    embed = discord.Embed(title=role, description=message)
    await ctx.respond(embed=embed, view=RoleManagerView())

bot.run(TOKEN)