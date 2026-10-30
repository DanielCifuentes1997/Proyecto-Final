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
    # la minúscula está 32 posiciones después de la mayúscula
    if "A" <= caracter <= "Z":
        return chr(ord(caracter) + 32)
    return caracter


def es_letra(caracter):
    return "a" <= caracter <= "z"


def tokenizar(texto):
    """Recorre el texto letra por letra y lo separa en palabras en minúscula."""
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
    if actual != "":
        palabras.append(actual)
    return palabras


def quitar_stopwords(palabras):
    limpias = []
    for i in range(len(palabras)):
        p = palabras[i]
        if len(p) >= 2 and p not in STOPWORDS:
            limpias.append(p)
    return limpias


def preprocesar(texto):
    return quitar_stopwords(tokenizar(texto))


if __name__ == "__main__":
    frase = ("Since artificial intelligence (AI) is finding its way into more and more areas of "
             "everyday life, improving the AI skills of non-experts is important")
    print(preprocesar(frase))
