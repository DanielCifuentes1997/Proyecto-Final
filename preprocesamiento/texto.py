"""
Preprocesamiento del texto de los abstracts.

Convierte un abstract en una lista de palabras limpias (tokens):
  1. pasar a minúsculas
  2. quitar signos (todo lo que no sea letra se vuelve separador)
  3. separar en palabras
  4. quitar las stopwords (palabras que no aportan significado)

Se hace letra por letra con ciclos, sin funciones de librerías,
para que el comportamiento sea transparente y se pueda analizar su T(n).
"""

# Palabras vacías del inglés (tomadas del seguimiento)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
    "can", "cannot", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "me", "more",
    "most", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
    "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should", "so", "some",
    "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we",
    "were", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "would", "you",
    "your", "yours", "yourself", "yourselves", "also", "using", "used", "paper", "study", "based",
    "results", "research", "aims", "may", "well", "one", "two", "three", "first", "second", "show",
    "shows", "found", "however", "within", "across", "et", "al",
}


def a_minuscula(caracter):
    """Si el carácter es una letra mayúscula (A-Z) devuelve su minúscula; si no, lo deja igual."""
    if "A" <= caracter <= "Z":
        # en la tabla de caracteres, cada minúscula está 32 posiciones después de su mayúscula
        return chr(ord(caracter) + 32)
    return caracter


def es_letra(caracter):
    """True si el carácter es una letra minúscula de la a a la z."""
    return "a" <= caracter <= "z"


def tokenizar(texto):
    """
    Pasos 1, 2 y 3: recorre el texto letra por letra.
    Va armando la palabra actual; cuando encuentra algo que no es letra
    (espacio, coma, punto, paréntesis, guion, número...), guarda la palabra y empieza otra.
    """
    palabras = []
    actual = ""
    for i in range(len(texto)):
        c = a_minuscula(texto[i])
        if es_letra(c):
            actual = actual + c
        else:
            if actual != "":
                palabras.append(actual)
            actual = ""
    if actual != "":  # la última palabra, si el texto no termina en signo
        palabras.append(actual)
    return palabras


def quitar_stopwords(palabras):
    """Paso 4: deja solo las palabras que no son stopwords y tienen 2 letras o más."""
    limpias = []
    for i in range(len(palabras)):
        p = palabras[i]
        if len(p) >= 2 and p not in STOPWORDS:
            limpias.append(p)
    return limpias


def preprocesar(texto):
    """Abstract original -> lista de palabras limpias."""
    return quitar_stopwords(tokenizar(texto))


if __name__ == "__main__":
    frase = ("Since artificial intelligence (AI) is finding its way into more and more areas of "
             "everyday life, improving the AI skills of non-experts is important")
    print("Tokens:", tokenizar(frase))
    print("Limpias:", preprocesar(frase))
