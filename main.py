import disnake
from disnake.ext import commands
from disnake.ext import tasks
import aiosqlite
from itertools import cycle
import os
import configparser
import datetime

intents = disnake.Intents.all()
bot = commands.Bot(
    command_prefix="ss",
    intents=intents,
    owner_ids=[671231351013376015],
    test_guilds=[911676954317582368],
)
bot.remove_command("help")
embedcolor = 0x0000FF
errorcolor = 0xFF0000
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8-sig")
token = config["token"]["token"]

for filename in os.listdir("Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

async def make_table(db, tables):
    async with aiosqlite.connect(db, isolation_level=None) as cursor:
        for i in tables:
            await cursor.execute(f"CREATE TABLE IF NOT EXISTS {i}")

@bot.event
async def on_ready():
    await make_table(
        "Picture.db",
        [
            "picture (id INTEGER NOT NULL UNIQUE PRIMARY KEY, link TEXT NOT NULL UNIQUE, title TEXT NOT NULL, author_id INTEGER NOT NULL, tags TEXT NOT NULL, thumbs_up INTEGER NOT NULL, can_remix INTEGER NOT NULL)",
            "thumbs_up (id INTEGER NOT NULL UNIQUE PRIMARY KEY, _id TEXT NOT NULL)"
        ],
    )
    await make_table(
        "User.db",
        [
            "user (id INTEGER NOT NULL UNIQUE PRIMARY KEY, commision INTEGER NOT NULL, level INTEGER NOT NULL, pictures INTEGER NOT NULL, joined_at INTEGER NOT NULL)"
        ],
    )
    print(f"Main\n{str(bot.user)}")
    status = cycle(
        [
            "/help(슬래시커맨드)",
            f"서버:{len(bot.guilds)}개/유저:{len(bot.users)}명이랑 함께 그리기",
            "이 메세지를 10초마다 다르게",
        ]
    )

    @tasks.loop(seconds=10)
    async def change_status():
        await bot.change_presence(
            status=disnake.Status.online, activity=disnake.Game(next(status))
        )

    change_status.start()

    @tasks.loop(hours=5)
    async def backup():
        await (await bot.fetch_channel(890483416041160744)).send(
            str(datetime.datetime.utcnow() + datetime.timedelta(hours=9)),
            files=[disnake.File("Picture.db"), disnake.File("User.db")],
        )

    backup.start()


bot.run(token)