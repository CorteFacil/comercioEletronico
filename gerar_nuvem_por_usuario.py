# Script para gerar nuvem de palavras por usuário/candidato
# Identifica automaticamente quem está falando baseado no contexto
# Requer: wordcloud, matplotlib, nltk

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
import os
import re
from collections import defaultdict

# Baixa stopwords do NLTK se necessário
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
from nltk.corpus import stopwords

ARQUIVO_TRANSCRICAO = 'data/transcricao.txt'
PASTA_IMAGENS = 'imgs'
os.makedirs(PASTA_IMAGENS, exist_ok=True)

# Stopwords em português
stopwords_pt = set(stopwords.words('portuguese'))
stopwords_pt.update(['senhor', 'senhora', 'candidato', 'candidata', 'professor', 'professora',
                    'ifis', 'debate', 'pergunta', 'resposta', 'minuto', 'minutos', 'bloco',
                    'agora', 'momento', 'gente', 'aqui', 'bom', 'ok', 'então', 'assim', 'também'])

def identificar_falantes(linhas):
    """
    Identifica automaticamente quem está falando baseado no contexto
    """
    falas_por_candidato = {
        'mediador': [],
        'adriana': [],
        'ludovico': []
    }
    
    # Padrões para identificar falantes
    padroes = {
        'mediador': [
            r'debate eleitoral',
            r'candidatos ao cargo de reitor',
            r'sejam todos muito bem-vindos',
            r'regras aqui',
            r'avisos importantes',
            r'primeiro bloco',
            r'segundo bloco',
            r'terceiro momento',
            r'convidamos',
            r'professor',
            r'candidata',
            r'candidato',
            r'ok',
            r'partir de agora',
            r'minutos para',
            r'passaremos então',
            r'próximo momento',
            r'encerra-se',
            r'considerações finais',
            r'vamos fazer',
            r'pessoal',
            r'aviso importante',
            r'intervalo',
            r'retomamos',
            r'sequência'
        ],
        'adriana': [
            r'sou adriana',
            r'candidata reitora',
            r'adriana peontkovic',
            r'adriana peondi-kovics',
            r'professora adriana',
            r'candidata adriana',
            r'candidata professora adriana',
            r'professora candidata adriana'
        ],
        'ludovico': [
            r'professor do vico',
            r'ludovico hortelébifaria',
            r'professor ludovico',
            r'candidato ludovico',
            r'professor ludovin',
            r'candidato ludovin',
            r'professor ludo vico',
            r'candidato professor ludo vico'
        ]
    }
    
    candidato_atual = 'mediador'  # Começa com o mediador
    
    for linha in linhas:
        linha_limpa = re.sub(r'\[\d{2}:\d{2}\]', '', linha).strip()
        if not linha_limpa:
            continue
            
        # Identifica quem está falando baseado nos padrões
        for candidato, padrao_list in padroes.items():
            for padrao in padrao_list:
                if re.search(padrao, linha_limpa.lower()):
                    candidato_atual = candidato
                    break
            if candidato_atual != 'mediador':
                break
        
        # Adiciona a fala ao candidato identificado
        falas_por_candidato[candidato_atual].append(linha_limpa)
    
    return falas_por_candidato

def gerar_nuvem_candidato(texto, nome_candidato, stopwords_pt):
    """
    Gera nuvem de palavras para um candidato específico
    """
    # Remove timestamps
    texto_limpo = re.sub(r'\[\d{2}:\d{2}\]', '', texto)
    
    # Gera a nuvem de palavras
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=stopwords_pt,
        collocations=False,
        max_words=100,
        colormap='viridis'
    ).generate(texto_limpo)
    
    # Plota e salva a imagem
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'Nuvem de Palavras - {nome_candidato.title()}', fontsize=16, pad=20)
    plt.tight_layout()
    
    # Salva a imagem
    nome_arquivo = f'nuvem_{nome_candidato.lower()}.png'
    caminho_arquivo = os.path.join(PASTA_IMAGENS, nome_arquivo)
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()
    
    return caminho_arquivo

def main():
    # Lê o arquivo de transcrição
    with open(ARQUIVO_TRANSCRICAO, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Identifica os falantes
    print("Identificando falantes...")
    falas_por_candidato = identificar_falantes(linhas)
    
    # Mostra estatísticas
    for candidato, falas in falas_por_candidato.items():
        print(f"{candidato.title()}: {len(falas)} falas")
    
    # Gera nuvens para cada candidato
    arquivos_gerados = []
    for candidato, falas in falas_por_candidato.items():
        if falas:  # Só gera se houver falas
            texto_candidato = ' '.join(falas)
            arquivo = gerar_nuvem_candidato(texto_candidato, candidato, stopwords_pt)
            arquivos_gerados.append(arquivo)
            print(f"Nuvem gerada para {candidato.title()}: {arquivo}")
    
    # Gera também uma nuvem geral para comparação
    texto_geral = ' '.join(linhas)
    arquivo_geral = gerar_nuvem_candidato(texto_geral, 'geral', stopwords_pt)
    arquivos_gerados.append(arquivo_geral)
    print(f"Nuvem geral gerada: {arquivo_geral}")
    
    print(f"\n✅ Total de {len(arquivos_gerados)} nuvens geradas com sucesso!")
    print("Arquivos gerados:")
    for arquivo in arquivos_gerados:
        print(f"  - {arquivo}")

if __name__ == '__main__':
    main() 
