import discord
from discord.ext import commands
from discord import Embed, ButtonStyle
import json, os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

SONG_FILE = "songs.json"

def load_songs():
    if not os.path.exists(SONG_FILE):
        with open(SONG_FILE, "w") as f:
            json.dump({}, f)
    with open(SONG_FILE, "r") as f:
        return json.load(f)

def save_songs(data):
    with open(SONG_FILE, "w") as f:
        json.dump(data, f, indent=4)

class CommandButton(discord.ui.View):
    def __init__(self, cmd):
        super().__init__(timeout=None)
        self.cmd = cmd

        button = discord.ui.Button(
            label="Copy Command",
            style=ButtonStyle.primary
        )
        button.callback = self.send_cmd
        self.add_item(button)

    async def send_cmd(self, interaction):
        await interaction.response.send_message(
            f"```
{self.cmd}
```",
            ephemeral=True
        )

@bot.event
async def on_ready():
    print(f"Bot is online: {bot.user}")

@bot.command()
async def help(ctx):
    embed = Embed(title="Help", description="Available commands:", color=0x3498db)
    embed.add_field(name="?search <name>", value="Search songs.", inline=False)
    embed.add_field(name="?save <command> name <song_name>", value="Save a song.", inline=False)
    embed.add_field(name="?list", value="List songs.", inline=False)
    embed.add_field(name="?delete <song_name>", value="Delete a song.", inline=False)
    await ctx.reply(embed=embed)

@bot.command()
async def save(ctx, command: str, label: str, *, song_name: str):
    if label.lower() != "name":
        return await ctx.reply("Error format. Use: ?save <command> name <song_name>")

    songs = load_songs()
    songs[song_name] = command
    save_songs(songs)

    embed = Embed(title="Saved", color=0x2ecc71)
    embed.add_field(name="Name", value=f"**{song_name}**", inline=False)
    embed.add_field(name="Command", value=f"`{command}`", inline=False)

    await ctx.reply(embed=embed)

@bot.command()
async def list(ctx):
    songs = load_songs()
    if not songs:
        return await ctx.reply("No songs saved.")

    embed = Embed(title="Song List", color=0x9b59b6)
    for name, cmd in songs.items():
        embed.add_field(name=f"**{name}**", value=f"`{cmd}`", inline=False)

    await ctx.reply(embed=embed)

@bot.command()
async def delete(ctx, *, name: str):
    songs = load_songs()
    if name not in songs:
        return await ctx.reply("Not found.")
    del songs[name]
    save_songs(songs)

    embed = Embed(title="Deleted", color=0xe74c3c)
    embed.add_field(name="Name", value=f"**{name}**", inline=False)
    await ctx.reply(embed=embed)

@bot.command()
async def search(ctx, *, name: str):
    songs = load_songs()
    result = {k:v for k,v in songs.items() if name.lower() in k.lower()}

    if not result:
        return await ctx.reply("No results.")

    embed = Embed(title="Search Results", color=0x1abc9c)

    for n, cmd in result.items():
        embed.add_field(name=f"**{n}**", value=f"`{cmd}`", inline=False)

    view = CommandButton(list(result.values())[0])
    await ctx.reply(embed=embed, view=view)

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("TOKEN missing")
