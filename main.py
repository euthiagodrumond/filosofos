import os
import random
from datetime import datetime
import google.generativeai as genai
import discord
from discord.ext import commands

# Configurar API Gemini com a chave correta
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use Gemini 1.5 Flash (mais rápido e gratuito para testes)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# Carregar lista de filósofos
with open("philosophers_list.txt", "r", encoding="utf-8") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Selecionar filósofo do dia
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Prompt completo
prompt = f"""
Escreva um artigo completo e objetivo em português sobre o filósofo {philosopher}.
Inclua:
- Onde nasceu, quando viveu, e classe social
- Seu contexto histórico e estilo de vida
- Onde lecionou ou atuou
- Seus amigos e influências filosóficas (ex: aristotélico, cartesiano, etc.)
- Suas principais teses
- Obra mais importante (nome, ano e resumo)
- Contribuição para a humanidade
- Como morreu
Use linguagem clara, parágrafos bem escritos, e estilo de revista científica.
"""

# Gerar resposta com Gemini 1.5
response = model.generate_content(prompt)
article = response.text.strip()

# Truncar para Discord
article = article[:1900]

# Enviar para o Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"📚 **{philosopher}**\n\n{article}")
    await bot.close()

bot.run(DISCORD_TOKEN)
