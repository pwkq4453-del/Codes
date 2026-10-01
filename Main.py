import os
import discord
from discord.ext import commands

# 봇 기본 설정 및 인텐트
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 고정 감시 대상 음성 채널 ID (입력해 준 채널 ID 2개)
TARGET_CHANNEL_IDS = {1551967661112426526, 1551967340420268112}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print(f"감시 대상 채널 수: {len(TARGET_CHANNEL_IDS)}개")
    print("------")

@bot.event
async def on_voice_state_update(member, before, after):
    channel = after.channel or before.channel
    
    # 지정한 채널 ID가 아니면 무시
    if not channel or channel.id not in TARGET_CHANNEL_IDS:
        return

    everyone_role = channel.guild.default_role
    current_members = len(channel.members)

    # 2명 이상 -> 채널 숨기기
    if current_members >= 2:
        overwrite = channel.overwrites_for(everyone_role)
        if overwrite.view_channel is not False:
            await channel.set_permissions(everyone_role, view_channel=False)
            print(f"[{channel.name}] 2명 달성 -> 숨김 처리 완료")
            
    # 2명 미만 -> 다시 표시
    else:
        overwrite = channel.overwrites_for(everyone_role)
        if overwrite.view_channel is False:
            await channel.set_permissions(everyone_role, view_channel=None)
            print(f"[{channel.name}] 1명 이하 -> 다시 표시 완료")

# 환경 변수에서 토큰 로드
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("❌ DISCORD_TOKEN 환경 변수가 설정되지 않았어!")
