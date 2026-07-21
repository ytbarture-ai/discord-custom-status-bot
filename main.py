import discord
from discord.ext import commands, tasks
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
# On peut toujours écraser le statut principal via TEXT_STATUS si besoin
CUSTOM_STATUS = os.getenv("TEXT_STATUS", "RecRDZ v0.2.0")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(seconds=10)
async def change_status():
    # Liste des statuts à alterner
    statuses = [
        discord.CustomActivity(name="Version 1.0.0"),
        discord.Game(name=CUSTOM_STATUS)
    ]
    
    for status in statuses:
        await bot.change_presence(activity=status, status=discord.Status.online)
        await asyncio.sleep(5) # Attend 5 secondes avant de passer au suivant dans la boucle interne

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")
    print(f"ID : {bot.user.id}")
    if not change_status.is_running():
        change_status.start()
    print("Boucle de statuts démarrée !")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def main():
    if not TOKEN:
        print("ERREUR : La variable d'environnement DISCORD_TOKEN est manquante !")
        return
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
