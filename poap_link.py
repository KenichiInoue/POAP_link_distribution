#%%
import random
import discord
import settings
# from discord.utils import get

DISCORD_TOKEN = settings.HENKAKU_POAP_LINK_BOT_TOKEN   # discord bot token
GUILD = 1003692205594128414   # Jikkenjo
VC_CH = 1015300873125113926   # VoiceChannels:12
OMIKUJI = ["大吉", "中吉", "吉", "小吉", "末吉"]
writing_hand = "✍️"
member_list = []

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_voice_state_update(member, before, after):
    global member_list
    global poap_list
    ch = client.get_channel(VC_CH)
    mem = str(member)
    mem_id = str(member.id)
    print(mem, mem_id)
    if before.channel == None and after.channel != None:
        print("VC in:", mem)
        if VC_CH == after.channel.id:
            if not mem in [m for [m, _] in member_list]:   # avoid re-enter
                await ch.send("こんにちは、{}さん".format(mem))
                await ch.send("{}さんの今日の運勢は「{}」です！".format(mem, OMIKUJI[random.randrange(5)]))
                member_list.append([mem, mem_id])
                print("member list:", member_list)
                if len(poap_list) > 0:
                    if len(member_list) <= len(poap_list):
                        guild = client.get_guild(GUILD)
                        print("guild:", guild)
                        for [mem, mem_id], c in zip(member_list, poap_list):
                            gm = await guild.fetch_member(int(mem_id))
                            print("gm={}".format(gm))
                            await gm.send("POAPのリンクです:{}".format(c))
                    else:
                        ch.send("POAPが売り切れました!{}さんの分がありません!".format(mem))
            else:
                await ch.send("おかえりなさい、{}さん".format(mem))
    if before.channel != None and after.channel == None:   # VC out
        print("VC out:", mem)
        if len(member_list) >= 1 and len(ch.members) == 0:
            print("deleting all list...")
            member_list = []
            poap_list = []


@client.event
async def on_raw_reaction_add(payload):
    global member_list
    global poap_list
    if payload.channel_id == VC_CH:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        # reaction = get(message.reactions, emoji=payload.emoji.name)
        # date = datetime.datetime.now()
        # mes_id = message.author.name
        # up_id = payload.member.name
        # print("{},{},{},{}".format(date, mes_id, up_id, reaction))
        if payload.emoji.name == writing_hand:
            attch = list(message.attachments)
            print("attach:", attch)
            if attch == []:
                print("message:", message)
                cnt = message.content
                print("message content:", cnt)
                poap_list = str(cnt).split("\n")
                print("poap_list:", poap_list)
            else:
                f = str(attch[0]).split("/")[-1]  # extract only file name, molstly links.txt
                print("open:", f)
                csv = open(f, "r")
                poap_list = list(csv)
                print("poap_list:", poap_list)
            if len(poap_list) > 0:
                guild = client.get_guild(GUILD)
                print("guild:", guild)
                print("guild members:", list(guild.members))
                await channel.send("今からPOAPのリンクを配布します!")
                if len(member_list) > len(poap_list):
                    await channel.send("全員にPOAPを配れないようです。")
                    await channel.send("最初の{}人に配ります。".format(len(poap_list)))
                for [mem, mem_id], c in zip(member_list, poap_list):
                    print("mem={}, mem_id={}, c={}".format(mem, mem_id, c))
                    # gm = guild.get_member(int(mem_id))
                    gm = await guild.fetch_member(int(mem_id))
                    print("gm={}".format(gm))
                    if str(gm) != "None":
                        await gm.send("POAPのリンクです:{}".format(c))
                        await channel.send("{}さんにリンクを送りました！".format(mem))
                    else:
                        await channel.send("{}さんは不在なのでリンクを置いておきます。".format(mem))
                        await channel.send("{}さんのPOAPのリンクです: {}".format(mem, c))


client.run(DISCORD_TOKEN)
