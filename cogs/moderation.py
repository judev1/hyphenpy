import discord
from discord.ext import commands, tasks
import asyncio
import re
import datetime
from copy import deepcopy
from dateutil.relativedelta import relativedelta

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} has been loaded\n-----")

    @commands.command(name="Kick", description="Kicks the specified user.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason="No reason was provided"):
        embed = discord.Embed(title="User Kicked!", description=(f"User : {member.mention}, was kicked by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await member.kick(reason=reason)

        channel = self.client.get_channel(774727230122622976)

        embed1 = discord.Embed(title="User Kicked!", description=(f"User : {member.mention}, was kicked by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await channel.send(embed=embed1)

        embed2 = discord.Embed(title=(f"You have been kicked from {server.name}!"), description=(f"You were kicked by Staff member : {ctx.message.author} with the reason : {reason}!\nJoin again if you like, but behave!"), color=0x31e30e)
        try:
            await member.send(embed=embed2)
            print(f"Messages succeded in sending to {member.name}")
        
        except discord.Forbidden:
            print("User has DMs disabled.")

    @commands.command(name="Ban", description="Bans the specified user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason="No reason was provided"):
        server = ctx.message.guild
        embed = discord.Embed(title="User Banned!", description=(f"User : {member.mention}, was banned by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await member.ban(reason=reason)

        channel = self.client.get_channel(774727230122622976)

        embed1 = discord.Embed(title="User Banned!", description=(f"User : {member.mention}, was banned by Staff member : {ctx.message.author.mention}. \n With the reason : {reason}!"), color=0x31e30e)
        await channel.send(embed=embed1)
        
        embed2 = discord.Embed(title=(f"You have been permanently banned from {server.name}!"), description=(f"Well, this is awkward...\nYou were banned by Staff member : {ctx.message.author} with the reason : {reason}!"), color=0x31e30e)
        try:
            await member.send(embed=embed2)
            print(f"Messages succeded in sending to {member.name}")
        
        except discord.Forbidden:
            print("User has DMs disabled.")

    @commands.command(name="unban", aliases=["ub"], description="Unbans the specified banned user.", usage="unban <ID/Username + Discriminator>")
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(title="User Unbanned!", description=(f"User : {user}, was unbanned by Staff member : {ctx.message.author.mention}!"), color=0x31e30e)
        await ctx.send(embed=embed)

        channel = self.client.get_channel(774727230122622976)

        embed1 = discord.Embed(title="User Unbanned!", description=(f"User : {user}, was unbanned by Staff member : {ctx.message.author.mention}!"), color=0x31e30e)
        await channel.send(embed=embed1)

        server = ctx.message.guild
        
        embed2 = discord.Embed(title=(f"You have been unbanned from {server.name}!"), description=(f"Welcome back! You have been unbanned from {server.name}.\nMake sure to behave this time!"), color=0x31e30e)
        try:
            await user.send(embed=embed2)
            print(f"Messages succeded in sending to {user.name}")
        
        except discord.Forbidden:
            print("User has DMs disabled.")

    @commands.command(name="Clear", description="Clears [int] amount of messages.", usage="clear [int]")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount : int):
        await ctx.channel.purge(limit=amount+1)
        embed = discord.Embed(title="Purged Message(s)!",  description=(f"Purged {amount} message(s)!"), color=0x31e30e)
        await ctx.send(embed=embed)
        await ctx.message.delete()
        
        embed1 = discord.Embed(title="Purged Message(s)!",  description=(f"Purged {amount} message(s) in channel <#{ctx.message.channel.id}>!"), color=0x31e30e)
        await ctx.send(embed=embed1)

def setup(client):
    client.add_cog(Moderation(client))