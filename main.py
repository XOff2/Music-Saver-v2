import discord
from discord.ext import commands
from discord.ui import View, Button

import json
import os

# -------------------- BOT CONFIG --------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)

DATA_FILE = "songs.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)


# -------------------- SAVE DATA --------------------
def load_songs():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_songs(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------- ?search --------------------
@bot.command(name="search")
async def search(ctx, *, song_name: str = None):
    if not song_name:
        embed = discord.Embed(
            title="Error",
            description="Usage: ?search <song_name>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    embed = discord.Embed(
        title="Search Result",
        description=f"**{song_name}**",
        color=0x3498db
    )

    # Button to insert /play <song>
    view = View()
    button = Button(
        label="Insert /play command",
        style=discord.ButtonStyle.primary,
        custom_id=f"insert_play_{song_name}"
    )
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


# -------------------- ?save <command> name <song> --------------------
@bot.command(name="save")
async def save(ctx, *, args=None):
    """
    Expected format:
    ?save play name despacito
    """
    if not args or "name" not in args:
        embed = discord.Embed(
            title="Error",
            description="Format: ?save <command> name <song_name>",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    parts = args.split("name", 1)
    command_part = parts[0].strip()
    song_name = parts[1].strip()

    if command_part == "" or song_name == "":
        embed = discord.Embed(
            title="Error",
            description="Invalid format. Example:\n?save play name despacito",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return

    data = load_songs()
    data[song_name] = command_part
    save_songs(data)

    embed = discord.Embed(
        title="Saved",
        description=f"Saved **{song_name}** with command `{command_part}`",
        color=0x2ecc71
    )

    await ctx.send(embed=embed)


# -------------------- ?list --------------------
@bot.command(name="list")
async def list_cmd(ctx):
    data = load_songs()

    embed = discord.Embed(
        title="Saved Songs",
        color=0xf1c40f
    )

    if not data:
        embed.description = "No songs saved."
        await ctx.send(embed=embed)
        return

    for name, cmd in data.items():
        embed.add_field(
            name=f"🎵 **{name}**",
            value=f"`{cmd}`",
            inline=False
        )

    await ctx.send(embed=embed)


# -------------------- ?delete --------------------
@bot.command(name="delete")
async def delete_cmd(ctx, *, song_name=None):
    if not song_name:
        embed = discord.Embed(
            title="Error",
            description="Usage: ?delete <song_name>",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return

    data = load_songs()

    if song_name not in data:
        embed = discord.Embed(
            title="Not Found",
            description=f"No entry for **{song_name}**",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return

    del data[song_name]
    save_songs(data)

    embed = discord.Embed(
        title="Deleted",
        description=f"Removed **{song_name}**",
        color=0xe67e22
    )

    await ctx.send(embed=embed)


# -------------------- ?help --------------------
@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="Music Saver Help",
        color=0x9b59b6
    )

    embed.add_field(name="?search <song>", value="Search a song", inline=False)
    embed.add_field(name="?save <command> name <song>", value="Save a song command", inline=False)
    embed.add_field(name="?list", value="Show all saved songs", inline=False)
    embed.add_field(name="?delete <song>", value="Delete a saved song", inline=False)
    embed.add_field(name="?help", value="Show this help menu", inline=False)

    await ctx.send(embed=embed)


# -------------------- BUTTON HANDLER --------------------
@bot.event
async def on_interaction(interaction: discord.Interaction):
    custom = interaction.data.get("custom_id")

    if custom and custom.startswith("insert_play_"):
        song = custom.replace("insert_play_", "")

        await interaction.response.send_message(
            f"/play {song}",
            ephemeral=True
        )


# -------------------- READY --------------------
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")


bot.run(os.getenv("BOT_TOKEN"))
