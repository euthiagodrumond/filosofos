import os
import random
import openai
import discord
from discord.ext import commands
from datetime import datetime

# Pegue estas chaves do ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

openai.api_key = OPENAI_API_KEY

# Carrega lista de filósofos
with open("philosophers_list.txt", "r") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Seleciona um filósofo do dia (pode ser aleatório ou pela ordem)
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Prompt para gerar o artigo com base no filósofo
prompt = f"""
Escreva um artigo completo em português sobre o filósofo {philosopher}.
Inclua:
- Nome, nascimento, morte, classe social, contexto histórico.
- Como viveu e morreu, onde ensinou ou trabalhou.
- Estilo de vida, amigos, influências.
- Corrente filosófica.
- Teorias principais.
- Obras (nome, ano, resumo).
- Seu maior contributo.
- Conexão com outros filósofos ou divergências importantes.
Estilo: texto corrido, estilo artigo de revista científica. Título: “{philosopher} e as ideias que formaram a humanidade”.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "Você é um historiador e filósofo escrevendo artigos bem estruturados sobre grandes pensadores."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
)

article = response['choices'][0]['message']['content']

# Envia para o Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(article)
    await bot.close()

bot.run(DISCORD_TOKEN)
