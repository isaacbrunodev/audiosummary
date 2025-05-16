# Baixe o dicionário de frequência em português para o SymSpell
# Execute este script dentro do container ou no host antes de rodar o app
import urllib.request

url = "https://raw.githubusercontent.com/mammothb/symspellpy/master/symspellpy/frequency_dictionary_pt_br.txt"
output = "frequency_dictionary_pt_br.txt"

print("Baixando dicionário de frequência em português...")
urllib.request.urlretrieve(url, output)
print("Download concluído: frequency_dictionary_pt_br.txt")
