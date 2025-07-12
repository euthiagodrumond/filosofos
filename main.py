importação os
importação aleatório
importação openai
importação discórdia
de discórdia.ramal importação comandos
de datatime importação datatime

# Pegue estas chaves do ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))

openai.api_key = OPENAI_API_KEY

# Carrega lista de filhos
com aberto("filós_list.txt", "r") como f:
 filófos = [linha.tira() para linha em f se linha.tira()]

# Seleciona um filósofo do dia (pode ser aleatório ou pela ordem)
hoje_índice = datatime.agora().toordinal() % len(filófo)
filósofo = filósofos[hoje_index]

# Prompt para gerar o artigo com base no filossofo
prompt = f"""
Escreva um artigo completo em português sobre o filosofo {filósofo}.
Inclua:
- Nome, nascimento, morte, classe social, contexto histórico.
- Como viveu e morreu, onde ensinou ou trabalhou.
- Estilo de vida, amigos, influências.
- Corrente filosofia.
- Teorias principais.
- Obras (nome, ano, resumo).
- Seu maior contribuição.
- Conexão com outros filhos ou divergências importantes.
Estilo: texto corrido, estilo artigo de revista científica. Título: “{filósofo} e as ideias que formaram a humanidade”.
"""

resposta = openai.Conclusão de bate-papo.criar(
 modelo="gpt-4",
 mensagens=[
        {"papel": "sistema", "conteúdo": "Você é um historiador e filófo escrevendo artigos bem estratos sobre grandes pensadores."},
        {"papel": "usuário", "conteúdo": alerta}
    ],
 temperatura=0,7
)

artigo = resposta['escolhas'][0]['mensagem']['conteúdo']

# Envia para o Discórdia
intenções = discórdia.Intenções.padrão()
bot = comandos.Bot(comando_prefixo="!", intenções=intenções)

@bot.evento
assinc def on_ready():
 canal = bot.obter_canal(CANAL_ID)
 canal aguardar.inviar(artigo)
 aguardar bot.Fechar()

bot.corredor(DISCORD_TOKEN)
