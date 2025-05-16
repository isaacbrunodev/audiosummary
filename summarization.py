from transformers import pipeline

# Função para resumir texto usando modelos transformers
# text: texto a ser resumido
# Retorna: texto resumido

def summarize_text(text):
    summarizer = pipeline("summarization")
    # O modelo pode ter limite de tokens, então pode ser necessário dividir textos grandes
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

resumidor = pipeline("summarization", model="facebook/bart-large-cnn")

def gerar_resumo(texto_limpo):
    return resumidor(texto_limpo, max_length=80, min_length=30, do_sample=False)[0]['summary_text']