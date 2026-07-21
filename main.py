import discord
from discord.ext import commands
import os
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
CUSTOM_STATUS = os.getenv("TEXT_STATUS", "Mon statut personnalisé par défaut")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté : {bot.user.name}")
    print(f"ID : {bot.user.id}")
    print(f"Statut personnalisé : {CUSTOM_STATUS}")
    await bot.change_presence(activity=discord.CustomActivity(name=CUSTOM_STATUS), status=discord.Status.online)
    print("Bot prêt !")

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
