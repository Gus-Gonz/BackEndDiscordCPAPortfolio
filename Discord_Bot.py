import discord, random, string
from discord.ext import commands
import DB_Hand_Mongo
from config.config_discord import token_discord_bot ,your_discord_account_id , account_available_in_gen , website_link



# ---------------------------------- CHECKING STOCK ------------------------------------ #
Ava_com = account_available_in_gen

def In_stock(lista):
    with_stock = []
    out_stock = []
    for ele in lista:
        i = DB_Hand_Mongo.Check_DB(ele)
        if i != 0:
            with_stock.append(ele + ': ' + str(i) + ' \n')
        else:
            out_stock.append(ele + ': ' + str(i) + ' \n')
        # ---------------------------------- SE CREA EL STR PARA EL BOT ------------------------------------ #
    w_stock = ' '.join(with_stock)
    o_stock = ' '.join(out_stock)
    return [w_stock, o_stock]

# ---------------------------------- CLASS GEN STOCK ------------------------------------ #
class Gen_Stock ():
    def __init__(self,ctx,message):
        self.ctx = ctx
        self.message = message.lower()

    async def return_message (self,Ava_com):
        if self.message in Ava_com:
            Tipo = self.message
            Token = token_gen()
            Link_Gen = '  ' + str(Token)
            Acc_Ready = DB_Hand_Mongo.Ext_DB(Tipo, Token)
            if Acc_Ready != None:
                await self.ctx.send(embed=embed_m(self.ctx.author))
                try:
                    await self.ctx.author.send(embed=embed_dm(self.ctx.author, Token))
                    return True
                except:
                    await self.ctx.send(':x: Failed to create a DM Channel!, please check your privacy settings')
            else:
                await  self.ctx.send(':x: This account is not currently in stock , im really sorry :broken_heart:')
                return False
        else :
            await self.ctx.send(f":x: I don't recognice the command {self.ctx.author}")

# ---------------------------------- EMBED M ------------------------------------ #
def embed_m(author):
    embed_m = discord.Embed(title="I'm about to send you a DM {} with all the info needed".format(author),
                            description="Once you get the DM , please follow the instructions",
                            color=discord.Color.orange())
    # embed_m.set_thumbnail(url=url_img)
    return embed_m

# ---------------------------------- EMBED PRIVATE ------------------------------------ #
def embed_dm(author, Token):
    embed_dm = discord.Embed(title="Here is your account {}".format(author),
                             description="Please follow the instructions",
                             color=discord.Color.orange())
    embed_dm.add_field(name="Your Token", value=Token)  # AQUI VA EL LINK
    embed_dm.add_field(name='Instructions',
                       value='1) Go to {website} \n2)Put the token and Click in "SUBMIT" \n3) Complete 1 ad \n4) Congratulation you got a brand new account, ENJOY !!'.format(website_link))
    # embed_dm.set_thumbnail(url=url_img)
    return embed_dm

# ---------------------------------- Token Gen ------------------------------------ #
def token_gen(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# ---------------------------------- Prefix ------------------------------------ #
bot = commands.Bot(command_prefix='!!', description="EasyGen.xyz")  # el prefijo se establece aqui


# ------------------------------------ Ping -------------------------------------- #
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


# --------------------------------- DM with GEN ----------------------------------- #

@bot.command()
async def gen(ctx, message):
    message_gen = Gen_Stock(ctx,message)
    await message_gen.return_message(Ava_com)


# --------------------------------- HELPME ----------------------------------- #

@bot.command()
async def helpme(ctx):
    embed = discord.Embed(title="Commands", description="This is a list of all the command I accept")
    embed.add_field(name='!!gen <account>',
                    value=' It will send you a Token so you can take the account from our website ')
    embed.add_field(name='!!stock', value='It will tell you what accounts are currently in stock')

    await ctx.send(embed=embed)


# --------------------------------- STOCK ----------------------------------- #

@bot.command()
async def stock(ctx):
    embedd = discord.Embed(title=f"Stock", description="The following accounts are available",
                           color=discord.Color.orange())
    embedd.add_field(name=':white_check_mark: In stock', value=str(In_stock(Ava_com)[0] + '-------------------'))
    embedd.add_field(name=':x: Out of stock', value=str(In_stock(Ava_com)[1] + '-------------------'))
    await ctx.send(embed=embedd)


# --------------------------------- STOCK ----------------------------------- #

@bot.command()
async def addstock(ctx, message):
    if ctx.author.id == int(your_discord_account_id):
        getstock = message.split('>')
        tipo = getstock.pop(0)
        try:
            DB_Hand_Mongo.Add_DB(getstock, tipo)
            await ctx.send(':white_check_mark: We added {} row to the DB under the Type {}'.format(len(getstock), tipo))
        except:
            await ctx.send(':x:We had an issue adding the stock to the DB')
    else:
        await ctx.send(':x:You are not allow to use this command')


# --------------------------------- ERASE STOCK ----------------------------------- #

@bot.command()
async def delstock(ctx, message):
    if ctx.author.id == int(your_discord_account_id) :
        print(message)
        delstock = message.split('>')
        tipo = delstock.pop(0)
        # try:
        DB_Hand_Mongo.EraseFrom_DB(tipo, delstock[0])
        await ctx.send(':white_check_mark: We erased {} row to the DB under the Type {}'.format(delstock[0], tipo))
    # except:
    #	await ctx.send (':x:We had an issue erasing the stock of the DB')
    else:
        await ctx.send(':x:You are not allow to use this command')


# --------------------------------- Events ----------------------------------- #
@bot.event  # evento de inicio del bot
async def on_ready():
    await bot.change_presence(
        activity=discord.Game(platform='Pornhub', url='https://www.pornhubpremium.com/', name="Feel this baby"))
    print('THE BOT IS READY :>')



bot.run(token_discord_bot)
