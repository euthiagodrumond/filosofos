import os
import random
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Escolher o modelo leve gratuito do Hugging Face
MODEL_NAME = "tiiuae/falcon-rw-1b"  # Pequeno, roda em CPU

# Carregar modelo e tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Carregar filósofos
with open("philosophers_list.txt", "r", encoding="utf-8") as f:
    philosophers = [line.strip() for line in f if line.strip()]

# Escolher filósofo do dia
today_index = datetime.now().toordinal() % len(philosophers)
philosopher = philosophers[today_index]

# Prompt reduzido por limitação do modelo
prompt = f"""
Escreva um resumo simples e informativo sobre o filósofo {philosopher}.
Inclua:
- Onde nasceu
- Quando viveu
- Principais ideias
- Obra mais importante
Texto em português, em parágrafo corrido.
"""

# Preparar input
inputs = tokenizer(prompt, return_tensors="pt")

# Gerar saída (em CPU)
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )

generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
article = generated.replace(prompt.strip(), "").strip()

# Enviar para o Discord (se configurado)
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
