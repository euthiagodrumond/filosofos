import os
import random
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Modelo melhorado com instruções
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Carregar filósofos
with open("philosophers_list.txt", "r", encoding="utf-8") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Escolher filósofo do dia
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Prompt mais limpo e específico
prompt = f"""Responda apenas em português. Escreva um parágrafo objetivo e claro sobre o filósofo {philosopher}.
Inclua:
- Onde nasceu
- Quando viveu
- Principais ideias
- Sua obra mais famosa

Não repita palavras e não inclua nenhum conteúdo em inglês. Não use listas. Escreva como se fosse um parágrafo de uma revista de filosofia brasileira.
"""

# Gerar resposta
inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=400,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
article = generated.replace(prompt.strip(), "").strip()

# Corta se passar de 1900 caracteres (limite seguro para Discord)
article = article[:1900]

# Enviar no Discord
import discord
from discord.ext import commands

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
