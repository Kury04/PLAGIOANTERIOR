import re
import math
from collections import Counter

WORD = re.compile(r'\w+')

# Devuelve la similitud de coseno entre dos vectores
def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    matchWords = {}
    
    for i in intersection:
        matchWords[i] = min(vec1[i], vec2[i])
    
    # Calcula el numerador
    numerator = sum([vec1[x] * matchWords[x] for x in intersection])
    
    # Calcula el denominador
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([matchWords[x]**2 for x in matchWords.keys()])
    
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    # Chequea división por cero
    if denominator == 0:
        return 0.0
    else:
        return float(numerator) / denominator

# Convierte el texto en un vector
def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)

# Retorna la similitud de coseno entre dos textos
def cosineSim(text1, text2):
    t1 = text1.lower()
    t2 = text2.lower()
    vector1 = text_to_vector(t1)
    vector2 = text_to_vector(t2)
    cosine = get_cosine(vector1, vector2)
    
    return cosine
