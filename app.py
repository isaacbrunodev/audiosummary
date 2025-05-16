import streamlit as st
from transcription import transcribe_audio
from summarization import summarize_text
from preprocess import reescrever_com_gpt4
import os
import tempfile

def main():
    st.title("Audio Summary Application - PT-BR IA")
    st.write("""
    Faça upload de um arquivo de áudio (reunião, WhatsApp, aula, etc). O sistema irá transcrever, corrigir e resumir o conteúdo usando IA em português.
    """)

    audio_file = st.file_uploader("Upload do arquivo de áudio", type=["wav", "mp3", "m4a"])

    if audio_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
            tmp_file.write(audio_file.getbuffer())
            temp_audio_path = tmp_file.name
        try:
            st.info("Transcrevendo áudio...")
            transcription = transcribe_audio(temp_audio_path)
            st.text_area("Transcrição Bruta", transcription, height=200)

            st.info("Reescrevendo com GPT-4...")
            texto_reescrito = reescrever_com_gpt4(transcription)
            st.text_area("Transcrição Corrigida e Coesa (GPT-4)", texto_reescrito, height=200)

            st.info("Gerando resumo...")
            summary = summarize_text(texto_reescrito)
            st.text_area("Resumo", summary, height=100)

            st.download_button("Baixar Transcrição Bruta", transcription, file_name="transcricao.txt")
            st.download_button("Baixar Transcrição Corrigida (GPT-4)", texto_reescrito, file_name="transcricao_corrigida.txt")
            st.download_button("Baixar Resumo", summary, file_name="resumo.txt")
        except Exception as e:
            st.error(f"Erro ao processar o áudio: {e}")
        finally:
            os.remove(temp_audio_path)

if __name__ == "__main__":
    main()