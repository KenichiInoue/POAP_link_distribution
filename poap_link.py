#%%
import random
import discord
import settings

DISCORD_TOKEN = settings.HENKAKU_POAP_LINK_BOT_TOKEN   # discord bot token
GUILD = 1003692205594128414   # Jikkenjo
VC_CH = 1015300873125113926   # VoiceChannels:12
OMIKUJI = ["大吉", "中吉", "吉", "小吉", "末吉"]
writing_hand = "✍️"
member_list, poaplist = [], []

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_voice_state_update(member, before, after):
    global member_list
    global poap_list
    ch = client.get_channel(VC_CH)
    mem = str(member)
    mem_id = str(member.id)
    if str(before.channel) == "None" and str(after.channel) != "None":   # VC in
        if VC_CH == after.channel.id:
            if before.channel == None and after.channel != None:
                if not mem in [m for [m, _] in member_list]:   # avoid re-enter
                    await ch.send("こんにちは、{}さん".format(mem))
                    await ch.send("{}さんの今日の運勢は「{}」です！".format(mem, OMIKUJI[random.randrange(5)]))
                    member_list.append([mem, mem_id])
                    if len(poap_list) > 0:   # if POAP list was already resistered.
                        if len(member_list) <= len(poap_list):
                            guild = client.get_guild(GUILD)
                            for [m, mid], c in zip(member_list, poap_list):
                                if m == mem:
                                    gm = await guild.fetch_member(int(mid))
                                    await gm.send("POAPのリンクです:{}".format(c))
                        else:
                            await ch.send("POAPが売り切れました!{}さんの分がありません!".format(mem))
                else:
                    await ch.send("おかえりなさい、{}さん".format(mem))
    if str(before.channel) != "None" and str(after.channel) == "None":   # VC out
        if len(member_list) >= 1 and len(ch.members) == 0:
            member_list = []
            poap_list = []


@client.event
async def on_raw_reaction_add(payload):
    global member_list
    global poap_list
    if payload.channel_id == VC_CH:
        ch = client.get_channel(payload.channel_id)
        message = await ch.fetch_message(payload.message_id)
        if payload.emoji.name == writing_hand:
            attch = list(message.attachments)
            if attch == []:   # if link list test is resistered.
                cnt = message.content
                poap_list = str(cnt).split("\n")
            else:             # if link file (often links.txt) is resistered.
                f = str(attch[0]).split("/")[-1]  # extract only file name
                csv = open(f, "r")
                poap_list = list(csv)
            if len(poap_list) > 0:    # if link list is successfully resistered.
                guild = client.get_guild(GUILD)
                await ch.send("今からPOAPのリンクを配布します!")
                if len(member_list) > len(poap_list):
                    await ch.send("全員にPOAPを配れないようです。")
                    await ch.send("最初の{}人に配ります。".format(len(poap_list)))
                for [mem, mem_id], c in zip(member_list, poap_list):
                    gm = await guild.fetch_member(int(mem_id))
                    if str(gm) != "None":
                        await gm.send("POAPのリンクです:{}".format(c))
                        await ch.send("{}さんにリンクを送りました！".format(mem))
                    else:
                        await ch.send("{}さんは不在なのでリンクを置いておきます。".format(mem))
                        await ch.send("{}さんのPOAPのリンクです: {}".format(mem, c))

client.run(DISCORD_TOKEN)
