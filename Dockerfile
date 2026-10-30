# Paso 1: construir la página web
FROM node:22-alpine AS pagina
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Paso 2: servidor de Python con los algoritmos
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ backend/
COPY preprocesamiento/ preprocesamiento/
COPY similitud/ similitud/
COPY clustering/ clustering/
COPY busqueda/ busqueda/
COPY extraccion/ extraccion/
COPY datos/corpus.json datos/embeddings.json datos/
COPY --from=pagina /app/frontend/dist frontend/dist
ENV PORT=8000
CMD ["sh", "-c", "uvicorn backend.api:app --host 0.0.0.0 --port ${PORT}"]
