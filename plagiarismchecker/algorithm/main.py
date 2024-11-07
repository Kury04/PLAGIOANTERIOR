from nltk.corpus import stopwords
from plagiarismchecker.algorithm import webSearch
import sys
import re

# Dada una cadena de texto, elimina todos los caracteres no alfanuméricos
def getQueries(text, n):
    sentenceEnders = re.compile("['.!?]")
    sentenceList = sentenceEnders.split(text)
    sentencesplits = []
    en_stops = set(stopwords.words('english'))

    for sentence in sentenceList:
        x = re.compile(r'\W+', re.UNICODE).split(sentence)
        # Filtrar palabras vacías (stopwords)
        x = [word for word in x if word.lower() not in en_stops and word]  # Uso de lista por comprensión
        if x:  # Solo agregar si x no está vacío
            sentencesplits.append(x)

    finalq = []
    for sentence in sentencesplits:
        l = len(sentence)
        if l > n:
            l = int(l / n)
            index = 0
            for i in range(0, l):
                finalq.append(sentence[index:index + n])
                index = index + n - 1
                if index + n > l:
                    index = l - n - 1
            if index != len(sentence):
                finalq.append(sentence[len(sentence) - index:len(sentence)])
        else:
            if l > 4:
                finalq.append(sentence)

    return finalq

def findSimilarity(text):
    n = 9
    queries = getQueries(text, n)
    print('GetQueries task complete')
    q = [' '.join(d) for d in queries]
    output = {}
    c = {}

    # Eliminar entradas vacías
    q = list(filter(None, q))
    count = len(q)
    if count > 100:
        count = 100
    numqueries = count

    for s in q[0:count]:
        output, c, errorCount = webSearch.searchWeb(s, output, c)
        print('Web search task complete')
        numqueries -= errorCount

    totalPercent = 0
    outputLink = {}
    prevlink = ''

    if numqueries > 0:
        for link in output:
            percentage = (output[link] * c[link] * 100) / numqueries
            if percentage > 10:
                totalPercent += percentage
                prevlink = link
                outputLink[link] = percentage
            elif len(prevlink) != 0:
                totalPercent += percentage
                outputLink[prevlink] += percentage
            elif c[link] == 1:
                totalPercent += percentage

        # Enviar los resultados al frontend
        print("Enlaces encontrados y sus valores de similitud:")
        for link, perc in outputLink.items():
            print(f"Link: {link} - Valor de Similitud: {perc}")

        # Retorna los resultados para la interfaz
        return totalPercent, outputLink  # Asegúrate de devolver estos resultados

    else:
        print("No hay consultas que procesar. No se puede calcular el porcentaje total.")

    print(count, numqueries)
    print(totalPercent, outputLink)
    print("\nConsulta completa")
    return totalPercent, outputLink
