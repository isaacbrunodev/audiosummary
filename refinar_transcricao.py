"""
Módulo para refinar transcrições de áudio em português, corrigindo erros fonéticos/ortográficos e reescrevendo para maior coesão e fluidez.
"""
from transformers import pipeline
from symspellpy import SymSpell, Verbosity
import pkg_resources
import os
import re

# Inicializa o corretor fonético/ortográfico SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
# Carrega dicionário português (precisa estar disponível no projeto ou baixar)
# Exemplo: https://github.com/mammothb/symspellpy/blob/master/symspellpy/frequency_dictionary_pt_br.txt
pt_dict_path = os.path.join(os.path.dirname(__file__), 'frequency_dictionary_pt_br.txt')
if os.path.exists(pt_dict_path):
    sym_spell.load_dictionary(pt_dict_path, term_index=0, count_index=1)
else:
    # Se não houver dicionário, o módulo ainda funciona, mas sem correção fonética
    pass

# Carrega o modelo de parafraseamento em português
parafraseador = pipeline(
    "text2text-generation",
    model="unicamp-dl/ptt5-base-portuguese-vocab",
    tokenizer="unicamp-dl/ptt5-base-portuguese-vocab"
)

def split_sentences_pt(texto):
    # Split por ponto, interrogação, exclamação seguidos de espaço ou fim de linha
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', texto) if s.strip()]

def refinar_transcricao(texto: str) -> str:
    """
    Refina uma transcrição de áudio:
    1. Tokeniza em sentenças.
    2. Corrige fonética/ortografia com SymSpell.
    3. Parafraseia cada sentença com ptt5-base-portuguese-vocab.
    4. Junta tudo em um texto final coeso.
    """
    # 1. Segmentação em sentenças (substitui NLTK por regex)
    sentencas = split_sentences_pt(texto)
    sentencas_corrigidas = []
    for s in sentencas:
        # 2. Correção fonética/ortográfica
        if sym_spell.words:
            palavras = s.split()
            palavras_corrigidas = []
            for palavra in palavras:
                sugestoes = sym_spell.lookup(palavra, Verbosity.CLOSEST, max_edit_distance=2)
                if sugestoes:
                    palavras_corrigidas.append(sugestoes[0].term)
                else:
                    palavras_corrigidas.append(palavra)
            s_corrigida = ' '.join(palavras_corrigidas)
        else:
            s_corrigida = s
        # 3. Parafraseamento
        prompt = f"parafraseie: {s_corrigida}"
        parafraseada = parafraseador(prompt, max_length=128)[0]['generated_text']
        sentencas_corrigidas.append(parafraseada)
    # 4. Texto final
    texto_final = ' '.join(sentencas_corrigidas)
    return texto_final

# Exemplo de uso
if __name__ == "__main__":
    texto = "Já agendei a mão. Eu agendei o combo de 550 aqui, a consulta de necoológica mais..."
    print(refinar_transcricao(texto))
