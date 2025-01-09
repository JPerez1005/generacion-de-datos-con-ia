import requests
from huggingface_hub import InferenceClient

def generate_image(prompt, token, model="stabilityai/stable-diffusion-xl-base-1.0"):
    """Genera una imagen a partir de un texto utilizando Hugging Face."""
    client = InferenceClient(model, token=token)
    return client.text_to_image(prompt)

def analyze_image(filename, api_url, headers):
    """Analiza una imagen utilizando un modelo de detección de objetos."""
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(api_url, headers=headers, data=data)
    return response.json()

def format_output(output):
    """Formatea la salida del análisis de objetos para una mejor lectura."""
    formatted_result = []
    if isinstance(output, list):
        for obj in output:
            label = obj.get("label", "Unknown")
            score = obj.get("score", 0)
            box = obj.get("box", [])
            formatted_result.append(f"Objeto: {label}, Confianza: {score:.2f}, Caja: {box}")
    else:
        formatted_result.append("No se detectaron objetos o el formato de la respuesta es inválido.")
    return formatted_result