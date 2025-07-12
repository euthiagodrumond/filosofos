import os
import random
from datetime import datetime

from openai import OpenAI
import discord
from discord.ext import commands

# Pegando as chaves de ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Inicializando o cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Lendo a lista de filósofos
with open("philosophers_list.txt", "r", encoding="utf-8") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Selecionar filósofo com base no dia
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Prompt para o artigo
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

# Fazendo a chamada à API
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um historiador e filósofo escrevendo artigos bem estruturados sobre grandes pensadores."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7
)

# Pegando o conteúdo gerado
article = response.choices[0].message.content

# Enviando o texto para o Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(article)
    await bot.close()

bot.run(DISCORD_TOKEN)
