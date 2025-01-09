from huggingface_hub import InferenceClient
import streamlit as st
from data.imagenes import generate_image,analyze_image,format_output
from data.chat import envio_mensaje
from data.configuracion import token

def generador_de_imagenes(token):
    # Streamlit UI
    st.title("Generador y Analizador de Imágenes")

    
    prompt = st.text_input("Escribe un texto para generar la imagen:", "una cama y una silla")
    generate_button = st.button("Generar Imagen")

    if generate_button:
        st.write("Generando imagen...")
        api_url = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            # Generar imagen
            image = generate_image(prompt, token)
            output_filename = "output.png"
            image.save(output_filename)
            
            # Mostrar imagen generada
            st.image(image, caption="Imagen Generada", use_column_width=True)
            st.write(f"Imagen generada guardada como {output_filename}")
            
            # Analizar imagen
            st.write("Analizando la imagen...")
            output = analyze_image(output_filename, api_url, headers)
            st.write("Resultados del análisis de la imagen:")
            st.json(output)  # Mostrar JSON de salida
            
            # Formatear resultados
            formatted_result = format_output(output)
            st.write("Resultados Formateados:")
            for result in formatted_result:
                st.write(result)
        except Exception as e:
            st.error(f"Error: {e}")

def chat_con_ia(api_key):
    # Configuración de la API
    client = InferenceClient(api_key=api_key)

    # Título de la aplicación
    st.title("Chat con HuggingFace")

    # Sesión para almacenar el historial de chat
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": "¡Bienvenido! Pregúntame lo que quieras."}]

    # Mostrar el historial de chat
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"**Usuario:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Asistente:** {message['content']}")

    user_input = st.text_input("Escribe tu mensaje aquí:", key="input")

    if st.button("Enviar"):
        envio_mensaje(user_input, client)

def paginacion():
    tab1, tab2 = st.tabs(['Chat con inteligencia Artificial', 'Generar y detectar objetos en imagenes']); 
    with tab1: chat_con_ia(token)
    with tab2: generador_de_imagenes(token)

paginacion()