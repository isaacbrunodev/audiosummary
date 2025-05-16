# AudioSummary

Projeto para transcrição e refinamento de áudios em português usando Whisper, Streamlit e modelos de NLP.

## Funcionalidades
- Upload de arquivos de áudio via navegador (mp3, wav, m4a, ogg, flac)
- Transcrição automática com Whisper
- Pronto para refinamento/cohesão textual (ver `refinar_transcricao.py`)
- Pronto para uso em Docker ou local

## Como usar

### 1. Clonar o repositório
```bash
git clone https://github.com/isaacbrunodev/audiosummary.git
cd audiosummary
```

### 2. Instalar dependências (opção local)
> Recomendado: use Python 3.10, 3.11 ou 3.12
```bash
pip install -r requirements.txt
```

### 3. Rodar com Docker (recomendado)
```powershell
docker build -t audiosummary:latest .
docker run --rm -p 8501:8501 -v ${PWD}:/app audiosummary:latest streamlit run transcription.py
```
Se `${PWD}` não funcionar, use o caminho completo:
```powershell
docker run --rm -p 8501:8501 -v C:\Users\ISAACSANTOS\audiosummary:/app audiosummary:latest streamlit run transcription.py
```

### 4. Rodar localmente (sem Docker)
```powershell
streamlit run transcription.py
```

### 5. Usar a aplicação
- Acesse: http://localhost:8501
- Faça upload do seu arquivo de áudio
- Veja a transcrição na tela

## Observações
- Para funcionalidades de refinamento/cohesão, configure sua chave da OpenAI API em `preprocess.py` (veja instruções no arquivo).
- Não compartilhe sua chave da OpenAI publicamente.
- O projeto está pronto para ser expandido com sumarização, parafraseamento e outros módulos.

---

**Mantenedor:** [isaacbrunodev](https://github.com/isaacbrunodev)

Contribuições são bem-vindas!
