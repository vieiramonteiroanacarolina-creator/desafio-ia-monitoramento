import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Monitor de IA - Finanças", page_icon="💹")

st.title("🔍 Monitor de Atualização de Conteúdo")
st.write("Compare novas resoluções com o conteúdo das aulas.")

# Entrada da chave da API na barra lateral
api_key = st.sidebar.text_input("Insira sua OpenAI API Key", type="password")

col1, col2 = st.columns(2)

with col1:
    norma = st.text_area("Texto da Nova Resolução (CVM/ANBIMA):", height=300, placeholder="Cole a nova regra aqui...")

with col2:
    aula = st.text_area("Conteúdo Atual da Aula/Curso:", height=300, placeholder="Cole a ementa ou transcrição da aula aqui...")

if st.button("Analisar Impacto com IA"):
    if not api_key:
        st.error("Por favor, insira sua chave da API da OpenAI na barra lateral esquerda.")
    elif not norma or not aula:
        st.warning("Preencha os dois campos (Norma e Aula) para que a IA possa comparar.")
    else:
        try:
            client = OpenAI(api_key=api_key)
            with st.spinner('A IA está analisando os textos...'):
                prompt = f"""
                Você é um especialista em regulação do mercado financeiro brasileiro.
                Analise se a 'Nova Norma' abaixo torna o 'Conteúdo da Aula' desatualizado.
                
                NOVA NORMA: {norma}
                CONTEÚDO DA AULA: {aula}
                
                Responda em português com:
                1. O conteúdo está desatualizado? (Sim/Não)
                2. Nível de Urgência (Baixo/Médio/Alto)
                3. O que exatamente mudou e precisa ser revisado?
                """
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.subheader("Resultado da Análise:")
                st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
