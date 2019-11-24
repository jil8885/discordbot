import asyncio
import discord
import os
import requests

app = discord.Client()
token = os.environ["discord_auth"]


@app.event
async def on_ready():
    print("Log in as :", app.user.name)
    await app.change_presence(activity=discord.Game(name="환영합니다 D:", type=1))


@app.event
async def on_message(message):
    if message.author.bot:
        return None
    txt = message.content
    if txt.split(" ")[0] == "!버전":
        # try:
        if "openttd" in txt.split(" ")[1].lower():
            release_url = "https://api.github.com/repos/OpenTTD/OpenTTD/releases"
            release_info = requests.get(release_url).json()
            release = False
            beta = False
            for x in release_info:
                if x["prerelease"] and not beta:
                    beta = True
                    string = "Vanilla Testing : " + x["tag_name"] + "\n"
                elif not x["prerelease"] and not release:
                    release = True
                    string += "Vanilla Stable : " + x["tag_name"] + "\n"
                else:
                    break
            release_url = "https://api.github.com/repos/JGRennison/OpenTTD-patches/releases"
            release_info = requests.get(release_url).json()
            release = False
            beta = False
            for x in release_info:
                if x["prerelease"] and not beta:
                    beta = True
                    string += "JGR Testing : " + x["tag_name"] + "\n"
                elif not x["prerelease"] and not release:
                    release = True
                    string += "JGR Stable : " + x["tag_name"]
                else:
                    break
        elif "rct" in txt.split(" ")[1].lower():
            release_url = "https://api.github.com/repos/OpenRCT2/OpenRCT2/releases/latest"
            commit_url = "https://api.github.com/repos/OpenRCT2/OpenRCT2/commits"
            release_info = requests.get(release_url).json()
            commit_info = requests.get(commit_url).json()[0]["sha"]
            string = "Stable version : " + release_info["tag_name"] + "\n"
            string += "Testing version : " + release_info["tag_name"] + "-" + commit_info[:7]
        elif txt.split(" ")[1].lower() == "help":
            string = "OpenTTD 버전 정보는 !버전 OpenTTD\nOpenRCT2 버전 정보는 !버전 OpenRCT2라고 입력해주세요."
        # except:
        #     string = "!버전 명령어 도움말은 !버전 help\nOpenTTD 버전 정보는 !버전 OpenTTD\nOpenRCT2 버전 정보는 !버전 OpenRCT2라고 입력해주세요."
        await message.channel.send(string)


app.run(token)