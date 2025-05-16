# melhorar_coesao.py
"""
Módulo para melhorar a coesão textual de transcrições brutas usando modelos gratuitos HuggingFace e NLTK.
"""
import nltk
from transformers import pipeline
import torch

# Baixa o tokenizer do NLTK se necessário
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Carrega o modelo de correção gramatical/coesa
corretor = pipeline("text2text-generation", model="flexudy/t5-base-multi-sentence-doctor", device=0 if torch.cuda.is_available() else -1)
# Carrega o modelo de parafraseamento
parafraseador = pipeline(
    "text2text-generation",
    model="unicamp-dl/ptt5-base-portuguese-vocab",
    tokenizer="unicamp-dl/ptt5-base-portuguese-vocab"
    # device=0 if torch.cuda.is_available() else -1  # Remova ou ajuste se necessário
)

def melhorar_coesao_texto(texto_bruto: str) -> str:
    """
    Recebe um texto bruto, corrige pontuação/coesão e parafraseia para maior fluidez.
    1. Segmenta em sentenças.
    2. Corrige cada sentença com T5 Doctor.
    3. Parafraseia cada sentença com T5 Paraphrase.
    4. Junta tudo em um texto final coeso.
    """
    # 1. Segmentação em sentenças
    sentencas = nltk.sent_tokenize(texto_bruto)
    sentencas_corrigidas = []
    # 2. Corrige cada sentença
    for s in sentencas:
        prompt = f"fix: {s}"
        corrigida = corretor(prompt, max_length=128)[0]['generated_text']
        sentencas_corrigidas.append(corrigida)
    # 3. Texto intermediário
    texto_intermediario = ' '.join(sentencas_corrigidas)
    # 4. Parafraseia cada sentença
    sentencas_para = nltk.sent_tokenize(texto_intermediario)
    sentencas_parafraseadas = []
    for s in sentencas_para:
        prompt = f"Paraphrase: {s}"
        parafraseada = parafraseador(prompt, max_length=128)[0]['generated_text']
        sentencas_parafraseadas.append(parafraseada)
    # 5. Texto final
    texto_final = ' '.join(sentencas_parafraseadas)
    return texto_final

# Exemplo de uso
if __name__ == "__main__":
    texto_exemplo = "necoológica trisâmio cheitam. éé então tipo assim né? isso é um exemplo de transcrição sem pontuação ou coesão."
    print("Texto original:")
    print(texto_exemplo)
    print("\nTexto melhorado:")
    print(melhorar_coesao_texto(texto_exemplo))
