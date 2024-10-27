import discord
from discord.ext import commands
from discord import Embed
from discord.ui import Button, View
import json
import random
import string
import unicodedata
import asyncio


# Botun token'ı
TOKEN = ''

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='$', intents=intents)
ADMIN_ROLE = "administrator"



def generate_password(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def save_applications(applications):
    data_to_save = []
    for app in applications:
        if app['user_id'] is not None:
            data_to_save.append({'user_id': app['user_id'], 'role': app['role']})
        else:
            print(f"Application could not be saved, user not found: {app}")
    with open('applications.json', 'w', encoding='utf-8') as file:
        json.dump(data_to_save, file, ensure_ascii=False)

def load_applications(guild):
    try:
        with open('applications.json', 'r', encoding='utf-8') as file:
            apps = json.load(file)
            return [{'user_id': app['user_id'], 'role': app['role'], 'user': guild.get_member(app['user_id'])} for app in apps]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []





@bot.event
async def on_ready():
    print(f'Bot logged in as {bot.user.name}.')


@bot.command()
async def mem(ctx):
    with open('OIP.jpeg', 'rb') as img:
        pict = discord.File(img)
    await ctx.send(file=pict)
    

# Ticket açma butonu
class TicketButton(View):
    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green)
    async def ticket_button(self, button: Button, interaction: discord.Interaction):
        # Ticket kanalını oluştur
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name='Tickets')
        
        if category is None:
            category = await guild.create_category('Tickets')

        ticket_channel = await guild.create_text_channel(f'ticket-{interaction.user.name}', category=category)

        # Kanal izinlerini ayarla
        await ticket_channel.set_permissions(guild.default_role, read_messages=False)  # Herkese kapat
        await ticket_channel.set_permissions(interaction.user, read_messages=True)  # Açan kullanıcıya aç
        admin_role = discord.utils.get(guild.roles, name=ADMIN_ROLE)
        if admin_role:
            await ticket_channel.set_permissions(admin_role, read_messages=True)  # Admin rolüne aç

        # Embed ile bilgi mesajı gönder
        embed = discord.Embed(title="Ticket Information", description="Welcome to your ticket! Please explain your issue or request below.\n\n**Rules:**\n1. Be respectful.\n2. No spamming.\n3. Only open one ticket at a time.")
        await ticket_channel.send(embed=embed)

        # Kapatma butonu ekle
        close_button = Button(label="Close Ticket", style=discord.ButtonStyle.red)

        async def close_callback(close_interaction: discord.Interaction):
            await ticket_channel.send("This ticket has been closed.")
            await ticket_channel.delete()

        close_button.callback = close_callback
        view = View()
        view.add_item(close_button)

        await ticket_channel.send(f"{interaction.user.mention}, your ticket has been created!", view=view)



# Ticket açma kanalı
@bot.command(name='ticket_channel')
@commands.has_role(ADMIN_ROLE)
async def ticket_channel(ctx):
    category = discord.utils.get(ctx.guild.categories, id=1297612572866121819)
    channel = await ctx.guild.create_text_channel('ticket-system', category=category)
    
    embed = discord.Embed(title="Ticket System", description="Click the button below to open a ticket.")
    await channel.send(embed=embed, view=TicketButton())




@bot.command(name='feedback')
async def feedback(ctx, *, feedback_message: str):
    """Kullanıcılardan geri bildirim toplar ve belirli bir kanalda adminlere gönderir."""
    feedback_channel_id = 1272834512296087603  # Admin geri bildirim kanalı ID'si
    feedback_channel = bot.get_channel(feedback_channel_id)
    if feedback_channel is not None:
        await feedback_channel.send(f"New feedback:\n{feedback_message}\n- Sent by: {ctx.author}")
        await ctx.send("Your feedback has been successfully sent!" )
    else:
        await ctx.send("Feedback channel not found." )





@bot.command(name='close')
async def close(ctx):
    global admin_channel_id, admin_channel_creator_id
    if ctx.author.id != admin_channel_creator_id:
        await ctx.send("This command can only be used by the channel creator." )
        return
    
    if admin_channel_id is None:
        await ctx.send("There is currently no open admin channel." )
        return

    guild = ctx.guild
    admin_channel = guild.get_channel(admin_channel_id)
    
    if admin_channel is not None:
        await admin_channel.delete()
        admin_channel_id = None
        admin_channel_creator_id = None  # Kanal kapatıldığında yaratıcının ID'sini de sıfırla
        await ctx.author.send(f"The channel with the passwordhas been closed.")
    else:
        await ctx.send("No channel to close was found.")





@bot.command(name='cmds')
async def cmds(ctx):
    commands_list = [
        {'name': 'add', 'description': 'Sends a request to add a new word.', 'roles': []},
        {'name': 'password', 'description': 'Creates an admin panel and sends the password.', 'roles': [ADMIN_ROLE]},
        {'name': 'requests', 'description': 'Lists all word addition requests.', 'roles': [ADMIN_ROLE]},
        {'name': 'accept', 'description': 'Accepts a word addition request.', 'roles': [ADMIN_ROLE]},
        {'name': 'decline', 'description': 'Declines a word addition request.', 'roles': [ADMIN_ROLE]},
        {'name': 'langlist', 'description': 'Lists the words and definitions in the dictionary.', 'roles': []},  # Public
        {'name': 'cmds', 'description': 'Lists all commands and their descriptions.', 'roles': []},  # Public
        {'name': 'passes', 'description': 'Lists passwords for admin channels.', 'roles': [ADMIN_ROLE]},  # Admin command
        {'name': 'apply', 'description': 'Applies and records the application with the role name.', 'roles': []},  # Public
        {'name': 'applications', 'description': 'Shows approved and declined applications.', 'roles': [ADMIN_ROLE]},  # Admin command
        {'name': 'approved', 'description': 'Approves applications by user ID.', 'roles': [ADMIN_ROLE]},  # Admin command
        {'name': 'declined', 'description': 'Declines applications by user ID.', 'roles': [ADMIN_ROLE]},  # Admin command
        {'name': 'feedback', 'description': 'Collects feedback and sends it to admins.', 'roles': []},  # Public
        {'name': 'close', 'description': 'Closes the currently open admin channel.', 'roles': [ADMIN_ROLE]}  # Admin command
    ]

    embed = Embed(title="Command List", color=discord.Color.blue())
    
    for command in commands_list:
        roles = ', '.join(command['roles']) if command['roles'] else 'Public'
        embed.add_field(name=f"${command['name']}", value=f"{command['description']}\nUser Roles: {roles}", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name='apply')
async def apply(ctx):
    """Başvuru yapar ve rol adı ile başvuru kaydeder."""
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send("Please choose the role you want to apply for: `word adder` or `administrator`.")
    
    try:
        role_message = await bot.wait_for('message', timeout=120.0, check=check)
        role_name = role_message.content.strip().lower()
        
        if role_name not in ['word adder', 'administrator']:
            await ctx.send("Please choose one of the roles: `word adder` or `administrator`.")
            return
        
        applications = load_applications(ctx.guild)
        
        if any(app['user_id'] == ctx.author.id for app in applications):
            await ctx.send("You already have an application.")
            return
        
        applications.append({
            'user_id': ctx.author.id,
            'role': role_name
        })
        
        save_applications(applications)
        await ctx.send(f"Your application for the `{role_name}` role has been received.")
    
    except asyncio.TimeoutError:
        await ctx.send("The application period has expired. Your application was not received.")

@bot.command(name='applications')
async def applications(ctx):
    """Onaylanmış ve reddedilmiş başvuruları gösterir."""
    if ADMIN_ROLE not in [role.name for role in ctx.author.roles]:
        await ctx.send("You do not have permission to use this command.")
        return
    
    applications = load_applications(ctx.guild)
    if not applications:
        await ctx.send("There are no applications yet.")
        return

    response = "Applications:\n"
    for idx, app in enumerate(applications):
        user = ctx.guild.get_member(app['user_id'])
        user_name = user.name if user else "Unknown"
        response += f"{idx + 1}: {app['user_id']} ({user_name}) - Role: {app['role']}\n"
    await ctx.send(response)

@bot.command(name='approved')
@commands.has_role(ADMIN_ROLE)
async def approved(ctx, user_id: int):
    """Approves an application by user ID."""
    applications = load_applications(ctx.guild)
    
    application = next((app for app in applications if app['user_id'] == user_id), None)

    if not application:
        await ctx.send("Application not found.")
        return

    user = ctx.guild.get_member(user_id)
    role = discord.utils.get(ctx.guild.roles, name=application['role'])

    if user and role:
        await user.add_roles(role)
        await ctx.send(f"Application approved: {user.id} ({user.name}) role added.")
        applications.remove(application)
        save_applications(applications)
    else:
        await ctx.send("Application or role not found.")


@bot.command(name='declined')
@commands.has_role(ADMIN_ROLE)
async def declined(ctx, user_id: int):
    """Declines an application by user ID."""
    applications = load_applications(ctx.guild)
    
    application = next((app for app in applications if app['user_id'] == user_id), None)

    if not application:
        await ctx.send("Application not found.")
        return

    # Remove the application
    applications.remove(application)
    save_applications(applications)
    await ctx.send(f"Application declined: {user_id}.")





bot.run(TOKEN)



MTI0Njc2NDczMDk4MzUxNDIwMw.G3fwzQ.Yx8kWn8visY3kCWrcN-lzJZNck8yfz9j5qMLyg