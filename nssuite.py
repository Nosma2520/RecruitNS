import asyncio
import logging

import aiohttp
import discord
from bs4 import BeautifulSoup
from discord.ext import commands

intents = discord.Intents.default()

# Initiate logging
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

with open("token.txt", "r") as tk:
    TOKEN = tk.read().strip()

bot = commands.Bot(command_prefix="&", intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Successfully logged in to discord.")


@bot.command()
async def help(ctx):
    # Rewrote help command and overrode default implementation.
    # This way, the help commmand looks slightly nicer, and sends
    # information to the author's DM, rather than clogging up
    # server channels with a one-message help command.
    # Realistically, it doesn't even need to be implemented, but here
    # we are. So... DM it is.
    embed = discord.Embed(
        title="Help Page",
        description="This bot is a NationStates API recruitment client. Only "
        "those with express permission can use it.\n\n**Command "
        "Structure**\n&recruit {Client Key} {Telegram ID} {Secret "
        "Key}{Your NS Nation} {number of telegrams} {region}",
    )
    await ctx.author.send(embed=embed)
    await ctx.send("Check your DMs!")


@bot.command()
async def recruit(ctx):
    def check(m):
        chk = False
        if m.author == ctx.author and m.author.bot is not True:
            chk = True
        return chk

    # Get client information
    await ctx.send("Please enter your client key")
    client = await bot.wait_for("message", check=check)
    await ctx.send("Please enter your TGID")
    tgid = await bot.wait_for("message", check=check)
    await ctx.send("Please enter your secret key")
    skey = await bot.wait_for("message", check=check)
    await ctx.send(
        "Please enter a useragent. This should ideally be your main nation on nationstates.net"
    )
    uagent = await bot.wait_for("message", check=check)
    await ctx.send("Please enter the number of telegrams you wish to send")
    numtgs = await bot.wait_for("message", check=check)
    await ctx.send("Please enter the region you wish to recruit for")
    reg = await bot.wait_for("message", check=check)

    # In keeping with user-interface principles, the command
    # is not a massive string of numbers and letters, requiring
    # the user to remember where to use quotes and where they should
    # not, but instead prompts the user to answer each question
    # individually, allowing for them to know what they are doing

    # Store variables in a dictionary for proper access handling
    authring = {
        "client": client.content,
        "tgid": tgid.content,
        "secret key": skey.content,
        "user agent": uagent.content,
        "number": numtgs.content,
        "region": reg.content,
    }

    # For "security" purposes, erase prior messages.
    # This doesn't actually really impact security, as anyone with half a brain would
    # be running the bot in a secured channel anyways, and you're passing your auth tokens
    # to some unknown server with no idea what's going on with the backend, but hey, at least
    # people in your server won't be able to see them.
    lim = 12
    await ctx.channel.purge(limit=lim)

    # Pass relevant information to an async context manager, ensuring that
    # the bot runs actually asynchronously, rather than a hack-job
    # async run. The async context manager is being used for the request, along
    # with aiohttp instead of requests, so that things work properly and requests
    # are non-blocking as opposed to requests, which works synchronously, and as
    # a side-effect tends to slow code execution, along with blocking command
    # usage in d.py.
    i = 0
    while i < numtgs:
        with authring as auth:
            headers = {"User-Agent": auth["user agent"]}
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://www.nationstates.net/cgi-bin/api.cgi?q=newnations",
                    headers=headers,
                ) as req:
                    soup = BeautifulSoup(req.text, "lxml")
                    natlist = soup.newnations.string
                    r_list = natlist.split()
                    async for new in r_list[:5]:
                        async with session.get(
                            f"https://nationstates.net/cgi-bin/api.cgi?nation={new}&q=tgcanrecruit",
                            headers=headers,
                        ) as que:
                            canrec_soup = BeautifulSoup(que.text, "lxml")
                            val = canrec_soup.tgcanrecruit.string
                            if val == 0:
                                await session.get(
                                    f"https://nationstates.net/cgi-bin/api.cgi?a=sendTG&"
                                    f"client={auth['client']}&tgid={auth['tgid']}&key="
                                    f"{auth['secret key']}&to={new}"
                                )
                                await ctx.send(
                                    "Telegram sent... waiting for API limit to expire."
                                )
                                await asyncio.sleep(180)
                            else:
                                await asyncio.sleep(0.6)
                                await ctx.send(
                                    "Target unable to be recruited. Moving to next one..."
                                )
        i = i + 1


bot.run(TOKEN)
