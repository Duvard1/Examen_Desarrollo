import streamlit as st
import requests

st.title("Clasificador de Texto")
st.title("Duvard Cisneros")
codigo = st.text_input("Ingresa el codigo: ")
texto = st.text_area("Ingresa el texto a clasificar: ")

if st.button("Clasificar"):
    if texto and codigo:
        response = requests.post('http://localhost:8008/clasificar', json={'codigo': codigo, 'texto': texto})
        if response.status_code == 200:
            resultados = response.json()
            resultado = resultados.get('resultado',{})
            historial = resultados.get('historial',[])


            st.subheader("Resultados de Clasificación")
            st.write(f"codigo: {resultado.get('codigo')}")
            st.write("Respuesta: ")

            for label, score in resultados.get('respuesta',{}).items():
                st.write(f"Etiqueta: {label}, Score: {score:.4f}")
            
            st.subheader("Historial de Clasificaciones")
            for item in historial:
                st.write(f"codigo: {item['codigo']}, Respuesta: {item['respuesta']}")
        else:
            st.error("Error en la clasificación")
    else:
        st.warning("Por favor, ingresa un texto")

