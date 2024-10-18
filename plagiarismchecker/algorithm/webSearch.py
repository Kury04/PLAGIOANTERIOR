import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from plagiarismchecker.algorithm import ConsineSim
from googleapiclient.discovery import build

# Configuración de la API de Google Custom Search
searchEngine_API = 'AIzaSyAQYLRBBeDQNxADPQtUnApntz78-urWEZI'
searchEngine_Id = '758ad3e78879f0e08'

# Inicializa Vertex AI
vertexai.init(project="plagio-inspector", location="us-central1")
model = GenerativeModel("gemini-1.5-flash-002")

# Configuración de generación de texto
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Configuración de seguridad
safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]

def searchWeb(text, output, c):
    try:
        resource = build("customsearch", 'v1', developerKey=searchEngine_API).cse()
        result = resource.list(q=text, cx=searchEngine_Id).execute()
        
        items = result.get('items', [])
        if not items:
            print("No se encontraron resultados.")
            return output, c, 1

        maxSim = 0
        itemLink = ''
        numList = min(5, len(items))  # Limitar a 5 resultados
        
        for item in items[:numList]:
            content = item.get('snippet', '')
            if content:  # Asegúrate de que el contenido no esté vacío
                simValue = ConsineSim.cosineSim(text, content)
                
                if simValue > maxSim:
                    maxSim = simValue
                    itemLink = item['link']
            
            if item['link'] in output:
                itemLink = item['link']
                break

        # Actualizar el conteo de resultados
        if itemLink in output:
            output[itemLink] += 1
            c[itemLink] = ((c[itemLink] * (output[itemLink] - 1) + maxSim) / output[itemLink])
        else:
            output[itemLink] = 1
            c[itemLink] = maxSim

        # Usar Vertex AI para análisis de texto
        chat = model.start_chat()
        try:
            vertex_response = chat.send_message(text)
            print("Respuesta de Vertex AI:", vertex_response)
        except Exception as e:
            print("Error al enviar mensaje a Vertex AI:", e)
            return output, c, 1  # Indica error

    except Exception as e:
        print("Error:", e)
        return output, c, 1
    
    return output, c, numList
