import discord
from discord.ext import commands, tasks
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")

# Récupération dynamique de 12 statuts (TEXT_STATUS, TEXT_STATUS2, ..., TEXT_STATUS12)
# Par défaut, les deux premiers ont des valeurs, les autres sont vides
STATUS_LIST = []
STATUS_LIST.append(os.getenv("TEXT_STATUS", "Version 1.0.0"))
STATUS_LIST.append(os.getenv("TEXT_STATUS2", "RecRDZ v0.2.0"))

for i in range(3, 13):
    status_val = os.getenv(f"TEXT_STATUS{i}")
    if status_val:
        STATUS_LIST.append(status_val)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@tasks.loop(seconds=60) # La boucle globale se répète toutes les minutes
async def change_status():
    # On rafraîchit la liste des statuts actifs à chaque cycle au cas où
    active_statuses = []
    # Statut 1 & 2 (toujours présents par défaut)
    active_statuses.append(os.getenv("TEXT_STATUS", "Version 1.0.0"))
    active_statuses.append(os.getenv("TEXT_STATUS2", "RecRDZ v0.2.0"))
    
    # Statuts 3 à 12 (seulement si définis)
    for i in range(3, 13):
        val = os.getenv(f"TEXT_STATUS{i}")
        if val:
            active_statuses.append(val)
    
    # Alternance entre les statuts actifs
    for status_text in active_statuses:
        await bot.change_presence(
            activity=discord.CustomActivity(name=status_text), 
            status=discord.Status.online
        )
        await asyncio.sleep(5) # 5 secondes par statut

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")
    print(f"ID : {bot.user.id}")
    print(f"Nombre de statuts configurés : {len(STATUS_LIST)}")
    if not change_status.is_running():
        change_status.start()
    print("Rotation des statuts (1-12) démarrée !")

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
