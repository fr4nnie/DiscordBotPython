# bot.py
import os, discord, asyncio, random, copy, time

from dotenv import load_dotenv
from discord.ext.commands import Bot
from discord.ext import commands

load_dotenv()           
TOKEN = os.getenv('DISCORD_TOKEN')  #load the .env file with the bot token in

intents = discord.Intents.all()     #allow all intents for bot, load bot and give it all intents
bot = commands.Bot(command_prefix='!', intents=intents) 


###############################################CONNECT AND TEST###############################################

#When ready and working, message to shell
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')  #fullusername
    print("I am running as: " + bot.user.name)      #shortname
    print("With the ID: " + str(bot.user.id))       #ID
    print('Bot is ready to be used and in the following guilds: ')
    for guild in bot.guilds:                        #gets and prints guild name and ID
        print(str(guild) + ": " + str(guild.id))    
        
    
#Test to ensure responce - USE bot.listen('on_message') as @bot.event async def on_message(message)stops commands working! make accept any case
@bot.listen() 
async def on_message(message):
    if message.author == bot.user: #if bot is the author do nothing
        return
    if message.content.lower() == 'test':
        await message.channel.send('Testing')


#Says hello if someone starts a message with hello in any		
@bot.listen()
async def on_message(message):
    if message.author == bot.user: #if bot is the author do nothing
        return
    if message.content.lower().startswith('hello'): #otherwise send the message to name of user i.e Superfran not Superfran#17823739827893
        await message.channel.send(f'Hello there {message.author.name} \nI hope you are having a nice day!')

        
###############################################GUILD EVENTS###############################################
		
#If someone joins guild
@bot.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general": #make sure sending the message to general 
            await channel.send(f"Welcome to the server {member.mention} please familiarise yourself with the rules and perhaps say hello to the other members!")
    print(f'{member.name} has joined the server {member.guild}: {member.guild.id}')
    

#If someone leaves guild
@bot.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "general": #make sure sending the message to general 
            await channel.send(f"Goodbye {member.mention} for they have left our little server!")
    print(f'{member.name} has left the server {member.guild}: {member.guild.id}')


#If someone changes their name
@bot.event
async def on_user_update(before, after):
    print("old nick: ", before.nick)
    print("new nick: ", after.nick)
#####GET THIS BIT working later if i can when i understand more - for now move forward##############
#    for channel in member.guild.channels:      
#        if str(channel) == "general":
#            await channel.send(f'Someone has changed their nickname {before.nick} to {after.nick}')


###############################################GUILD COMMANDS###############################################
    
#Output guild info (name, # members, owner)
@bot.command(name='server', help='Prints server information.')
async def serverInfo(ctx):
    guild = ctx.guild
    await ctx.send(f'Server Name: {guild.name}')
    await ctx.send(f'Server Size: {len(guild.members)}')
    await ctx.send(f'Server Owner: {guild.owner.display_name}')
    print('Server Info has been queried')


#Prints all members in a guild/server
@bot.command(name='members', help='Prints member list.')
async def serverMembers(ctx):
    guild = ctx.guild
    members = '\n - '.join([member.name for member in guild.members])
    await ctx.send(f'Guild Members:\n - {members}')
    print('Member list has been queried')


#member info (joined date) 
@bot.command(name='whois', help='Lookup member information example !whois @Name')
async def whoIs(ctx, *, member: discord.Member): #improve the format of joined date
    guild = ctx.guild
    print(f'{member.name} has been queried '.format(member))
    #think about making a command query - see if theres a way to also input the 2nd arguement sent
    await ctx.send(f'Member Username: {member.name} \nMember Nickname: {member.nick}'.format(member))
    await ctx.send(f'Member Joined at: {member.joined_at} \nMember\'s Status: {member.status}'.format(member))
    await ctx.send(f'Member\'s Avatar: {member.avatar_url}'.format(member))
    #improve the date/time format


#tableRoll d100 d20 d6 4 2 for tabletop style games
@bot.command(name='tableRoll', help='roll a dice by using !tableRoll d20 d6 d3 1 2 3 for example')
async def tblroll(ctx, *args): 
    rollList = []
    sumList = []
    await ctx.send('{} arguements: {}'.format(len(args), ' - '.join(args)))    #test the sent arguements and put them into the chat
    
    for each in args:
        if each.lower().startswith("d"):        #if it starts with a D/d
            listItem = int(each[1:])            #attempting to remove the D/d at the start and convert it to an integer if it isnt
            rollList.append(listItem)           #and add it to rollList so that i can use it for a roll later - is this by copy or by reference?) 
        if not each.lower().startswith("d"):    #if it doesnt start with a D 
            if each.isdecimal():                #and is a decimal
                sumItem = int(each)             #make it an int
                sumList.append(sumItem)         #put in list called sumList

    #TO DO: if any each in args is not a D d or decimal: 

    for dice in rollList:                   #random roll from 1 to number for each in rolllist
        random.seed(time.time())
        roll = random.randint(1, dice)
        print(f'dice to roll is {dice}')
        print(f'roll for this dice is {roll}')
        print('\n')
        sumList.append(roll)                #add this random to sumList

    results = sum(sumList)  #work out the total
    await ctx.send(f'The total of each dice roll plus any modifiers is {results}')   
    print(*args)            #print to console full list given
    print(*sumList)
    print(f'sum = {results}')  


#TO DO: add loot roll, simple 1 to X
@bot.command(name='roll', help='!roll 100 will make a simple quickroll from a given whole number')
async def quickroll(ctx, droll: int):
    random.seed(time.time())
    troll = random.randint(1, droll)
    await ctx.send(f'Out of {droll} you have rolled {troll}')


#TO DO: command lookup in English (word defenition) 



###############################################WILL BE MAIN###############################################

bot.run(TOKEN) #run the bot

