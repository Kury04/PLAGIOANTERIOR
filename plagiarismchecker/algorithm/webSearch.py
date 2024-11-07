from googleapiclient.discovery import build
from plagiarismchecker.algorithm import ConsineSim

# Configuración de la API de Google Custom Search
searchEngine_API = 'AIzaSyCdC_2wCnMMGQmdAiZi6FfkHSwnRU82sOU' 
searchEngine_Id = 'd16f95807e09243f6'

# Función de búsqueda en la web
def searchWeb(text, output, c):
    try:
        # Inicializa el recurso de búsqueda
        resource = build("customsearch", 'v1', developerKey=searchEngine_API).cse()
        result = resource.list(q=text, cx=searchEngine_Id).execute()

        items = result.get('items', [])
        if not items:
            print("No se encontraron resultados.")
            return output, c, 0

        # Limitar a 5 resultados
        numList = min(5, len(items))
        maxSim = 0
        itemLinks = []  # Lista para almacenar los enlaces encontrados

        for item in items[:numList]:
            content = item.get('snippet', '')
            link = item.get('link', '')
            if content:  
                simValue = ConsineSim.cosineSim(text, content)
                
                # Almacenar el enlace y el valor de similitud
                itemLinks.append((link, simValue))
                
                if simValue > maxSim:
                    maxSim = simValue  # Actualiza la similitud máxima
            
            # Aumentar el conteo de resultados
            if link in output:
                output[link] += 1
                c[link] = ((c[link] * (output[link] - 1) + simValue) / output[link])
            else:
                output[link] = 1
                c[link] = simValue

        # Imprimir resultados
        print("Enlaces encontrados y sus valores de similitud:")
        for link, simValue in itemLinks:
            print(f"Link: {link} - Valor de Similitud: {simValue}")

        # Devolver la lista de enlaces y la similitud máxima
        return output, c, numList

    except Exception as e:
        print("Error:", e)
        return output, c, 0  # Cambiado a 0 para indicar error



