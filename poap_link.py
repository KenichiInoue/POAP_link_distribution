#%%
import numpy as np
import random
import discord
# import discord.app_commands
import settings
# import datetime
from discord.utils import get

DISCORD_TOKEN = settings.HENKAKU_BOT_TOKEN   # discord bot token
JIKKENJO = 1003692205594128414
VC_CH = 1015300873125113926   # VoiceChannels:12
OMIKUJI = ["大吉", "中吉", "吉", "小吉", "末吉"]
writing_hand = "✍️"
member_list = []

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_voice_state_update(member, before, after):
    global member_list
    ch = client.get_channel(VC_CH)
    mem = str(member)
    mem_id = str(member.id)
    # print(mem, mem_id)
    if before.channel == None and after.channel != None:
        if VC_CH == after.channel.id:
            if not mem in [m for [m, _] in member_list]:   # avoid re-enter
                await ch.send("こんにちは、{}さん".format(mem))
                await ch.send("{}さんの今日の運勢は「{}」です！".format(mem, OMIKUJI[random.randrange(5)]))
                member_list.append([mem, mem_id])
                # print("member list:", member_list)
            else:
                await ch.send("おかえりなさい、{}さん".format(mem))


@client.event
async def on_raw_reaction_add(payload):
    global member_list
    if payload.channel_id == VC_CH:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # reaction = get(message.reactions, emoji=payload.emoji.name)
        # date = datetime.datetime.now()
        # #mes_id = message.author.name
        # up_id = payload.member.name
        # print("{},{},{},{}".format(date, mes_id, up_id, reaction))
        if payload.emoji.name == writing_hand:
            f = str(list(message.attachments)[0]).split("/")[-1]  # extract only file name, molstly links.txt
            csv = open(f)
            poap_list = str(list(csv)).replace("[", "").replace("]", "").replace("\n", "").replace("'", "").split(", ")
            if len(poap_list) > 0:
              guild = client.get_guild(JIKKENJO)
              # print("guild:", guild)
              # print("guild members:", list(guild.members))
              await channel.send("今からPOAPのリンクを配布します!")
              if len(member_list) > len(poap_list):
                  await channel.send("全員にPOAPを配れないようです。")
                  await channel.send("最初の{}人に配ります。".format(len(poap_list)))
              for [mem, mem_id], c in zip(member_list, poap_list):
                  # print("mem={}, mem_id={}, c={}".format(mem, mem_id, c))
                  gm = guild.get_member(int(mem_id))
                  # print("gm={}".format(gm))
                  await gm.send("POAPのリンクです: {}".format(c))
                  await channel.send("{}さんにリンクを送りました！".format(mem))


client.run(DISCORD_TOKEN)
