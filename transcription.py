import streamlit as st
import whisper
import os

def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result['text']

st.title("Transcrição de Áudio com Whisper")

uploaded_file = st.file_uploader("Faça upload de um arquivo de áudio (mp3, wav, etc.)", type=["mp3", "wav", "m4a", "ogg", "flac"]) 

if uploaded_file is not None:
    with st.spinner('Transcrevendo áudio...'):
        # Salva o arquivo temporariamente
        with open("temp_audio", "wb") as f:
            f.write(uploaded_file.read())
        texto = transcribe_audio("temp_audio")
        st.subheader("Transcrição bruta:")
        st.write(texto)
        # Remove o arquivo temporário
        os.remove("temp_audio")