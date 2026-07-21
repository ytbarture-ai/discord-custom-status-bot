import discord
from discord.ext import commands, tasks
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
# Variable pour le statut personnalisé (ex: Version 1.0.0)
STATUS_1 = os.getenv("TEXT_STATUS", "Version 1.0.0")
# Variable pour le statut "Joue à" (ex: RecRDZ v0.2.0)
STATUS_2 = os.getenv("TEXT_STATUS2", "RecRDZ v0.2.0")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(seconds=10)
async def change_status():
    # Liste des statuts à alterner (tous en CustomActivity)
    statuses = [
        discord.CustomActivity(name=STATUS_1),
        discord.CustomActivity(name=STATUS_2)
    ]
    
    for status in statuses:
        await bot.change_presence(activity=status, status=discord.Status.online)
        await asyncio.sleep(5) # Attend 5 secondes avant de passer au suivant

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")
    print(f"ID : {bot.user.id}")
    print(f"Statut 1 : {STATUS_1}")
    print(f"Statut 2 (Joue à) : {STATUS_2}")
    if not change_status.is_running():
        change_status.start()
    print("Boucle de statuts alternés démarrée !")

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
