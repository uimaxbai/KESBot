from keep_alive import keep_alive
import discord
import discord.ext
from discord.ext import commands
from discord.commands import Option
import os
import requests
import json
import datetime
from random import randint
# ^^ All of our necessary imports

#Define our bot
bot = commands.Bot()
weather_token = os.environ['WEATHER_API_KEY']

def mailgun_send(email_address, verification_code):
	return requests.post(
		"https://api.mailgun.net/v3/{}/messages".format(os.environ.get('MAILGUN_DOMAIN')),
		auth=("api", os.environ.get('MAILGUN_API_KEY')),
		data={"from": "KESBot <mailgun@{}>".format(os.environ.get('MAILGUN_DOMAIN')),
			"to": email_address,
			"subject": "Verify your server email",
			"text": "Please verify your identity by posting the following code below:\n"+str(verification_code)})

def email_check(email):
  if email.find("@kes.net") != -1:
    code= randint(100000,999999)
    mailgun_send(email, code)
  elif email.find("@kes.net") == -1:
    return 404
  else:
    return 403
    
@bot.event
async def on_ready():
    code = -1
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name='KESBot | /help | /kes')
    )  #Bot status, change this to anything you like
    print("Bot online"
          )  #will print "bot online" in the console when the bot is online


#Send message "pong" when user sends /ping
@bot.slash_command(name="kes", description="KESBot is here!")
async def kes(ctx):
    await ctx.respond(content="Hi! I'm still here")


# Space given text by user
@bot.slash_command(name="fact", description="Make me say a cool fact")
async def fact(ctx):
    limit = 1
    api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
    facttoken = os.getenv('ninjatoken')
    response = requests.get(api_url, headers={'X-Api-Key': facttoken})
    if response.status_code == requests.codes.ok:
        original = response.text
        parsed = original.replace('''[{"fact": "''', "")
        original = parsed
        parsed = original.replace('''"}]''', "")
        embed = discord.Embed(title="Your cool fact",
                              color=0xebb907,
                              timestamp=datetime.datetime.now(),
                              description=parsed)
        embed.set_author(
            name="KESBot's FACTS",
            icon_url=
            '''https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L'''
        )
        embed.set_footer(text="That was cool, right???")
        await ctx.respond(embed=embed)
        chance = randint(1, 4)
        if chance == 2:
            await ctx.respond("*What???*")
    else:
        await ctx.respond("Error:", response.status_code, response.text)


@bot.slash_command(name="joke", description="Gimme a joke man")
async def joke(ctx):
    facttoken = os.getenv('ninjatoken')
    response = requests.get('https://api.api-ninjas.com/v1/jokes?limit=1',
                            headers={'X-Api-Key': facttoken})
    original = response.text
    parsed = original.replace('''[{"joke": "''', " ")
    original = parsed
    parsed = original.replace('''"}]''', "")
    original = parsed.replace("\n\n", "")
    embed = discord.Embed(title="Your joke",
                          color=0xebb907,
                          timestamp=datetime.datetime.now(),
                          description=original)
    embed.set_author(
        name="KESBot's lame jokes",
        icon_url=
        "https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L"
    )
    embed.set_footer(text="😬 You cringed, right?")
    await ctx.respond(embed=embed)


@bot.slash_command(name="quote", description="A cool Zen quote")
async def quote(ctx):
    response = requests.get("https://zenquotes.io/api/random/")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    author = json_data[0]['a']
    embed = discord.Embed(title="Your quote.",
                          color=0xebb907,
                          timestamp=datetime.datetime.now())
    embed.set_author(
        name="KESBot's Zen Quotes",
        icon_url=
        '''https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L'''
    )
    embed.add_field(name=f"**'{quote}'**", value=f"- {author}", inline=False)
    embed.set_footer(text="Hey, like a good quote!")
    await ctx.respond(embed=embed)


@bot.slash_command(name="help", description="When all else fails")
async def help(ctx):
    embed = discord.Embed(title="Help:",
                          description='Stop it, get some help',
                          timestamp=datetime.datetime.now(),
                          color=0xebb907)
    embed.set_author(
        name="KESBot Help",
        icon_url=
        "https://drive.google.com/uc?export=download&id=1dx4JTP4dK97GY7sDmaqnntK7-manXx0L"
    )
    embed.add_field(name="/help",
                    value="Displays this help menu.",
                    inline=False)
    embed.add_field(name="/kes", value="Tests the KESBot.", inline=False)
    embed.add_field(name="/quote", value="Gives you a quote.", inline=False)
    embed.add_field(name="/fact",
                    value="Gives out a very cool fact.",
                    inline=False)
    embed.add_field(name="/joke",
                    value="Gives out a very lame joke.",
                    inline=False)
    chance = randint(1, 4)
    if chance == 1:
        text = "🤔 What is the meaning of life?"
    elif chance == 2:
        text = "plz help me...i need help plzz 😭"
    else:
        text = "Stop it, get some help"
    embed.set_footer(text=text)
    await ctx.respond(embed=embed)



@bot.slash_command(name="verify", description="Verifies that you are from KES.")
async def verify(
  ctx: discord.ApplicationContext, 
  user: discord.Member,
  email: Option(str, 
    "email", 
    required = True, 
    default = ''
  )
):
  role = discord.utils.get(ctx.guild.roles, name="Verified")
  if role in user.roles:
    await ctx.respond("You/he/she/they have already been verified!!!!1!111!")
  else:
    email_check(email)
    if email_check == 404:
      await ctx.respond("Incorrect email. Check that it has a @kes.net at the end")
    elif email_check == 403:
      await ctx.respond("Something went wrong. Please try again after a few minutes.")
    elif email_check == 402:
      await ctx.respond("Something went wrong. Please try again after a few minutes.")
    elif email_check == 200:
      await ctx.respond("Email sent to your inbox. Please check your spam for the code and type it in here.")


@bot.slash_command(name="weather", description="Find the weather in a certain place")
async def weather(ctx, place: discord.Option(str)):
  response = requests.request("GET", f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{place}?unitGroup=metric&key={weather_token}&contentType=json")
  jsonData = response.json()
  if response.status_code!=200:
    await ctx.respond('Unexpected Status code: ', response.status_code)


#Run our webserver, this is what we will ping
keep_alive()

#Run our bot
token = os.getenv("discordtoken")
bot.run(token)
