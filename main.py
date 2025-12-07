import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="?", intents=intents, help_command=None)  # حذف help پیش‌فرض


# ------------------------- CUSTOM HELP -----------------------------

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title="🎵 راهنمای ربات Music Saver",
        description="تمام کامندهای ربات اینجاست:",
        color=0xFFD700
    )

    embed.add_field(name="🎶 ?play <اسم آهنگ>", value="پخش آهنگ", inline=False)
    embed.add_field(name="⬇️ ?save <اسم آهنگ>", value="سیو آهنگ", inline=False)
    embed.add_field(name="📜 ?list", value="نمایش لیست کامل کامندها", inline=False)

    # دکمه‌ای که کامند "/play" را وارد چت کاربر کند
    view = View()
    view.add_item(Button(
        label="🎧 اجرای دستور /play",
        style=discord.ButtonStyle.primary,
        custom_id="insert_play"
    ))

    await ctx.send(embed=embed, view=view)


# ------------------------- BUTTON HANDLER -----------------------------

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type.name == "component":   # یعنی دکمه زده شد
        if interaction.data.get("custom_id") == "insert_play":
            await interaction.response.send_message(
                "برای استفاده:\n`/play <اسم آهنگ>` 🎵",
                ephemeral=True
            )


# ------------------------- ?list COMMAND -----------------------------

@bot.command(name="list")
async def list_command(ctx):
    embed = discord.Embed(
        title="📜 Commands List",
        description="All the Commands you can use:",
        color=0x00FFAA
    )

    embed.add_field(name="?play", value="پخش آهنگ", inline=False)
    embed.add_field(name="?save", value="سیو آهنگ", inline=False)
    embed.add_field(name="?list", value="نمایش همین لیست", inline=False)
    embed.add_field(name="?help", value="کمک و راهنما", inline=False)

    await ctx.send(embed=embed)


# ------------------------- BOT READY -----------------------------

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands.")
    except Exception as e:
        print("Sync Error:", e)


bot.run("YOUR_TOKEN")
