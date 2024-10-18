import re
import math
from nltk.corpus import stopwords

def findFileSimilarity(inputQuery, database):
    universalSetOfUniqueWords = []

    lowercaseQuery = inputQuery.lower()
    en_stops = set(stopwords.words('english'))

    # Reemplazar la puntuación por espacios y dividir
    queryWordList = re.sub(r"[^\w]", " ", lowercaseQuery).split()

    # Elimina stopwords del query
    queryWordList = [word for word in queryWordList if word not in en_stops]

    # Si la lista está vacía después de eliminar stopwords
    if not queryWordList:
        return 0

    for word in queryWordList:
        if word not in universalSetOfUniqueWords:
            universalSetOfUniqueWords.append(word)

    database1 = database.lower()

    # Reemplazar la puntuación por espacios y dividir
    databaseWordList = re.sub(r"[^\w]", " ", database1).split()

    # Elimina stopwords de la base de datos
    databaseWordList = [word for word in databaseWordList if word not in en_stops]

    # Si la lista está vacía después de eliminar stopwords
    if not databaseWordList:
        return 0

    for word in databaseWordList:
        if word not in universalSetOfUniqueWords:
            universalSetOfUniqueWords.append(word)

    queryTF = []
    databaseTF = []

    for word in universalSetOfUniqueWords:
        queryTfCounter = queryWordList.count(word)
        queryTF.append(queryTfCounter)

        databaseTfCounter = databaseWordList.count(word)
        databaseTF.append(databaseTfCounter)

    # Producto escalar
    dotProduct = sum([queryTF[i] * databaseTF[i] for i in range(len(queryTF))])

    # Magnitudes de los vectores
    queryVectorMagnitude = math.sqrt(sum([tf**2 for tf in queryTF]))
    databaseVectorMagnitude = math.sqrt(sum([tf**2 for tf in databaseTF]))

    # Verificar si alguna magnitud es 0 para evitar la división por 0
    if queryVectorMagnitude == 0 or databaseVectorMagnitude == 0:
        return 0

    # Calcular la similitud del coseno
    cosineSimilarity = dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)

    # Convertir la similitud en porcentaje
    matchPercentage = cosineSimilarity * 100

    return matchPercentage
