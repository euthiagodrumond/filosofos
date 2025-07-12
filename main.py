import os
import random
from datetime import datetime
import google.generativeai as genai
import discord
from discord.ext import commands

# Pegar variáveis do ambiente
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Configurar modelo do Google
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Carregar lista de filósofos
with open("philosophers_list.txt", "r", encoding="utf-8") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Selecionar filósofo do dia
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Prompt completo
prompt = f"""
Escreva um artigo completo e detalhado em português sobre o filósofo {philosopher}.
Inclua:
- Onde nasceu, quando viveu, se fazia parte da elite ou não
- Seu contexto histórico e estilo de vida
- Onde lecionou ou trabalhou
- Seus amigos, influências e se era aristotélico, cartesiano, etc.
- Suas principais teses
- Obra mais importante (nome, ano, resumo)
- Contribuição para a humanidade
- Como morreu
Use linguagem clara, fluente, e estilo de revista científica.
"""

# Gerar resposta com Gemini
response = model.generate_content(prompt)
article = response.text.strip()

# Corta se passar do limite de mensagem do Discord (~2000)
article = article[:1900]

# Enviar para o Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"📚 **{philosopher}**\n\n{article}")
    await bot.close()

bot.run(DISCORD_TOKEN)
