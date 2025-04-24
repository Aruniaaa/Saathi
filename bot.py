
import discord
from discord.ext import commands
import random
import asyncio
import logging
from dotenv import load_dotenv
import os
from bad_words import bad_words

load_dotenv()
token = os.getenv("DISCORD_BOT_TOKEN")




mod_role = '🦋 .  Moderator'
trial_mod_role = '🪶  .  Trial Mod'
admin_role = '🛠️﹒Admin'
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.all()
intents.message_content = True  
intents.members  = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.event
async def on_member_join(member):
     await member.send(f"Hey {member.name}! Welcome to the server, have fun, make new friends, and follow the rules!")

@bot.event
async def on_message(message):
     if message.author == bot.user:
          return
     for word in bad_words:
      if word in message.content.lower():
          await message.delete()
          await message.channel.send(f"{message.author.mention} please avoid from using bad language and let's keep this clean!")
     await bot.process_commands(message)

@bot.event
async def on_member_remove(member):
     await member.send(f"We are sad to see you go, {member.name}. Hope you enjoyed your stay.")



@bot.command()
@commands.has_role(admin_role)
async def makemod(ctx):
    await ctx.send("Please mention the user you want to assign the mod role to.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.mentions:
            member = msg.mentions[0]
            role = discord.utils.get(ctx.guild.roles, name=mod_role)
            if role:
                await member.add_roles(role)
                await ctx.send(f"{member.mention} is now assigned the {mod_role} role!")
            else:
                await ctx.send("Mod role doesn't exist!")
        else:
            await ctx.send("You need to mention a user!")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")


@bot.command()
@commands.has_role(admin_role)
async def maketrialmod(ctx):
    await ctx.send("Please mention the user you want to assign the trial mod role to.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.mentions:
            member = msg.mentions[0]
            role = discord.utils.get(ctx.guild.roles, name=trial_mod_role)
            if role:
                await member.add_roles(role)
                await ctx.send(f"{member.mention} is now assigned the {trial_mod_role} role!")
            else:
                await ctx.send("Mod role doesn't exist!")
        else:
            await ctx.send("You need to mention a user!")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")



@bot.command()
@commands.has_role(admin_role)
async def removemod(ctx):
    await ctx.send("Please mention the user you want to remove the mod role from.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.mentions:
            member = msg.mentions[0]
            role = discord.utils.get(ctx.guild.roles, name=mod_role)
            if role:
                await member.remove_roles(role)
                await ctx.send(f"{member.mention} has had the {mod_role} role removed!")
            else:
                await ctx.send("Mod role doesn't exist!")
        else:
            await ctx.send("You need to mention a user!")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")

@bot.event
async def on_command_error(ctx, error):
            if isinstance(error, commands.MissingRequiredArgument):
                await ctx.send("⚠️ You missed a required argument. Please check the command usage.")
            elif isinstance(error, commands.MissingRole):
                await ctx.send("⛔ You don't have the required role to use this command.")
            elif isinstance(error, commands.CommandNotFound):
                await ctx.send("❓ This command does not exist. Use `!help` to see the available commands.")
            elif isinstance(error, commands.BadArgument):
                await ctx.send("❌ Invalid argument provided. Please check the command usage.")
            elif isinstance(error, commands.CommandInvokeError):
                await ctx.send("⚙️ An error occurred while executing the command. Please try again later.")
            elif isinstance(error, asyncio.TimeoutError):
                await ctx.send("⏳ You took too long to respond. Please try again.")
            else:
                await ctx.send("🚨 An unexpected error occurred. Please contact the admin.")
            # Optionally log the error for debugging
            logging.error(f"Error in command {ctx.command}: {error}")


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Help", description="List of available commands:")
    embed.add_field(name="!hello", value="Greets the user.", inline=False)
    embed.add_field(name="!rps", value="Play rock, paper, scissors with the bot.", inline=False)
    embed.add_field(name="!flames", value="Check your compatibility with someone using FLAMES.", inline=False)
    embed.add_field(name="!love_calc", value="Calculate your love percentage with someone.", inline=False)
    embed.add_field(name="!dice_roll", value="Roll a dice.", inline=False)
    embed.add_field(name="!math", value="Solve a random math question.", inline=False)
    embed.add_field(name="!poll <question>", value="Create a poll with a question.", inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_role(admin_role)
async def removetrialmod(ctx):
    await ctx.send("Please mention the user you want to remove the trial mod role from.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for("message", check=check, timeout=30)
        if msg.mentions:
            member = msg.mentions[0]
            role = discord.utils.get(ctx.guild.roles, name=trial_mod_role)
            if role:
                await member.remove_roles(role)
                await ctx.send(f"{member.mention} has had the {trial_mod_role} role removed!")
            else:
                await ctx.send("Mod role doesn't exist!")
        else:
            await ctx.send("You need to mention a user!")
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond!")

    

# hello command
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hey {ctx.author.mention}!')


# rock paper scissors
@bot.command()
async def rps(ctx):
    await ctx.send("rock, paper, or scissors?")

    def check(m):
         return m.author == ctx.author and m.channel == ctx.channel
    try:
         msg = await bot.wait_for("message", check=check, timeout=15)
         user_choice = msg.content.lower()
    except asyncio.TimeoutError:
         await ctx.send("Timeout error! Please choose as soon as possible next time!")



    options = ['rock', 'paper', 'scissors']
    user_choice = user_choice.lower()  # Make sure it's lowercase for consistency
    
    if user_choice not in options:
        await ctx.send("Invalid choice! Please choose 'rock', 'paper', or 'scissors'.")
        return

    bot_choice = random.choice(options)  # Bot chooses randomly
    await ctx.send(f'You chose {user_choice} and I chose {bot_choice}.')

    # Game logic
    if user_choice == bot_choice:
        await ctx.send("It's a draw!")
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'paper' and bot_choice == 'rock') or \
         (user_choice == 'scissors' and bot_choice == 'paper'):
        await ctx.send("You win! 🎉")
    else:
        await ctx.send("You lose! 😭")


# FLAMES
@bot.command()
async def flames(ctx):
    await ctx.send("enter your name ")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    try:
            msg = await bot.wait_for("message", check=check, timeout=30)  
            your_name = msg.content.lower()

    except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")


    await ctx.send("enter their (your crush's) name")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    try:
            msg = await bot.wait_for("message", check=check, timeout=30)  
            their_name = msg.content.lower()

    except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")



    lst = []
    flames = ['f', 'l', 'a', 'm', 'e', 's'] # friend, love, affection, marry, enemies, siblings

    your_name = list(your_name)
    their_name = list(their_name)

    for i in your_name[:]:
        if i in their_name:
             your_name.remove(i)
             their_name.remove(i)
 

    for i in range(len(your_name)):
            lst.append(1)
    for i in range(len(their_name)):
            lst.append(1)
    lst = sum(lst)


    index = 0  
    while len(flames) != 1:
         index = (index + lst - 1) % len(flames)
         flames.pop(index)

       

    if 'm' in flames:
          await ctx.send(f"You two got 'M' which means marry!!! 💍")
    elif 'f' in flames:
         await ctx.send(f"You two got 'F' which means friendship!!! 🤝")
    elif 'l' in flames:
          await ctx.send(f"You two got 'L' which means love!!! ❤️")
    elif 'a' in flames:
          await ctx.send(f"You two got 'A' which means attraction!!! 💘")
    elif 'e' in flames:
          await ctx.send(f"You two got 'E' which means enemies!!! 💢")
    elif 's' in flames:
          await ctx.send(f"You two got 's' which means siblings!!! 🍜")
      
# love calculator
@bot.command()
async def love_calc(ctx):    
    await ctx.send("enter your name ")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    try:
            msg = await bot.wait_for("message", check=check, timeout=30)  
            your_name = msg.content.lower()

    except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")


    await ctx.send("enter their (your crush's) name ")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


    try:
            msg = await bot.wait_for("message", check=check, timeout=30)  
            their_name = msg.content.lower()

    except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")

    try:    
     lst = [] 
     your_name = your_name.lower()
     their_name = their_name.lower()
     your_name = list(your_name)
     their_name = list(their_name)

     for i in your_name[:]:
            if i in their_name:
                your_name.remove(i)
                their_name.remove(i)
                lst.append(2)

     for i in range(len(your_name)):
            lst.append(1)
     for i in range(len(their_name)):
            lst.append(1)
     def reduce_list(lst):
       new = []
       left = 0
       right = len(lst) - 1

       while left < right:
        new.append(lst[left] + lst[right])
        left += 1
        right -= 1

       if left == right:
        new.append(lst[left])  
       return new


     while len(lst) > 2:
            lst = reduce_list(lst)

     await ctx.send(f"Your love percentage is {lst[0]}{lst[1]}% ❤️")
     # this is the end of the love_calc function
    except Exception as e:
         await ctx.send(e)


# dice roll
@bot.command()
async def dice_roll(ctx): 
    while True:
      await ctx.send("Roll the dice? (y/n)")

      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel


      try:
            msg = await bot.wait_for("message", check=check, timeout=30)  
            cmd = msg.content.lower()

            if cmd in ['y', 'yes']:
                num1 = random.randint(1, 6)
                await ctx.send(f"The number you rolled is {num1}")
                break  
            elif cmd in ['n', 'no']:
                await ctx.send("Thanks for playing!")
                break  
            else:
                await ctx.send("Please enter a valid command! (y/n)")
      except asyncio.TimeoutError:
            await ctx.send("You took too long to respond!")
            break



@bot.command()
async def math(ctx):
     await ctx.send("please enter a maximum number range for the question")

     def check(m):
          return m.author == ctx.author and m.channel == ctx.channel
     try:
        msg = await bot.wait_for("message", check=check, timeout=30)  
        max_range = msg.content.lower()
        max_range = int(max_range)
     except asyncio.TimeoutError:
          await ctx.send("Please enter a maximum range faster next time!")

     
     operations = ["+", "-", "/", "*"]


     num1 = random.randint(1, max_range)
     num2 = random.randint(1, max_range)
     operation = random.choice(operations)
     if operation == "+":
         correct_answer = num1 + num2
     elif operation == "-":
         correct_answer = num1 - num2
     elif operation == "/":
         correct_answer = num1 / num2
     elif operation == "*":
         correct_answer = num1 * num2



     await ctx.send(f"{num1} {operation} {num2} = ?")

     def check(m):
          return m.author == ctx.author and m.channel == ctx.channel
     try:
        msg = await bot.wait_for("message", check=check, timeout=30)  
        answer = msg.content.lower()
        answer = int(answer)
     except asyncio.TimeoutError:
          await ctx.send("Please enter a maximum range faster next time!")



        
     if answer == correct_answer:
            await ctx.send(f"Your answer ({answer}) is correct!")
     else:
            await ctx.send(f"Your answer ({answer}) is incorrect!")


@bot.command()
async def poll(ctx, *, question):
     embed = discord.Embed(title=f"Poll made by {ctx.author}", description=question)
     poll_message = await ctx.send(embed=embed)
     await poll_message.add_reaction("👍")
     await poll_message.add_reaction("👎")
    

# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG )

