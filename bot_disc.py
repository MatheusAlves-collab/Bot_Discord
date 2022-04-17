import discord

from discord.ext import commands,tasks

#import youtube_dl as YoutubeDL

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

# Links
url_code = 'https://codenames.game/room/create'

#import https://discord.com/developers/applications

#client = discord.Client()

Bot1 = commands.Bot(command_prefix='$')

TOKKEN = 'YOUR_OWN_TOKKEN'
GUILD = 'Matheus teste'

# Verificando nome do servidor que o bot esta conectado
@Bot1.event
async def on_ready():
    for guild in Bot1.guilds:
        #if guild.name == 'Matheus teste':
        #print(guild.name)
        print(f'{Bot1.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}\n')

# mensagem teste
@Bot1.command()
async def ping(ctx):
	await ctx.channel.send("pong")

# mensagens de Olá
@Bot1.event
async def on_message(message):
    if message.author == Bot1.user:
        return
    if message.content.startswith(('$Oi','$Olá','$Ola', '$Alô','$oi','$olá', '$ola', '$alô')):
        await message.channel.send('Olá amigo !!!')
    if message.content.startswith(('$Hi','$Hello', '$hi','$hello')):
        await message.channel.send('Hello friend !!!')
    await Bot1.process_commands(message)

# comando de criar sala codenames, so funciona no pc do adm
@Bot1.command()
async def codenames(ctx):
    user_id = ctx.author.id
    user1 = await Bot1.fetch_user(user_id)
    await ctx.send(str(user1) + " está criando sala...",file = discord.File('codenames.jpg'))
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options=options,service=Service(ChromeDriverManager().install()))
    sleep(3)

    driver.get(url_code)
    sleep(2)

    driver.find_element(by='id', value = "nickname-input").send_keys('Matheus')
    sleep(1)

    # botao selecionar linguagem
    driver.find_element_by_xpath("//*[@id='__next']/main/section/section[1]/main").click()
    sleep(1)

    # botao selecionar portugues
    driver.find_element_by_xpath("//*[@id='__next']/main/section/section[1]/main/section/section/article[16]/div/div/div").click()
    sleep(1)

    # botao criar sala
    driver.find_element_by_xpath("//*[@id='__next']/main/section/section[1]/div/section/button").click()
    sleep(9)

    # botao liguagem sala
    driver.find_element_by_xpath("//*[@id='layoutRoot']/div[2]/main/section[1]/div/header/div/main/button/div/p").click()
    sleep(1)

    # botao liguagem sala portugues
    driver.find_element_by_xpath("//*[@id='scaledModals']/section/section/button[32]/div/div/div").click()
    sleep(1)

    #criar jogo
    driver.find_element_by_xpath("//*[@id='layoutRoot']/div[2]/main/section[2]/div[2]/button").click()
    sleep(2)

    url_nova = driver.current_url
    await ctx.send("Sala criada: "+ url_nova)
    
#Bem vindo
@Bot1.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Olá {member.name}, bem vindo ao discord de Teste do Matheus!'
    )

Bot1.run(TOKKEN)

