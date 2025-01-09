import streamlit as st

def envio_mensaje(user_input,client):
    if user_input.strip():
            # Agregar el mensaje del usuario al historial
            st.session_state.messages.append({"role": "user", "content": user_input})

            # Preparar mensajes para la API
            chat_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

            # Realizar la consulta
            stream = client.chat.completions.create(
                model="Qwen/QwQ-32B-Preview",
                messages=chat_messages,
                max_tokens=500,
                stream=True
            )

            # Construir la respuesta del asistente
            assistant_response = ""
            for chunk in stream:
                delta_content = chunk.choices[0].delta.content
                assistant_response += delta_content

            # Agregar la respuesta final al historial
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            # Mostrar solo la respuesta final
            st.markdown(f"**Asistente:** {assistant_response}")