import discord
from discord.ext import commands
from discord import Embed
from discord.ui import Button, View
import json
import random

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='$', intents=intents)
chat = "Disabled"

TOKEN = ""


@bot.event
async def on_ready():
    print("Bot has logged in.")

@bot.command()
async def enablechat(ctx):
    global chat
    chat = "Enabled"
    await ctx.send("Chat has been enabled")

@bot.command()
async def disablechat(ctx):
    global chat
    chat = "Disabled"
    await ctx.send("Chat has been disabled")

@bot.command()
async def explain(ctx):
    embed = discord.Embed(
        title="Dünyayı Nasıl Kurtarırız?", 
        description="Burada dünyayı kirlilikten kurtarmak için fikirler bulacaksınız. İyi okumalar :D",
        color=discord.Color.green()
        )
    
    embed.add_field(name="İnsanları uyarın", value="Sadece siz kirliğin zararını biliyorsanız ne işe yarar? İnsanlara bunun zararını anlatmaya çalışın, bir kişi bir kişidir, yine de yararı var.", inline=True)
    embed.add_field(name="Kendiniz de yapmayın!", value="İnsanları uyarın ancak bunu kendiniz yaparsanız kimse size inanmaz. Kendinizle çelişmeyin. Dünyayı koruyun", inline=True)
    embed.add_field(name="Bağış yapın!", value="Doğa için aksiyon alacak vaktiniz olmayabilir. Bunu sizin için yapan kurumlar var. Kurumları araştırın ve bağış yapın.", inline=True)
    embed.add_field(name="Sürdürülebilir ürünleri tercih edin", value="Plastik yerine yeniden kullanılabilir ürünleri tercih edin. Çevre dostu markaları destekleyerek daha az atık oluşturun.", inline=True)
    embed.add_field(name="Etkinliklere katılın!", value="Vakit bulabilirseniz ağaçlandırma veya doğayı temizleme etkinliklerine katılabilirsiniz.", inline=True)
    embed.add_field(name="Eğitimlere katılın!", value="Vakit bulabilirseniz geri dönüşüm ile alakalı veya doğayı korumayla alakalı eğitimlere katılabilirsiniz. Buradan daha detaylı anlatırlar :D", inline=True)
    
    embed.set_footer(text="xclsvity tarafından yapıldı")
    await ctx.send(embed=embed)

@bot.command()
async def embed(ctx):
    # Create an embed object
    embed = discord.Embed(
        title="Sample Embed",
        description="This is a detailed example of an embed in discord.py.",
        color=discord.Color.blue()
    )
    
    # Add fields to the embed
    embed.add_field(name="Field 1", value="This is the value for field 1.", inline=False)
    embed.add_field(name="Field 2", value="This is the value for field 2.", inline=True)
    embed.add_field(name="Field 3", value="This is the value for field 3.", inline=True)
    
    # Set a footer and thumbnail
    embed.set_footer(text="This is a footer")
    embed.set_thumbnail(url="https://example.com/thumbnail.png")
    
    # Set the author
    embed.set_author(name="Author Name", icon_url="https://example.com/icon.png")
    
    # Set a timestamp
    embed.timestamp = discord.utils.utcnow()

    # Send the embed
    await ctx.send(embed=embed)


bot.run(TOKEN)
