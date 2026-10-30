# Caso de estudio: artículo 11 vs artículo 16

A = A scoping review on how generative artificial intelligence transform assessment in higher education
B = Generative Artificial Intelligence in Tertiary Education: Assessment Redesign Principles and Considerations

## 1. Levenshtein

Fragmento A (primeros 15 caracteres del art. 11): "generative arti"
Fragmento B (primeros 15 caracteres del art. 16): "the emergence o"

|  | ε | t | h | e | ␣ | e | m | e | r | g | e | n | c | e | ␣ | o |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ε | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| g | 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| e | 2 | 2 | 2 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 8 | 9 | 10 | 11 | 12 | 13 |
| n | 3 | 3 | 3 | 3 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 8 | 9 | 10 | 11 | 12 |
| e | 4 | 4 | 4 | 3 | 4 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 9 | 9 | 10 | 11 |
| r | 5 | 5 | 5 | 4 | 4 | 4 | 4 | 5 | 5 | 6 | 7 | 8 | 9 | 10 | 10 | 11 |
| a | 6 | 6 | 6 | 5 | 5 | 5 | 5 | 5 | 6 | 6 | 7 | 8 | 9 | 10 | 11 | 11 |
| t | 7 | 6 | 7 | 6 | 6 | 6 | 6 | 6 | 6 | 7 | 7 | 8 | 9 | 10 | 11 | 12 |
| i | 8 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 8 | 8 | 9 | 10 | 11 | 12 |
| v | 9 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 9 | 9 | 10 | 11 | 12 |
| e | 10 | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 9 | 9 | 8 | 9 | 10 | 9 | 10 | 11 |
| ␣ | 11 | 10 | 10 | 9 | 8 | 9 | 9 | 9 | 9 | 10 | 9 | 9 | 10 | 10 | 9 | 10 |
| a | 12 | 11 | 11 | 10 | 9 | 9 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 11 | 10 | 10 |
| r | 13 | 12 | 12 | 11 | 10 | 10 | 10 | 11 | 10 | 11 | 11 | 11 | 11 | 11 | 11 | 11 |
| t | 14 | 13 | 13 | 12 | 11 | 11 | 11 | 11 | 11 | 11 | 12 | 12 | 12 | 12 | 12 | 12 |
| i | 15 | 14 | 14 | 13 | 12 | 12 | 12 | 12 | 12 | 12 | 12 | 13 | 13 | 13 | 13 | 13 |

Distancia del fragmento = D[15][15] = 13
Similitud del fragmento = 1 - 13/15 = 0.1333
Tamaño de la matriz con los abstracts completos: 1380 x 1089 = 1502820 casillas

## 2 y 3. Jaccard y Dice

|A| (palabras distintas del art. 11) = 78
|B| (palabras distintas del art. 16) = 72
A ∩ B = 12 palabras: generative, artificial, intelligence, challenges, education, assessment, retrieved, students, integrity, ai, rethink, provide
|A ∪ B| = 78 + 72 - 12 = 138

Jaccard = 12 / 138 = 0.0870
Dice = 2·12 / (78 + 72) = 24 / 150 = 0.1600

## 4. TF-IDF + coseno

N = 20 abstracts. idf = log10(N / df). peso = tf · idf.

Palabras comunes (las únicas que aportan al producto punto):

| palabra | tf A | tf B | df | idf | peso A | peso B | A×B |
|---|---|---|---|---|---|---|---|
| generative | 2 | 7 | 5 | 0.6021 | 1.2041 | 4.2144 | 5.0747 |
| artificial | 2 | 1 | 20 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| intelligence | 2 | 1 | 20 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| challenges | 1 | 1 | 6 | 0.5229 | 0.5229 | 0.5229 | 0.2734 |
| education | 4 | 2 | 18 | 0.0458 | 0.1830 | 0.0915 | 0.0167 |
| assessment | 8 | 3 | 10 | 0.3010 | 2.4082 | 0.9031 | 2.1749 |
| retrieved | 1 | 1 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| students | 2 | 1 | 8 | 0.3979 | 0.7959 | 0.3979 | 0.3167 |
| integrity | 1 | 1 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| ai | 2 | 7 | 18 | 0.0458 | 0.0915 | 0.3203 | 0.0293 |
| rethink | 1 | 1 | 2 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| provide | 1 | 1 | 10 | 0.3010 | 0.3010 | 0.3010 | 0.0906 |
| **Suma (producto punto)** |  |  |  |  |  |  | **10.9763** |

Producto punto A·B = 10.9763
|A| = raíz(94.2507) = 9.7083   (78 palabras con peso)
|B| = raíz(127.8083) = 11.3052   (72 palabras con peso)
cos(θ) = 10.9763 / (9.7083 · 11.3052) = 0.1000
θ = 84.26 grados

## 5 y 6. Modelos de IA (embeddings)

### all-MiniLM-L6-v2 (sentence-transformers, 384 dimensiones)
Dimensión del vector: 384
Primeros 5 valores A: -0.0728, 0.0169, 0.0063, 0.0105, -0.0377
Primeros 5 valores B: -0.0985, -0.0041, 0.0579, -0.0224, 0.0035
A·B = 0.7356   |A| = 1.0000   |B| = 1.0000
coseno = 0.7356 / (1.0000 · 1.0000) = 0.7356
distancia euclidiana = 0.7272

### glove-wiki-gigaword-100 (promedio de vectores de palabras, 100 dimensiones)
Dimensión del vector: 100
Primeros 5 valores A: -0.0549, 0.2585, -0.0634, 0.2285, 0.0170
Primeros 5 valores B: -0.0854, 0.2649, 0.1965, 0.1604, -0.0326
A·B = 7.6330   |A| = 3.1756   |B| = 2.5694
coseno = 7.6330 / (3.1756 · 2.5694) = 0.9355
distancia euclidiana = 1.1918

## Resumen

| Algoritmo | Similitud | Tiempo |
|---|---|---|
| Levenshtein | 0.2864 | 1.6749 s |
| Jaccard | 0.0870 | 0.0012 s |
| Dice | 0.1600 | 0.0012 s |
| TF-IDF + coseno | 0.1000 | 0.0096 s |
| MiniLM (IA) | 0.7356 | 0.0001 s |
| GloVe (IA) | 0.9355 | 0.0000 s |
