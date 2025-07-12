import os
import random
from datetime import datetime
import google.generativeai as genai
import discord
from discord.ext import commands

# Configurar a API Gemini com a variável correta
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Inicializar o modelo
model = genai.GenerativeModel("gemini-pro")

# Carregar lista de filósofos
with open("philosophers_list.txt", "r", encoding="utf-8") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Escolher filósofo com base na data
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Criar o prompt detalhado em português
prompt = f"""
Escreva um artigo completo em português sobre o filósofo {philosopher}.
Inclua:
- Onde nasceu, quando viveu, se fazia parte da elite ou não
- Seu contexto histórico e estilo de vida
- Onde lecionou ou trabalhou
- Seus amigos, influências e se era aristotélico, cartesiano, etc.
- Suas principais teses
- Obra mais importante (nome, ano, resumo)
- Contribuição para a humanidade
- Como morreu
Estilo: texto corrido, linguagem clara e fluente, como artigo de revista filosófica.
"""

# Gerar a resposta com o modelo Gemini
response = model.generate_content(prompt)
article = response.text.strip()

# Garantir que o texto não ultrapasse o limite do Discord
article = article[:1900]

# Inicializar o bot do Discord
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
