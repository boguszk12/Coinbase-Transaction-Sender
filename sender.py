import time,discord,requests,os,asyncio,json,imaplib,aiohttp,email
from random import choice                         
from discord.ext import commands,tasks
from discord.utils import get
from coinbase.wallet.client import Client
from discord import Permissions
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString, Tag

#@commands.has_any_role('Admin','Support')

static_role = 'Support'
notification_channel = 
owner_id = 
api_key,api_secret = '', '' #coinbase api keys

client = commands.Bot(command_prefix= 'cbs.')      
client2 = Client(api_key, api_secret)


@client.event  
async def on_ready():                  
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Sending Crypto!"))
    print('Ready for Sending!')

@commands.has_any_role(static_role)
@client.command()
async def balance(ctx):
    await ctx.channel.purge(limit=1)
    user = client2.get_current_user()
    request = client2.get_primary_account()
    chec = discord.Embed(
        title=f"Your account" , 
        description=f"Here are the details",
        colour = discord.Colour.from_rgb(239,21,21))
    chec.set_author(name= user['email'], icon_url=user['avatar_url'])
    chec.add_field(name='Crypto balance:',value=f"`{request['balance']['amount']} {request['balance']['currency']}`",inline = False)
    chec.add_field(name='Fiat balance:',value=f"`{request['native_balance']['amount']} {request['native_balance']['currency']}`",inline = False)
    chec.set_footer(text =f"Thanks for using our services!" )
    await ctx.channel.send(embed = chec, content = None)

@client.command()
async def comm(ctx):
    chec = discord.Embed(
        title=f"Help" , 
        description=f"Get all of your commands",
        colour = discord.Colour.from_rgb(239,21,21))
    chec.add_field(name='Sending crypto',value=f"`cbs.send [amount] [wallet email/address] [currency]`",inline = False)
    chec.add_field(name='Checking balance:',value=f"`cbs.balance`",inline = False)
    chec.add_field(name='Online:',value=f"`cbs.run`",inline = False)
    chec.set_footer(text =f"Thanks for using our services!" )
    await ctx.channel.send(embed = chec, content = None)

@commands.has_any_role(static_role)
@client.command()
async def send(ctx,amount,to,currency):
    try:
        request = client2.send_money(client2.get_primary_account()['id'],to=to,amount=amount,currency=currency)
        se = discord.Embed(
            title=f"Transaction sent" , 
            description=f"Processing request...",
            colour = discord.Colour.from_rgb(239,21,21))
        se.add_field(name='Crypto amount:',value=f"`{request['amount']['amount']} {currency}`",inline = False)
        se.add_field(name='Fiat amount:',value=f"`{request['native_amount']['amount']} {request['native_amount']['currency']}`",inline = False)
        se.add_field(name='Status:',value=f"`{request['network']['status_description']}`",inline = False)
        se.add_field(name='Link:',value=f"[Here]({request['to']['address_url']})",inline = False)
        se.set_footer(text =f"Thanks for using our services!" )
        await ctx.channel.send(embed = se, content = None)
    except Exception as e:
        exe = discord.Embed(
            title=f"Error Occured" , 
            description=f"{str(e).split(':')[-1]}",
            colour = discord.Colour.from_rgb(239,21,21))
        exe.set_footer(text =f"Thanks for using our services!" )
        await ctx.channel.send(embed = exe, content = None)

@client.command()
async def run(ctx):
    await ctx.channel.send('Running')
                    

client.run('')       #token bot
