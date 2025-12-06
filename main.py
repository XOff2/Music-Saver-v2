import discord
from discord.ext import commands
from discord.ui import Button, View
import json
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

DATA_FILE = "songs.json"

# Load or create storage
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

bot = commands.Bot(command_prefix="?", help_command=None, intents=intents)

# ---------------- HELP COMMAND ----------------
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description=(
            "**?search <name>** - Search song name\n"
            "**?save <command> name <songname>** - Save a music command\n"
            "**?list** - List saved commands\n"
            "**?delete <songname>** - Delete a saved command\n"
        ),
        color=0x2b8cff
    )
    await ctx.send(embed=embed)


# ---------------- SEARCH COMMAND ----------------
@bot.command()
async def search(ctx, *, query=None):
    if not query:
        return await ctx.send("You must enter a song name.")

    embed = discord.Embed(
        title="Search Result",
        description=f"Search keyword: **{query}**",
        color=0x00ff9d
    )
    await ctx.send(embed=embed)


# ---------------- SAVE COMMAND ----------------
@bot.command()
async def save(ctx, command=None, name=None, *, songname=None):

    if not command or not name or not songname:
        return await ctx.send("Format: ?save <command> name <songname>")

    if name.lower() not in ["name", "-name", "--name"]:
        return await ctx.send("Format error: expected keyword 'name' between command and songname.")

    data = load_data()
    data[songname] = command
    save_data(data)

    embed = discord.Embed(
        title="Saved",
        description=f"Saved: **{songname}**",
        color=0x5cff4d
    )
    await ctx.send(embed=embed)


# ---------------- LIST COMMAND ----------------
@bot.command()
async def list(ctx):
    data = load_data()

    if not data:
        return await ctx.send("No saved commands.")

    embed = discord.Embed(
        title="Saved Music Commands",
        color=0x7289da
    )

    for song, cmd in data.items():

        # Insert into chat button
        button = Button(label="Insert Command", style=discord.ButtonStyle.green)

        async def button_callback(interaction, text=cmd):
            await interaction.response.send_message(
                content=f"`{text}`", ephemeral=True
            )

        button.callback = button_callback
        view = View()
        view.add_item(button)

        embed.add_field(
            name=f"**{song}**",
            value=f"Command stored.",
            inline=False
        )

        await ctx.send(embed=embed, view=view)
        embed = discord.Embed(title="")  # reset loop embed


# ---------------- DELETE COMMAND ----------------
@bot.command()
async def delete(ctx, *, songname=None):
    if not songname:
        return await ctx.send("Enter a song name to delete.")

    data = load_data()

    if songname not in data:
        return await ctx.send("Song not found.")

    del data[songname]
    save_data(data)

    embed = discord.Embed(
        title="Deleted",
        description=f"Removed: **{songname}**",
        color=0xff4040
    )
    await ctx.send(embed=embed)


# ---------------- RUN BOT ----------------
import os
bot.run(os.getenv("DISCORD_TOKEN"))
